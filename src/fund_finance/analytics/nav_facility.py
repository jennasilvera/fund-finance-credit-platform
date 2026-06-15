from dataclasses import dataclass
from datetime import date
from decimal import Decimal

import pandas as pd
from sqlalchemy import text

from fund_finance.analytics.borrowing_base import calculate_subscription_borrowing_base
from fund_finance.db.connection import get_engine


@dataclass
class NavBorrowingBaseResult:
    facility_id: str
    fund_id: str
    facility_type: str
    reporting_date: str
    latest_nav_date: str
    gross_nav_usd: float
    eligible_nav_usd: float
    nav_advance_rate_pct: float
    nav_borrowing_base_usd: float
    subscription_borrowing_base_usd: float
    total_borrowing_base_usd: float
    outstanding_amount_usd: float
    availability_usd: float
    ltv_pct: float
    utilization_pct: float
    headroom_pct: float
    breach_flag: bool
    top_portfolio_company_concentration_pct: float
    top_sector_concentration_pct: float
    portfolio_detail: pd.DataFrame


def _to_float(value: object) -> float:
    if value is None:
        return 0.0

    if isinstance(value, Decimal):
        return float(value)

    return float(value)


def _get_facility(facility_id: str) -> dict:
    engine = get_engine()

    query = text(
        """
        SELECT
            facility_id,
            fund_id,
            facility_type,
            outstanding_amount_usd,
            nav_advance_rate_pct,
            max_ltv_pct,
            max_top_portfolio_company_pct,
            max_sector_concentration_pct
        FROM facility_terms
        WHERE facility_id = :facility_id;
        """
    )

    with engine.connect() as connection:
        dataframe = pd.read_sql(query, connection, params={"facility_id": facility_id})

    if dataframe.empty:
        raise ValueError(f"Facility not found: {facility_id}")

    return dataframe.iloc[0].to_dict()


def _get_latest_nav(fund_id: str, reporting_date: str) -> dict:
    engine = get_engine()

    query = text(
        """
        SELECT
            reporting_date,
            gross_nav_usd,
            net_nav_usd,
            quarter_over_quarter_nav_change_pct,
            audit_status
        FROM nav_history
        WHERE fund_id = :fund_id
          AND reporting_date <= :reporting_date
        ORDER BY reporting_date DESC
        LIMIT 1;
        """
    )

    with engine.connect() as connection:
        dataframe = pd.read_sql(
            query,
            connection,
            params={"fund_id": fund_id, "reporting_date": reporting_date},
        )

    if dataframe.empty:
        raise ValueError(f"No NAV history found for fund {fund_id} on or before {reporting_date}")

    return dataframe.iloc[0].to_dict()


def _get_portfolio(fund_id: str) -> pd.DataFrame:
    engine = get_engine()

    query = text(
        """
        SELECT
            company_id,
            company_name,
            sector,
            geography,
            cost_basis_usd,
            current_fair_value_usd,
            revenue_growth_pct,
            ebitda_margin_pct,
            cash_runway_months,
            valuation_mark,
            non_performing_flag
        FROM portfolio_companies
        WHERE fund_id = :fund_id
        ORDER BY current_fair_value_usd DESC;
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(query, connection, params={"fund_id": fund_id})


def calculate_nav_borrowing_base(
    facility_id: str,
    reporting_date: str | None = None,
) -> NavBorrowingBaseResult:
    """
    Calculate NAV or hybrid borrowing base.

    For NAV facilities:
    total borrowing base = eligible NAV * NAV advance rate

    For hybrid facilities:
    total borrowing base = subscription borrowing base + NAV borrowing base
    """

    if reporting_date is None:
        reporting_date = date.today().isoformat()

    facility = _get_facility(facility_id)
    facility_type = facility["facility_type"]

    if facility_type not in {"nav", "hybrid"}:
        raise ValueError(
            f"Facility {facility_id} is type '{facility_type}'. "
            "NAV borrowing base applies only to NAV or hybrid facilities."
        )

    fund_id = facility["fund_id"]
    latest_nav = _get_latest_nav(fund_id, reporting_date)
    portfolio = _get_portfolio(fund_id)

    if portfolio.empty:
        raise ValueError(f"No portfolio companies found for fund {fund_id}")

    portfolio = portfolio.copy()
    portfolio["current_fair_value_usd"] = portfolio["current_fair_value_usd"].astype(float)

    gross_nav = _to_float(latest_nav["gross_nav_usd"])
    net_nav = _to_float(latest_nav["net_nav_usd"])

    total_portfolio_value = float(portfolio["current_fair_value_usd"].sum())

    if total_portfolio_value <= 0:
        raise ValueError(f"Portfolio value is zero for fund {fund_id}")

    portfolio["portfolio_concentration_pct"] = (
        portfolio["current_fair_value_usd"] / total_portfolio_value
    ) * 100.0

    top_company_concentration = float(portfolio["portfolio_concentration_pct"].max())

    sector_summary = (
        portfolio.groupby("sector", as_index=False)["current_fair_value_usd"]
        .sum()
        .sort_values("current_fair_value_usd", ascending=False)
    )

    sector_summary["sector_concentration_pct"] = (
        sector_summary["current_fair_value_usd"] / total_portfolio_value
    ) * 100.0

    top_sector_concentration = float(sector_summary["sector_concentration_pct"].max())

    max_company_pct = _to_float(facility["max_top_portfolio_company_pct"])
    max_sector_pct = _to_float(facility["max_sector_concentration_pct"])

    portfolio["eligible_value_before_haircut_usd"] = portfolio["current_fair_value_usd"]

    if max_company_pct > 0:
        company_cap = total_portfolio_value * (max_company_pct / 100.0)
        portfolio["eligible_value_after_company_cap_usd"] = portfolio[
            "eligible_value_before_haircut_usd"
        ].clip(upper=company_cap)
    else:
        portfolio["eligible_value_after_company_cap_usd"] = portfolio[
            "eligible_value_before_haircut_usd"
        ]

    portfolio["performance_haircut_pct"] = 0.0

    portfolio.loc[
        portfolio["valuation_mark"] == "down",
        "performance_haircut_pct",
    ] = 10.0

    portfolio.loc[
        portfolio["non_performing_flag"].astype(bool),
        "performance_haircut_pct",
    ] = 25.0

    portfolio["eligible_nav_contribution_usd"] = portfolio[
        "eligible_value_after_company_cap_usd"
    ] * (1.0 - portfolio["performance_haircut_pct"] / 100.0)

    eligible_nav = min(float(portfolio["eligible_nav_contribution_usd"].sum()), net_nav)

    nav_advance_rate_pct = _to_float(facility["nav_advance_rate_pct"])
    nav_borrowing_base = eligible_nav * (nav_advance_rate_pct / 100.0)

    subscription_borrowing_base = 0.0

    if facility_type == "hybrid":
        subscription_result = calculate_subscription_borrowing_base(
            facility_id=facility_id,
            reporting_date=reporting_date,
        )
        subscription_borrowing_base = subscription_result.total_borrowing_base_usd

    total_borrowing_base = subscription_borrowing_base + nav_borrowing_base
    outstanding = _to_float(facility["outstanding_amount_usd"])

    availability = max(total_borrowing_base - outstanding, 0.0)

    ltv_pct = 0.0
    if eligible_nav > 0:
        ltv_pct = (outstanding / eligible_nav) * 100.0

    utilization_pct = 0.0
    headroom_pct = 0.0

    if total_borrowing_base > 0:
        utilization_pct = (outstanding / total_borrowing_base) * 100.0
        headroom_pct = (availability / total_borrowing_base) * 100.0

    max_ltv_pct = _to_float(facility["max_ltv_pct"])
    breach_flag = False

    if total_borrowing_base > 0 and outstanding > total_borrowing_base:
        breach_flag = True

    if max_ltv_pct > 0 and ltv_pct > max_ltv_pct:
        breach_flag = True

    if max_company_pct > 0 and top_company_concentration > max_company_pct:
        breach_flag = True

    if max_sector_pct > 0 and top_sector_concentration > max_sector_pct:
        breach_flag = True

    return NavBorrowingBaseResult(
        facility_id=facility_id,
        fund_id=fund_id,
        facility_type=facility_type,
        reporting_date=reporting_date,
        latest_nav_date=str(latest_nav["reporting_date"]),
        gross_nav_usd=gross_nav,
        eligible_nav_usd=eligible_nav,
        nav_advance_rate_pct=nav_advance_rate_pct,
        nav_borrowing_base_usd=nav_borrowing_base,
        subscription_borrowing_base_usd=subscription_borrowing_base,
        total_borrowing_base_usd=total_borrowing_base,
        outstanding_amount_usd=outstanding,
        availability_usd=availability,
        ltv_pct=ltv_pct,
        utilization_pct=utilization_pct,
        headroom_pct=headroom_pct,
        breach_flag=breach_flag,
        top_portfolio_company_concentration_pct=top_company_concentration,
        top_sector_concentration_pct=top_sector_concentration,
        portfolio_detail=portfolio,
    )


def save_nav_borrowing_base_snapshot(result: NavBorrowingBaseResult) -> str:
    engine = get_engine()

    compact_date = result.reporting_date.replace("-", "")[2:]
    snapshot_id = f"BBS{result.facility_id[-3:]}{compact_date}"

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                DELETE FROM borrowing_base_snapshots
                WHERE facility_id = :facility_id
                  AND reporting_date = :reporting_date;
                """
            ),
            {
                "facility_id": result.facility_id,
                "reporting_date": result.reporting_date,
            },
        )

        connection.execute(
            text(
                """
                INSERT INTO borrowing_base_snapshots (
                    snapshot_id,
                    facility_id,
                    reporting_date,
                    eligible_uncalled_commitments_usd,
                    eligible_nav_usd,
                    total_borrowing_base_usd,
                    outstanding_amount_usd,
                    availability_usd,
                    utilization_pct,
                    headroom_pct,
                    breach_flag
                )
                VALUES (
                    :snapshot_id,
                    :facility_id,
                    :reporting_date,
                    :eligible_uncalled_commitments_usd,
                    :eligible_nav_usd,
                    :total_borrowing_base_usd,
                    :outstanding_amount_usd,
                    :availability_usd,
                    :utilization_pct,
                    :headroom_pct,
                    :breach_flag
                );
                """
            ),
            {
                "snapshot_id": snapshot_id,
                "facility_id": result.facility_id,
                "reporting_date": result.reporting_date,
                "eligible_uncalled_commitments_usd": result.subscription_borrowing_base_usd,
                "eligible_nav_usd": result.eligible_nav_usd,
                "total_borrowing_base_usd": result.total_borrowing_base_usd,
                "outstanding_amount_usd": result.outstanding_amount_usd,
                "availability_usd": result.availability_usd,
                "utilization_pct": result.utilization_pct,
                "headroom_pct": result.headroom_pct,
                "breach_flag": result.breach_flag,
            },
        )

    return snapshot_id
