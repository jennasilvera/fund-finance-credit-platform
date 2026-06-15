from dataclasses import dataclass
from datetime import date
from decimal import Decimal

import pandas as pd
from sqlalchemy import text

from fund_finance.db.connection import get_engine


@dataclass
class BorrowingBaseResult:
    facility_id: str
    fund_id: str
    facility_type: str
    reporting_date: str
    eligible_uncalled_commitments_usd: float
    total_borrowing_base_usd: float
    outstanding_amount_usd: float
    availability_usd: float
    utilization_pct: float
    headroom_pct: float
    breach_flag: bool
    top_investor_concentration_pct: float
    top5_investor_concentration_pct: float
    investor_detail: pd.DataFrame


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
            commitment_amount_usd,
            outstanding_amount_usd,
            advance_rate_rated_pct,
            advance_rate_non_rated_pct,
            advance_rate_designated_pct,
            max_top_investor_concentration_pct,
            max_top5_investor_concentration_pct
        FROM facility_terms
        WHERE facility_id = :facility_id;
        """
    )

    with engine.connect() as connection:
        dataframe = pd.read_sql(query, connection, params={"facility_id": facility_id})

    if dataframe.empty:
        raise ValueError(f"Facility not found: {facility_id}")

    return dataframe.iloc[0].to_dict()


def _get_commitments_for_fund(fund_id: str) -> pd.DataFrame:
    engine = get_engine()

    query = text(
        """
        SELECT
            c.commitment_id,
            c.fund_id,
            c.investor_id,
            i.investor_name,
            i.investor_type,
            i.country,
            i.external_rating,
            i.internal_rating,
            i.investor_category,
            i.affiliate_group,
            i.included_in_borrowing_base_flag,
            i.liquidity_watch_flag,
            i.side_letter_restriction_flag,
            c.commitment_amount_usd,
            c.called_amount_usd,
            c.uncalled_amount_usd,
            c.default_status,
            c.exclusion_reason
        FROM capital_commitments c
        JOIN investors i
            ON c.investor_id = i.investor_id
        WHERE c.fund_id = :fund_id
        ORDER BY c.uncalled_amount_usd DESC;
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(query, connection, params={"fund_id": fund_id})


def _advance_rate_for_investor(row: pd.Series, facility: dict) -> float:
    if not row["eligible_for_borrowing_base"]:
        return 0.0

    investor_category = row["investor_category"]

    if investor_category == "rated_included":
        return _to_float(facility["advance_rate_rated_pct"]) / 100.0

    if investor_category == "non_rated_included":
        return _to_float(facility["advance_rate_non_rated_pct"]) / 100.0

    if investor_category == "designated":
        return _to_float(facility["advance_rate_designated_pct"]) / 100.0

    return 0.0


def calculate_subscription_borrowing_base(
    facility_id: str,
    reporting_date: str | None = None,
) -> BorrowingBaseResult:
    """
    Calculate a subscription-style borrowing base.

    Logic:
    1. Pull facility terms.
    2. Pull investor commitments for the related fund.
    3. Exclude ineligible, defaulting, restricted, and side-letter investors.
    4. Apply top-investor concentration cap.
    5. Apply investor-category advance rates.
    6. Calculate borrowing base, availability, utilization, and breach status.
    """

    if reporting_date is None:
        reporting_date = date.today().isoformat()

    facility = _get_facility(facility_id)
    facility_type = facility["facility_type"]

    if facility_type not in {"subscription", "hybrid"}:
        raise ValueError(
            f"Facility {facility_id} is type '{facility_type}'. "
            "Subscription borrowing base applies only to subscription or hybrid facilities."
        )

    fund_id = facility["fund_id"]
    commitments = _get_commitments_for_fund(fund_id)

    if commitments.empty:
        raise ValueError(f"No commitments found for fund {fund_id}")

    commitments = commitments.copy()

    numeric_columns = [
        "commitment_amount_usd",
        "called_amount_usd",
        "uncalled_amount_usd",
    ]

    for column in numeric_columns:
        commitments[column] = commitments[column].astype(float)

    commitments["eligible_for_borrowing_base"] = (
        commitments["included_in_borrowing_base_flag"].astype(bool)
        & (commitments["investor_category"] != "excluded")
        & (commitments["default_status"] != "defaulted")
        & (~commitments["side_letter_restriction_flag"].astype(bool))
    )

    commitments["eligibility_reason"] = "Eligible"

    commitments.loc[
        ~commitments["included_in_borrowing_base_flag"].astype(bool),
        "eligibility_reason",
    ] = "Excluded by investor flag"

    commitments.loc[
        commitments["investor_category"] == "excluded",
        "eligibility_reason",
    ] = "Excluded investor category"

    commitments.loc[
        commitments["default_status"] == "defaulted",
        "eligibility_reason",
    ] = "Defaulting investor"

    commitments.loc[
        commitments["side_letter_restriction_flag"].astype(bool),
        "eligibility_reason",
    ] = "Side-letter restriction"

    commitments["pre_cap_eligible_uncalled_usd"] = commitments.apply(
        lambda row: row["uncalled_amount_usd"] if row["eligible_for_borrowing_base"] else 0.0,
        axis=1,
    )

    total_pre_cap_eligible_uncalled = float(
        commitments["pre_cap_eligible_uncalled_usd"].sum()
    )

    top_investor_concentration_pct = 0.0
    top5_investor_concentration_pct = 0.0

    if total_pre_cap_eligible_uncalled > 0:
        eligible_uncalled_sorted = commitments["pre_cap_eligible_uncalled_usd"].sort_values(
            ascending=False
        )
        top_investor_concentration_pct = (
            float(eligible_uncalled_sorted.iloc[0]) / total_pre_cap_eligible_uncalled
        ) * 100.0
        top5_investor_concentration_pct = (
            float(eligible_uncalled_sorted.head(5).sum()) / total_pre_cap_eligible_uncalled
        ) * 100.0

    top_investor_limit_pct = _to_float(
        facility["max_top_investor_concentration_pct"]
    )

    if top_investor_limit_pct > 0 and total_pre_cap_eligible_uncalled > 0:
        single_investor_cap = total_pre_cap_eligible_uncalled * (
            top_investor_limit_pct / 100.0
        )
    else:
        single_investor_cap = total_pre_cap_eligible_uncalled

    commitments["post_concentration_cap_uncalled_usd"] = commitments[
        "pre_cap_eligible_uncalled_usd"
    ].clip(upper=single_investor_cap)

    commitments["advance_rate"] = commitments.apply(
        lambda row: _advance_rate_for_investor(row, facility),
        axis=1,
    )

    commitments["borrowing_base_contribution_usd"] = (
        commitments["post_concentration_cap_uncalled_usd"] * commitments["advance_rate"]
    )

    eligible_uncalled_commitments = float(
        commitments["post_concentration_cap_uncalled_usd"].sum()
    )

    total_borrowing_base = float(commitments["borrowing_base_contribution_usd"].sum())
    outstanding = _to_float(facility["outstanding_amount_usd"])

    availability = max(total_borrowing_base - outstanding, 0.0)

    utilization_pct = 0.0
    headroom_pct = 0.0

    if total_borrowing_base > 0:
        utilization_pct = (outstanding / total_borrowing_base) * 100.0
        headroom_pct = (availability / total_borrowing_base) * 100.0

    breach_flag = outstanding > total_borrowing_base

    investor_detail_columns = [
        "investor_id",
        "investor_name",
        "investor_category",
        "internal_rating",
        "uncalled_amount_usd",
        "eligible_for_borrowing_base",
        "eligibility_reason",
        "pre_cap_eligible_uncalled_usd",
        "post_concentration_cap_uncalled_usd",
        "advance_rate",
        "borrowing_base_contribution_usd",
    ]

    investor_detail = commitments[investor_detail_columns].sort_values(
        "borrowing_base_contribution_usd",
        ascending=False,
    )

    return BorrowingBaseResult(
        facility_id=facility_id,
        fund_id=fund_id,
        facility_type=facility_type,
        reporting_date=reporting_date,
        eligible_uncalled_commitments_usd=eligible_uncalled_commitments,
        total_borrowing_base_usd=total_borrowing_base,
        outstanding_amount_usd=outstanding,
        availability_usd=availability,
        utilization_pct=utilization_pct,
        headroom_pct=headroom_pct,
        breach_flag=breach_flag,
        top_investor_concentration_pct=top_investor_concentration_pct,
        top5_investor_concentration_pct=top5_investor_concentration_pct,
        investor_detail=investor_detail,
    )


def save_borrowing_base_snapshot(result: BorrowingBaseResult) -> str:
    """Persist a borrowing base result to borrowing_base_snapshots."""
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
                    0,
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
                "eligible_uncalled_commitments_usd": result.eligible_uncalled_commitments_usd,
                "total_borrowing_base_usd": result.total_borrowing_base_usd,
                "outstanding_amount_usd": result.outstanding_amount_usd,
                "availability_usd": result.availability_usd,
                "utilization_pct": result.utilization_pct,
                "headroom_pct": result.headroom_pct,
                "breach_flag": result.breach_flag,
            },
        )

    return snapshot_id


def get_borrowing_base_snapshots() -> pd.DataFrame:
    engine = get_engine()

    query = text(
        """
        SELECT
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
        FROM borrowing_base_snapshots
        ORDER BY reporting_date DESC, facility_id;
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(query, connection)
