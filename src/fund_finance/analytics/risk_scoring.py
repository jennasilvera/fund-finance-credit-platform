from dataclasses import dataclass
from datetime import date

import pandas as pd
from sqlalchemy import text

from fund_finance.analytics.borrowing_base import calculate_subscription_borrowing_base
from fund_finance.analytics.covenant_monitoring import run_covenant_monitoring
from fund_finance.analytics.nav_facility import calculate_nav_borrowing_base
from fund_finance.db.connection import get_engine


@dataclass
class CreditScoreResult:
    facility_id: str
    fund_id: str
    fund_name: str
    facility_type: str
    analysis_date: str
    sponsor_score: float
    investor_base_score: float
    fund_performance_score: float
    collateral_score: float
    liquidity_score: float
    covenant_score: float
    reporting_score: float
    total_score: float
    credit_rating: str
    recommendation: str
    key_strengths: str
    key_risks: str
    required_mitigants: str


def _get_facility_context(facility_id: str) -> dict:
    engine = get_engine()

    query = text(
        """
        SELECT
            ft.facility_id,
            ft.facility_type,
            ft.commitment_amount_usd,
            ft.outstanding_amount_usd,
            ft.maturity_date,
            f.fund_id,
            f.fund_name,
            f.fund_type,
            f.vintage_year,
            f.committed_capital_usd,
            f.called_capital_usd,
            f.uncalled_capital_usd,
            f.nav_usd,
            f.dpi,
            f.tvpi,
            f.net_irr,
            f.fund_status,
            fm.manager_name,
            fm.total_aum_usd,
            fm.years_operating,
            fm.prior_funds_count,
            fm.realized_track_record_flag,
            fm.sponsor_risk_rating
        FROM facility_terms ft
        JOIN funds f
            ON ft.fund_id = f.fund_id
        JOIN fund_managers fm
            ON f.manager_id = fm.manager_id
        WHERE ft.facility_id = :facility_id;
        """
    )

    with engine.connect() as connection:
        dataframe = pd.read_sql(query, connection, params={"facility_id": facility_id})

    if dataframe.empty:
        raise ValueError(f"Facility not found: {facility_id}")

    return dataframe.iloc[0].to_dict()


def _get_latest_nav_change(fund_id: str, analysis_date: str) -> float:
    engine = get_engine()

    query = text(
        """
        SELECT quarter_over_quarter_nav_change_pct
        FROM nav_history
        WHERE fund_id = :fund_id
          AND reporting_date <= :analysis_date
        ORDER BY reporting_date DESC
        LIMIT 1;
        """
    )

    with engine.connect() as connection:
        value = connection.execute(
            query,
            {"fund_id": fund_id, "analysis_date": analysis_date},
        ).scalar()

    return float(value or 0.0)


def _get_open_monitoring_events(facility_id: str, analysis_date: str) -> pd.DataFrame:
    engine = get_engine()

    query = text(
        """
        SELECT
            event_id,
            event_type,
            severity,
            description,
            recommended_action
        FROM monitoring_events
        WHERE facility_id = :facility_id
          AND event_date <= :analysis_date
          AND resolved_flag = false
        ORDER BY event_date DESC;
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(
            query,
            connection,
            params={"facility_id": facility_id, "analysis_date": analysis_date},
        )


def _score_sponsor(context: dict) -> float:
    sponsor_rating = str(context["sponsor_risk_rating"]).lower()
    years_operating = int(context["years_operating"])
    prior_funds = int(context["prior_funds_count"])
    realized_track_record = bool(context["realized_track_record_flag"])

    if sponsor_rating == "strong":
        score = 88.0
    elif sponsor_rating == "acceptable":
        score = 74.0
    else:
        score = 55.0

    if years_operating >= 15:
        score += 5
    if prior_funds >= 4:
        score += 4
    if realized_track_record:
        score += 3

    return min(score, 100.0)


def _score_investor_base(facility_type: str, subscription_result) -> float:
    if facility_type == "nav" or subscription_result is None:
        return 75.0

    top_1 = subscription_result.top_investor_concentration_pct
    top_5 = subscription_result.top5_investor_concentration_pct

    if top_1 <= 20 and top_5 <= 55:
        return 90.0

    if top_1 <= 25 and top_5 <= 65:
        return 78.0

    if top_1 <= 35 and top_5 <= 75:
        return 60.0

    return 40.0


def _score_fund_performance(context: dict, latest_nav_change_pct: float) -> float:
    tvpi = float(context["tvpi"])
    dpi = float(context["dpi"])
    net_irr = float(context["net_irr"])

    score = 50.0

    if tvpi >= 1.50:
        score += 22
    elif tvpi >= 1.20:
        score += 15
    elif tvpi >= 1.00:
        score += 8

    if dpi >= 0.50:
        score += 10
    elif dpi >= 0.10:
        score += 5

    if net_irr >= 18:
        score += 12
    elif net_irr >= 12:
        score += 8
    elif net_irr >= 8:
        score += 4

    if latest_nav_change_pct <= -10:
        score -= 15
    elif latest_nav_change_pct <= -5:
        score -= 8

    return max(min(score, 100.0), 0.0)


def _score_collateral(facility_type: str, subscription_result, nav_result) -> float:
    if facility_type == "subscription" and subscription_result is not None:
        utilization = subscription_result.utilization_pct

        if utilization <= 40:
            score = 90.0
        elif utilization <= 65:
            score = 78.0
        elif utilization <= 85:
            score = 62.0
        else:
            score = 42.0

        if subscription_result.breach_flag:
            score = min(score, 45.0)

        return score

    if nav_result is not None:
        ltv = nav_result.ltv_pct

        if ltv <= 10:
            score = 90.0
        elif ltv <= 20:
            score = 78.0
        elif ltv <= 30:
            score = 60.0
        else:
            score = 35.0

        if nav_result.top_portfolio_company_concentration_pct > 25:
            score -= 10

        if nav_result.top_sector_concentration_pct > 40:
            score -= 10

        if nav_result.breach_flag:
            score = min(score, 45.0)

        return max(score, 0.0)

    return 50.0


def _score_liquidity(subscription_result, nav_result) -> float:
    active_result = nav_result or subscription_result

    if active_result is None:
        return 50.0

    outstanding = active_result.outstanding_amount_usd
    availability = active_result.availability_usd

    if outstanding <= 0:
        return 90.0

    availability_to_outstanding = availability / outstanding

    if availability_to_outstanding >= 1.00:
        return 90.0

    if availability_to_outstanding >= 0.50:
        return 75.0

    if availability_to_outstanding >= 0.15:
        return 58.0

    if availability > 0:
        return 45.0

    return 30.0


def _score_covenants(covenant_results) -> float:
    breaches = [result for result in covenant_results if result.result == "BREACH"]

    if not breaches:
        return 88.0

    high_breaches = [
        result
        for result in breaches
        if result.breach_severity in {"high", "event_of_default"}
    ]

    if len(high_breaches) >= 2:
        return 25.0

    if len(high_breaches) == 1:
        return 42.0

    if len(breaches) == 1:
        return 60.0

    return 45.0


def _score_reporting(events: pd.DataFrame) -> float:
    if events.empty:
        return 88.0

    severities = set(events["severity"].str.lower().tolist())

    if "critical" in severities:
        return 25.0

    if "high" in severities:
        return 45.0

    if "medium" in severities:
        return 65.0

    return 78.0


def _rating_from_score(total_score: float) -> str:
    if total_score >= 85:
        return "Strong"
    if total_score >= 70:
        return "Acceptable"
    if total_score >= 55:
        return "Watchlist"
    if total_score >= 40:
        return "Weak"
    return "Problem Credit"


def _recommendation_from_score(total_score: float, covenant_results) -> str:
    breaches = [result for result in covenant_results if result.result == "BREACH"]

    # Credit-policy override:
    # Any covenant breach should be escalated for credit officer review,
    # even if the overall quantitative score remains acceptable.
    if breaches:
        return "escalate"

    if total_score >= 85:
        return "approve"

    if total_score >= 70:
        return "approve_with_conditions"

    if total_score >= 55:
        return "monitor"

    if total_score >= 40:
        return "escalate"

    return "decline"


def _build_strengths(context: dict, subscription_result, nav_result, sponsor_score: float) -> str:
    strengths = []

    if sponsor_score >= 85:
        strengths.append("Experienced sponsor with strong institutional track record")

    if context["tvpi"] >= 1.2:
        strengths.append("Fund performance remains above cost on a TVPI basis")

    if subscription_result is not None and not subscription_result.breach_flag:
        strengths.append("Subscription borrowing base supports current utilization")

    if nav_result is not None and nav_result.ltv_pct <= 20:
        strengths.append("NAV LTV remains moderate relative to policy threshold")

    if not strengths:
        strengths.append("Transaction has identifiable collateral support but requires monitoring")

    return "; ".join(strengths)


def _build_risks(covenant_results, events: pd.DataFrame, subscription_result, nav_result) -> str:
    risks = []

    breaches = [result for result in covenant_results if result.result == "BREACH"]

    for breach in breaches:
        risks.append(f"{breach.covenant_name} breach")

    if subscription_result is not None:
        if subscription_result.top5_investor_concentration_pct > 65:
            risks.append("Elevated top-five investor concentration")

    if nav_result is not None:
        if nav_result.top_portfolio_company_concentration_pct > 25:
            risks.append("Elevated top portfolio company concentration")
        if nav_result.top_sector_concentration_pct > 40:
            risks.append("Elevated sector concentration")

    if not events.empty:
        severe_events = events[events["severity"].isin(["high", "critical"])]
        if not severe_events.empty:
            risks.append("Open high-severity monitoring events")

    if not risks:
        risks.append("No material covenant breach identified as of analysis date")

    return "; ".join(risks)


def _build_mitigants(recommendation: str, covenant_results) -> str:
    if recommendation == "approve":
        return "Maintain routine quarterly monitoring and borrowing base reporting."

    if recommendation == "approve_with_conditions":
        return (
            "Require quarterly borrowing base certificate, NAV package, and prompt notice "
            "of investor or portfolio valuation changes."
        )

    if recommendation == "monitor":
        return (
            "Place on enhanced monitoring; refresh collateral analysis monthly and require "
            "management commentary on key risk drivers."
        )

    if recommendation == "escalate":
        breach_actions = [
            result.recommended_action
            for result in covenant_results
            if result.result == "BREACH"
        ]
        if breach_actions:
            return " ".join(breach_actions)

        return "Escalate to credit officer and prepare updated credit review."

    return "Decline or reduce exposure unless structure is materially improved."


def run_credit_scoring(
    facility_id: str,
    analysis_date: str | None = None,
) -> CreditScoreResult:
    if analysis_date is None:
        analysis_date = date.today().isoformat()

    context = _get_facility_context(facility_id)
    facility_type = context["facility_type"]

    subscription_result = None
    nav_result = None

    if facility_type in {"subscription", "hybrid"}:
        subscription_result = calculate_subscription_borrowing_base(
            facility_id=facility_id,
            reporting_date=analysis_date,
        )

    if facility_type in {"nav", "hybrid"}:
        nav_result = calculate_nav_borrowing_base(
            facility_id=facility_id,
            reporting_date=analysis_date,
        )

    covenant_results = run_covenant_monitoring(
        facility_id=facility_id,
        reporting_date=analysis_date,
    )

    open_events = _get_open_monitoring_events(
        facility_id=facility_id,
        analysis_date=analysis_date,
    )

    latest_nav_change = _get_latest_nav_change(
        fund_id=context["fund_id"],
        analysis_date=analysis_date,
    )

    sponsor_score = _score_sponsor(context)
    investor_base_score = _score_investor_base(facility_type, subscription_result)
    fund_performance_score = _score_fund_performance(context, latest_nav_change)
    collateral_score = _score_collateral(facility_type, subscription_result, nav_result)
    liquidity_score = _score_liquidity(subscription_result, nav_result)
    covenant_score = _score_covenants(covenant_results)
    reporting_score = _score_reporting(open_events)

    total_score = (
        sponsor_score * 0.20
        + investor_base_score * 0.20
        + fund_performance_score * 0.15
        + collateral_score * 0.15
        + liquidity_score * 0.10
        + covenant_score * 0.10
        + reporting_score * 0.10
    )

    credit_rating = _rating_from_score(total_score)
    recommendation = _recommendation_from_score(total_score, covenant_results)

    key_strengths = _build_strengths(
        context=context,
        subscription_result=subscription_result,
        nav_result=nav_result,
        sponsor_score=sponsor_score,
    )

    key_risks = _build_risks(
        covenant_results=covenant_results,
        events=open_events,
        subscription_result=subscription_result,
        nav_result=nav_result,
    )

    required_mitigants = _build_mitigants(
        recommendation=recommendation,
        covenant_results=covenant_results,
    )

    return CreditScoreResult(
        facility_id=facility_id,
        fund_id=context["fund_id"],
        fund_name=context["fund_name"],
        facility_type=facility_type,
        analysis_date=analysis_date,
        sponsor_score=sponsor_score,
        investor_base_score=investor_base_score,
        fund_performance_score=fund_performance_score,
        collateral_score=collateral_score,
        liquidity_score=liquidity_score,
        covenant_score=covenant_score,
        reporting_score=reporting_score,
        total_score=round(total_score, 2),
        credit_rating=credit_rating,
        recommendation=recommendation,
        key_strengths=key_strengths,
        key_risks=key_risks,
        required_mitigants=required_mitigants,
    )


def run_all_credit_scoring(analysis_date: str | None = None) -> list[CreditScoreResult]:
    if analysis_date is None:
        analysis_date = date.today().isoformat()

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

    return [
        run_credit_scoring(facility_id=facility_id, analysis_date=analysis_date)
        for facility_id in facility_ids
    ]


def save_credit_recommendation(result: CreditScoreResult) -> str:
    engine = get_engine()

    compact_date = result.analysis_date.replace("-", "")[2:]
    recommendation_id = f"REC{result.facility_id[-3:]}{compact_date}"

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                DELETE FROM credit_recommendations
                WHERE recommendation_id = :recommendation_id;
                """
            ),
            {"recommendation_id": recommendation_id},
        )

        connection.execute(
            text(
                """
                INSERT INTO credit_recommendations (
                    recommendation_id,
                    facility_id,
                    analysis_date,
                    risk_score,
                    credit_rating,
                    recommendation,
                    key_strengths,
                    key_risks,
                    required_mitigants,
                    analyst_name
                )
                VALUES (
                    :recommendation_id,
                    :facility_id,
                    :analysis_date,
                    :risk_score,
                    :credit_rating,
                    :recommendation,
                    :key_strengths,
                    :key_risks,
                    :required_mitigants,
                    :analyst_name
                );
                """
            ),
            {
                "recommendation_id": recommendation_id,
                "facility_id": result.facility_id,
                "analysis_date": result.analysis_date,
                "risk_score": result.total_score,
                "credit_rating": result.credit_rating,
                "recommendation": result.recommendation,
                "key_strengths": result.key_strengths,
                "key_risks": result.key_risks,
                "required_mitigants": result.required_mitigants,
                "analyst_name": "Portfolio Project Analyst",
            },
        )

    return recommendation_id


def get_credit_recommendations() -> pd.DataFrame:
    engine = get_engine()

    query = text(
        """
        SELECT
            cr.recommendation_id,
            cr.facility_id,
            f.fund_name,
            cr.analysis_date,
            cr.risk_score,
            cr.credit_rating,
            cr.recommendation,
            cr.key_strengths,
            cr.key_risks,
            cr.required_mitigants
        FROM credit_recommendations cr
        JOIN facility_terms ft
            ON cr.facility_id = ft.facility_id
        JOIN funds f
            ON ft.fund_id = f.fund_id
        ORDER BY cr.analysis_date DESC, cr.facility_id;
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(query, connection)
