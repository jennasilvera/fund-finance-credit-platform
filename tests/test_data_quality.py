from pathlib import Path

import pandas as pd

from fund_finance.controls.data_quality import validate_raw_data
from fund_finance.etl.generate_sample_data import generate_all


def test_generated_raw_data_passes_quality_checks():
    generate_all()

    issues = validate_raw_data()

    assert issues == []


def test_duplicate_primary_key_is_detected(tmp_path: Path):
    raw_dir = tmp_path

    for table_name, columns in {
        "fund_managers": ["manager_id", "manager_name", "sponsor_risk_rating"],
        "funds": [
            "fund_id",
            "manager_id",
            "fund_name",
            "committed_capital_usd",
            "called_capital_usd",
            "uncalled_capital_usd",
            "nav_usd",
        ],
        "investors": [
            "investor_id",
            "investor_name",
            "investor_category",
            "included_in_borrowing_base_flag",
        ],
        "capital_commitments": [
            "commitment_id",
            "fund_id",
            "investor_id",
            "commitment_amount_usd",
            "called_amount_usd",
            "uncalled_amount_usd",
            "default_status",
        ],
        "capital_calls": [
            "capital_call_id",
            "fund_id",
            "investor_id",
            "call_date",
            "due_date",
            "amount_called_usd",
            "amount_funded_usd",
            "status",
        ],
        "nav_history": ["nav_id", "fund_id", "reporting_date", "gross_nav_usd", "net_nav_usd"],
        "portfolio_companies": [
            "company_id",
            "fund_id",
            "company_name",
            "sector",
            "current_fair_value_usd",
        ],
        "facility_terms": [
            "facility_id",
            "fund_id",
            "facility_type",
            "commitment_amount_usd",
            "outstanding_amount_usd",
        ],
        "covenant_terms": ["covenant_id", "facility_id", "covenant_name", "threshold_value"],
        "monitoring_events": ["event_id", "fund_id", "facility_id", "event_date", "severity"],
    }.items():
        pd.DataFrame([{column: "x" for column in columns}]).to_csv(
            raw_dir / f"{table_name}.csv",
            index=False,
        )

    pd.DataFrame(
        [
            {
                "investor_id": "INV001",
                "investor_name": "Investor A",
                "investor_category": "rated_included",
                "included_in_borrowing_base_flag": True,
            },
            {
                "investor_id": "INV001",
                "investor_name": "Investor B",
                "investor_category": "rated_included",
                "included_in_borrowing_base_flag": True,
            },
        ]
    ).to_csv(raw_dir / "investors.csv", index=False)

    issues = validate_raw_data(raw_dir)

    assert any(issue.check_name == "primary_key_unique" for issue in issues)
