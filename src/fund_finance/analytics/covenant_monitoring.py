from dataclasses import dataclass
from datetime import date
from decimal import Decimal

import pandas as pd
from sqlalchemy import text

from fund_finance.analytics.borrowing_base import calculate_subscription_borrowing_base
from fund_finance.analytics.nav_facility import calculate_nav_borrowing_base
from fund_finance.db.connection import get_engine


@dataclass
class CovenantTestResult:
    facility_id: str
    covenant_id: str
    covenant_name: str
    covenant_type: str
    threshold_value: float
    threshold_unit: str
    actual_value: float
    result: str
    breach_severity: str
    recommended_action: str


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
            facility_type
        FROM facility_terms
        WHERE facility_id = :facility_id;
        """
    )

    with engine.connect() as connection:
        dataframe = pd.read_sql(query, connection, params={"facility_id": facility_id})

    if dataframe.empty:
        raise ValueError(f"Facility not found: {facility_id}")

    return dataframe.iloc[0].to_dict()


def _get_covenants(facility_id: str) -> pd.DataFrame:
    engine = get_engine()

    query = text(
        """
        SELECT
            covenant_id,
            facility_id,
            covenant_name,
            covenant_type,
            threshold_value,
            threshold_unit,
            test_frequency,
            breach_severity
        FROM covenant_terms
        WHERE facility_id = :facility_id
        ORDER BY covenant_id;
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(query, connection, params={"facility_id": facility_id})


def _recommend_action(covenant_name: str, result: str, severity: str) -> str:
    if result == "PASS":
        return "No action required. Continue routine monitoring."

    if "LTV" in covenant_name:
        return (
            "Escalate to credit officer; request updated NAV package; "
            "consider limiting incremental drawings."
        )

    if "Borrowing Base Coverage" in covenant_name:
        return (
            "Escalate borrowing base deficiency; request cure plan, paydown, "
            "or additional eligible collateral support."
        )

    if "Investor Concentration" in covenant_name:
        return (
            "Review LP exposure, confirm concentration-limit calculation, "
            "and consider excluding excess exposure from availability."
        )

    if "Portfolio Company Concentration" in covenant_name:
        return (
            "Escalate portfolio concentration issue; request portfolio update, "
            "valuation support, and exit/liquidity plan."
        )

    if "Sector Concentration" in covenant_name:
        return (
            "Review sector exposure and stress case; request portfolio manager commentary."
        )

    if severity in {"high", "event_of_default"}:
        return "Escalate to credit officer and prepare breach notice."

    return "Add to watchlist and continue enhanced monitoring."


def run_covenant_monitoring(
    facility_id: str,
    reporting_date: str | None = None,
) -> list[CovenantTestResult]:
    if reporting_date is None:
        reporting_date = date.today().isoformat()

    facility = _get_facility(facility_id)
    facility_type = facility["facility_type"]
    covenants = _get_covenants(facility_id)

    if covenants.empty:
        raise ValueError(f"No covenants found for facility {facility_id}")

    subscription_result = None
    nav_result = None

    if facility_type in {"subscription", "hybrid"}:
        subscription_result = calculate_subscription_borrowing_base(
            facility_id=facility_id,
            reporting_date=reporting_date,
        )

    if facility_type in {"nav", "hybrid"}:
        nav_result = calculate_nav_borrowing_base(
            facility_id=facility_id,
            reporting_date=reporting_date,
        )

    results: list[CovenantTestResult] = []

    for _, covenant in covenants.iterrows():
        covenant_name = str(covenant["covenant_name"])
        threshold_value = _to_float(covenant["threshold_value"])
        actual_value = 0.0
        passed = True

        if covenant_name == "Maximum Top Investor Concentration":
            if subscription_result is None:
                actual_value = 0.0
                passed = True
            else:
                actual_value = subscription_result.top_investor_concentration_pct
                passed = actual_value <= threshold_value

        elif covenant_name == "Minimum Borrowing Base Coverage":
            if subscription_result is None:
                actual_value = 0.0
                passed = False
            elif subscription_result.outstanding_amount_usd == 0:
                actual_value = 999.0
                passed = True
            else:
                actual_value = (
                    subscription_result.total_borrowing_base_usd
                    / subscription_result.outstanding_amount_usd
                )
                passed = actual_value >= threshold_value

        elif covenant_name == "Maximum LTV":
            if nav_result is None:
                actual_value = 0.0
                passed = True
            else:
                actual_value = nav_result.ltv_pct
                passed = actual_value <= threshold_value

        elif covenant_name == "Maximum Top Portfolio Company Concentration":
            if nav_result is None:
                actual_value = 0.0
                passed = True
            else:
                actual_value = nav_result.top_portfolio_company_concentration_pct
                passed = actual_value <= threshold_value

        elif covenant_name == "Maximum Sector Concentration":
            if nav_result is None:
                actual_value = 0.0
                passed = True
            else:
                actual_value = nav_result.top_sector_concentration_pct
                passed = actual_value <= threshold_value

        else:
            actual_value = 0.0
            passed = True

        result_label = "PASS" if passed else "BREACH"
        severity = str(covenant["breach_severity"])

        results.append(
            CovenantTestResult(
                facility_id=facility_id,
                covenant_id=str(covenant["covenant_id"]),
                covenant_name=covenant_name,
                covenant_type=str(covenant["covenant_type"]),
                threshold_value=threshold_value,
                threshold_unit=str(covenant["threshold_unit"]),
                actual_value=actual_value,
                result=result_label,
                breach_severity=severity,
                recommended_action=_recommend_action(
                    covenant_name=covenant_name,
                    result=result_label,
                    severity=severity,
                ),
            )
        )

    return results


def run_all_covenant_monitoring(reporting_date: str | None = None) -> list[CovenantTestResult]:
    if reporting_date is None:
        reporting_date = date.today().isoformat()

    engine = get_engine()

    query = text(
        """
        SELECT facility_id
        FROM facility_terms
        ORDER BY facility_id;
        """
    )

    with engine.connect() as connection:
        facility_ids = [row[0] for row in connection.execute(query).fetchall()]

    all_results: list[CovenantTestResult] = []

    for facility_id in facility_ids:
        all_results.extend(
            run_covenant_monitoring(
                facility_id=facility_id,
                reporting_date=reporting_date,
            )
        )

    return all_results


def save_covenant_breach_events(
    results: list[CovenantTestResult],
    reporting_date: str | None = None,
) -> int:
    if reporting_date is None:
        reporting_date = date.today().isoformat()

    breach_results = [result for result in results if result.result == "BREACH"]

    if not breach_results:
        return 0

    engine = get_engine()

    inserted = 0

    with engine.begin() as connection:
        for result in breach_results:
            facility = _get_facility(result.facility_id)
            compact_date = reporting_date.replace("-", "")[2:]
            event_id = f"BR{result.facility_id[-3:]}{result.covenant_id[-3:]}{compact_date}"

            connection.execute(
                text(
                    """
                    DELETE FROM monitoring_events
                    WHERE event_id = :event_id;
                    """
                ),
                {"event_id": event_id},
            )

            connection.execute(
                text(
                    """
                    INSERT INTO monitoring_events (
                        event_id,
                        fund_id,
                        facility_id,
                        event_date,
                        event_type,
                        severity,
                        description,
                        recommended_action,
                        escalation_required_flag,
                        resolved_flag
                    )
                    VALUES (
                        :event_id,
                        :fund_id,
                        :facility_id,
                        :event_date,
                        :event_type,
                        :severity,
                        :description,
                        :recommended_action,
                        :escalation_required_flag,
                        false
                    );
                    """
                ),
                {
                    "event_id": event_id,
                    "fund_id": facility["fund_id"],
                    "facility_id": result.facility_id,
                    "event_date": reporting_date,
                    "event_type": "Covenant breach",
                    "severity": "high"
                    if result.breach_severity in {"high", "event_of_default"}
                    else "medium",
                    "description": (
                        f"{result.covenant_name} breached. "
                        f"Actual value {result.actual_value:.2f} vs threshold "
                        f"{result.threshold_value:.2f} {result.threshold_unit}."
                    ),
                    "recommended_action": result.recommended_action,
                    "escalation_required_flag": result.breach_severity
                    in {"high", "event_of_default"},
                },
            )

            inserted += 1

    return inserted
