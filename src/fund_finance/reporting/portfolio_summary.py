from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

PORTFOLIO_SUMMARY_OUTPUT = Path("data/outputs/portfolio_summary.csv")


@dataclass(frozen=True)
class PortfolioSummaryExport:
    output_path: str
    row_count: int


def fetch_portfolio_summary(engine: Engine) -> pd.DataFrame:
    query = text(
        """
        WITH latest_recommendations AS (
            SELECT DISTINCT ON (facility_id)
                facility_id,
                risk_score,
                credit_rating,
                recommendation,
                analysis_date
            FROM credit_recommendations
            ORDER BY facility_id, analysis_date DESC
        ),
        open_events AS (
            SELECT
                facility_id,
                COUNT(*) FILTER (
                    WHERE COALESCE(resolved_flag, false) = false
                ) AS open_monitoring_events,
                COUNT(*) FILTER (
                    WHERE COALESCE(escalation_required_flag, false) = true
                    AND COALESCE(resolved_flag, false) = false
                ) AS escalation_events
            FROM monitoring_events
            GROUP BY facility_id
        )
        SELECT
            ft.facility_id,
            f.fund_id,
            f.fund_name,
            ft.facility_type,
            ft.commitment_amount_usd,
            ft.outstanding_amount_usd,
            ft.max_ltv_pct,
            lr.risk_score,
            lr.credit_rating,
            lr.recommendation,
            COALESCE(oe.open_monitoring_events, 0) AS open_monitoring_events,
            COALESCE(oe.escalation_events, 0) AS escalation_events
        FROM facility_terms ft
        JOIN funds f
            ON ft.fund_id = f.fund_id
        LEFT JOIN latest_recommendations lr
            ON ft.facility_id = lr.facility_id
        LEFT JOIN open_events oe
            ON ft.facility_id = oe.facility_id
        ORDER BY ft.facility_id;
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(query, connection)


def export_portfolio_summary(
    engine: Engine,
    output_path: Path = PORTFOLIO_SUMMARY_OUTPUT,
) -> PortfolioSummaryExport:
    dataframe = fetch_portfolio_summary(engine)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False)

    return PortfolioSummaryExport(
        output_path=str(output_path),
        row_count=len(dataframe),
    )
