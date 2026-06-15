from typer.testing import CliRunner

from fund_finance.cli import app

runner = CliRunner()


def test_run_nav_stress_cli_detects_breach():
    result = runner.invoke(
        app,
        [
            "run-nav-stress",
            "--facility-id",
            "FAC002",
            "--eligible-nav-usd",
            "640000000",
            "--outstanding-amount-usd",
            "180000000",
            "--max-ltv-pct",
            "30",
        ],
    )

    assert result.exit_code == 0
    assert "NAV / LTV Stress Test: FAC002" in result.output
    assert "Stress breach detected" in result.output
    assert "YES" in result.output


def test_run_nav_stress_cli_detects_no_breach():
    result = runner.invoke(
        app,
        [
            "run-nav-stress",
            "--facility-id",
            "FAC003",
            "--eligible-nav-usd",
            "4435000000",
            "--outstanding-amount-usd",
            "320000000",
            "--max-ltv-pct",
            "30",
        ],
    )

    assert result.exit_code == 0
    assert "NAV / LTV Stress Test: FAC003" in result.output
    assert "No stress breaches detected" in result.output
