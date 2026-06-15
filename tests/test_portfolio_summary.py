from pathlib import Path

import pandas as pd

from fund_finance.reporting.portfolio_summary import PortfolioSummaryExport


def test_portfolio_summary_export_dataclass():
    export = PortfolioSummaryExport(
        output_path="data/outputs/portfolio_summary.csv",
        row_count=3,
    )

    assert export.output_path.endswith("portfolio_summary.csv")
    assert export.row_count == 3


def test_portfolio_summary_csv_can_be_written(tmp_path: Path):
    output_path = tmp_path / "portfolio_summary.csv"

    dataframe = pd.DataFrame(
        [
            {
                "facility_id": "FAC001",
                "fund_name": "Test Fund",
                "facility_type": "subscription",
                "recommendation": "Approve",
            }
        ]
    )

    dataframe.to_csv(output_path, index=False)

    loaded = pd.read_csv(output_path)

    assert loaded.loc[0, "facility_id"] == "FAC001"
    assert loaded.loc[0, "recommendation"] == "Approve"
