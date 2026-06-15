from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from fund_finance.analytics.borrowing_base import (
    calculate_subscription_borrowing_base,
    get_borrowing_base_snapshots,
    save_borrowing_base_snapshot,
)
from fund_finance.analytics.covenant_monitoring import (
    run_all_covenant_monitoring,
    run_covenant_monitoring,
    save_covenant_breach_events,
)
from fund_finance.analytics.nav_facility import (
    calculate_nav_borrowing_base,
    save_nav_borrowing_base_snapshot,
)
from fund_finance.analytics.risk_scoring import (
    get_credit_recommendations,
    run_all_credit_scoring,
    run_credit_scoring,
    save_credit_recommendation,
)
from fund_finance.db.connection import list_tables, test_connection
from fund_finance.db.load import count_loaded_rows, load_all_raw_data
from fund_finance.reporting.credit_memo import generate_credit_approval_memo

app = typer.Typer(
    help="Fund Finance Credit Underwriting & Portfolio Monitoring Platform"
)

console = Console()


def _format_usd(value: float) -> str:
    return f"${value:,.0f}"


def _format_pct(value: float) -> str:
    return f"{value:,.2f}%"


def _format_actual(value: float, unit: str) -> str:
    if unit == "percent":
        return _format_pct(value)

    if unit == "x":
        return f"{value:,.2f}x"

    return f"{value:,.2f}"


@app.command("check-db")
def check_db() -> None:
    """Check PostgreSQL connectivity and list available tables."""
    try:
        version = test_connection()
        tables = list_tables()
    except Exception as exc:
        console.print(f"[red]Database connection failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print("[green]Database connection successful.[/green]")
    console.print(f"[bold]PostgreSQL:[/bold] {version}")

    table = Table(title="Public Database Tables")
    table.add_column("Table Name", style="cyan")

    for table_name in tables:
        table.add_row(table_name)

    console.print(table)


@app.command("validate-schema-file")
def validate_schema_file() -> None:
    """Validate that sql/schema.sql exists and contains core tables."""
    schema_path = Path("sql/schema.sql")

    if not schema_path.exists():
        console.print("[red]Missing sql/schema.sql[/red]")
        raise typer.Exit(code=1)

    schema_text = schema_path.read_text()

    required_tables = [
        "fund_managers",
        "funds",
        "investors",
        "capital_commitments",
        "capital_calls",
        "nav_history",
        "portfolio_companies",
        "facility_terms",
        "covenant_terms",
        "borrowing_base_snapshots",
        "monitoring_events",
        "credit_recommendations",
        "audit_runs",
    ]

    missing = [table for table in required_tables if f"CREATE TABLE {table}" not in schema_text]

    if missing:
        console.print("[red]Schema validation failed. Missing tables:[/red]")
        for table_name in missing:
            console.print(f"- {table_name}")
        raise typer.Exit(code=1)

    console.print("[green]Schema file validation passed.[/green]")


@app.command("load-data")
def load_data() -> None:
    """Load generated raw CSV files into PostgreSQL."""
    try:
        row_counts = load_all_raw_data(reset=True)
    except Exception as exc:
        console.print(f"[red]Data load failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title="Loaded Raw Data")
    table.add_column("Table", style="cyan")
    table.add_column("Rows Loaded", justify="right", style="green")

    for table_name, row_count in row_counts.items():
        table.add_row(table_name, str(row_count))

    console.print(table)
    console.print("[green]Raw data load completed successfully.[/green]")


@app.command("row-counts")
def row_counts() -> None:
    """Show row counts for loaded source tables."""
    try:
        counts = count_loaded_rows()
    except Exception as exc:
        console.print(f"[red]Could not count rows:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title="Database Row Counts")
    table.add_column("Table", style="cyan")
    table.add_column("Rows", justify="right", style="green")

    for table_name, row_count in counts.items():
        table.add_row(table_name, str(row_count))

    console.print(table)


@app.command("run-subscription-borrowing-base")
def run_subscription_borrowing_base(
    facility_id: str = typer.Option(..., help="Facility ID, for example FAC001"),
    reporting_date: str = typer.Option("2025-12-31", help="Reporting date YYYY-MM-DD"),
    save: bool = typer.Option(True, help="Save result to borrowing_base_snapshots"),
) -> None:
    """Run subscription-style borrowing base analysis."""
    try:
        result = calculate_subscription_borrowing_base(
            facility_id=facility_id,
            reporting_date=reporting_date,
        )
    except Exception as exc:
        console.print(f"[red]Borrowing base calculation failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    summary = Table(title=f"Subscription Borrowing Base: {result.facility_id}")
    summary.add_column("Metric", style="cyan")
    summary.add_column("Value", justify="right", style="green")

    summary.add_row("Fund ID", result.fund_id)
    summary.add_row("Facility Type", result.facility_type)
    summary.add_row(
        "Eligible Uncalled Commitments",
        _format_usd(result.eligible_uncalled_commitments_usd),
    )
    summary.add_row("Total Borrowing Base", _format_usd(result.total_borrowing_base_usd))
    summary.add_row("Outstanding Amount", _format_usd(result.outstanding_amount_usd))
    summary.add_row("Availability", _format_usd(result.availability_usd))
    summary.add_row("Utilization", _format_pct(result.utilization_pct))
    summary.add_row("Headroom", _format_pct(result.headroom_pct))
    summary.add_row(
        "Top Investor Concentration",
        _format_pct(result.top_investor_concentration_pct),
    )
    summary.add_row(
        "Top 5 Investor Concentration",
        _format_pct(result.top5_investor_concentration_pct),
    )
    summary.add_row("Breach Flag", "YES" if result.breach_flag else "NO")

    console.print(summary)

    if save:
        snapshot_id = save_borrowing_base_snapshot(result)
        console.print(f"[green]Saved borrowing base snapshot:[/green] {snapshot_id}")


@app.command("run-nav-borrowing-base")
def run_nav_borrowing_base(
    facility_id: str = typer.Option(..., help="Facility ID, for example FAC002 or FAC003"),
    reporting_date: str = typer.Option("2025-12-31", help="Reporting date YYYY-MM-DD"),
    save: bool = typer.Option(True, help="Save result to borrowing_base_snapshots"),
) -> None:
    """Run NAV or hybrid borrowing base analysis."""
    try:
        result = calculate_nav_borrowing_base(
            facility_id=facility_id,
            reporting_date=reporting_date,
        )
    except Exception as exc:
        console.print(f"[red]NAV borrowing base calculation failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    summary = Table(title=f"NAV / Hybrid Borrowing Base: {result.facility_id}")
    summary.add_column("Metric", style="cyan")
    summary.add_column("Value", justify="right", style="green")

    summary.add_row("Fund ID", result.fund_id)
    summary.add_row("Facility Type", result.facility_type)
    summary.add_row("Latest NAV Date", result.latest_nav_date)
    summary.add_row("Gross NAV", _format_usd(result.gross_nav_usd))
    summary.add_row("Eligible NAV", _format_usd(result.eligible_nav_usd))
    summary.add_row("NAV Advance Rate", _format_pct(result.nav_advance_rate_pct))
    summary.add_row("NAV Borrowing Base", _format_usd(result.nav_borrowing_base_usd))
    summary.add_row(
        "Subscription Borrowing Base",
        _format_usd(result.subscription_borrowing_base_usd),
    )
    summary.add_row("Total Borrowing Base", _format_usd(result.total_borrowing_base_usd))
    summary.add_row("Outstanding Amount", _format_usd(result.outstanding_amount_usd))
    summary.add_row("Availability", _format_usd(result.availability_usd))
    summary.add_row("LTV", _format_pct(result.ltv_pct))
    summary.add_row("Utilization", _format_pct(result.utilization_pct))
    summary.add_row("Headroom", _format_pct(result.headroom_pct))
    summary.add_row(
        "Top Company Concentration",
        _format_pct(result.top_portfolio_company_concentration_pct),
    )
    summary.add_row("Top Sector Concentration", _format_pct(result.top_sector_concentration_pct))
    summary.add_row("Breach Flag", "YES" if result.breach_flag else "NO")

    console.print(summary)

    if save:
        snapshot_id = save_nav_borrowing_base_snapshot(result)
        console.print(f"[green]Saved NAV borrowing base snapshot:[/green] {snapshot_id}")


@app.command("borrowing-base-snapshots")
def borrowing_base_snapshots() -> None:
    """Show saved borrowing base snapshots."""
    try:
        snapshots = get_borrowing_base_snapshots()
    except Exception as exc:
        console.print(f"[red]Could not load borrowing base snapshots:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title="Borrowing Base Snapshots")
    table.add_column("Snapshot ID", style="cyan")
    table.add_column("Facility")
    table.add_column("Date")
    table.add_column("Borrowing Base", justify="right")
    table.add_column("Outstanding", justify="right")
    table.add_column("Availability", justify="right")
    table.add_column("Utilization", justify="right")
    table.add_column("Breach")

    for _, row in snapshots.iterrows():
        table.add_row(
            row["snapshot_id"],
            row["facility_id"],
            str(row["reporting_date"]),
            _format_usd(float(row["total_borrowing_base_usd"])),
            _format_usd(float(row["outstanding_amount_usd"])),
            _format_usd(float(row["availability_usd"])),
            _format_pct(float(row["utilization_pct"])),
            "YES" if row["breach_flag"] else "NO",
        )

    console.print(table)


@app.command("run-covenant-monitoring")
def run_covenants(
    facility_id: str = typer.Option("ALL", help="Facility ID or ALL"),
    reporting_date: str = typer.Option("2025-12-31", help="Reporting date YYYY-MM-DD"),
    save_events: bool = typer.Option(True, help="Save covenant breaches as monitoring events"),
) -> None:
    """Run covenant tests for one facility or all facilities."""
    try:
        if facility_id.upper() == "ALL":
            results = run_all_covenant_monitoring(reporting_date=reporting_date)
        else:
            results = run_covenant_monitoring(
                facility_id=facility_id,
                reporting_date=reporting_date,
            )
    except Exception as exc:
        console.print(f"[red]Covenant monitoring failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title=f"Covenant Monitoring Results: {facility_id}")
    table.add_column("Facility", style="cyan")
    table.add_column("Covenant")
    table.add_column("Threshold", justify="right")
    table.add_column("Actual", justify="right")
    table.add_column("Result", justify="center")
    table.add_column("Severity")
    table.add_column("Recommended Action")

    for result in results:
        result_style = "green" if result.result == "PASS" else "red"

        table.add_row(
            result.facility_id,
            result.covenant_name,
            _format_actual(result.threshold_value, result.threshold_unit),
            _format_actual(result.actual_value, result.threshold_unit),
            f"[{result_style}]{result.result}[/{result_style}]",
            result.breach_severity,
            result.recommended_action,
        )

    console.print(table)

    breach_count = len([result for result in results if result.result == "BREACH"])

    if save_events:
        inserted = save_covenant_breach_events(results, reporting_date=reporting_date)
        console.print(f"[green]Saved monitoring events:[/green] {inserted}")

    if breach_count > 0:
        console.print(f"[red]Breaches detected:[/red] {breach_count}")
        raise typer.Exit(code=2)

    console.print("[green]All covenant tests passed.[/green]")


@app.command("run-credit-scoring")
def run_credit_scoring_command(
    facility_id: str = typer.Option("ALL", help="Facility ID or ALL"),
    analysis_date: str = typer.Option("2025-12-31", help="Analysis date YYYY-MM-DD"),
    save: bool = typer.Option(True, help="Save credit recommendations"),
) -> None:
    """Run transparent fund finance credit scoring and recommendation logic."""
    try:
        if facility_id.upper() == "ALL":
            results = run_all_credit_scoring(analysis_date=analysis_date)
        else:
            results = [
                run_credit_scoring(
                    facility_id=facility_id,
                    analysis_date=analysis_date,
                )
            ]
    except Exception as exc:
        console.print(f"[red]Credit scoring failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title=f"Credit Scoring Results: {facility_id}")
    table.add_column("Facility", style="cyan")
    table.add_column("Fund")
    table.add_column("Type")
    table.add_column("Score", justify="right")
    table.add_column("Rating")
    table.add_column("Recommendation")
    table.add_column("Key Risks")

    for result in results:
        if result.recommendation in {"approve", "approve_with_conditions"}:
            rec_style = "green"
        elif result.recommendation == "monitor":
            rec_style = "yellow"
        else:
            rec_style = "red"

        table.add_row(
            result.facility_id,
            result.fund_name,
            result.facility_type,
            f"{result.total_score:.2f}",
            result.credit_rating,
            f"[{rec_style}]{result.recommendation}[/{rec_style}]",
            result.key_risks,
        )

    console.print(table)

    detail = Table(title="Credit Score Component Breakdown")
    detail.add_column("Facility", style="cyan")
    detail.add_column("Sponsor", justify="right")
    detail.add_column("Investor Base", justify="right")
    detail.add_column("Fund Perf.", justify="right")
    detail.add_column("Collateral", justify="right")
    detail.add_column("Liquidity", justify="right")
    detail.add_column("Covenants", justify="right")
    detail.add_column("Reporting", justify="right")

    for result in results:
        detail.add_row(
            result.facility_id,
            f"{result.sponsor_score:.1f}",
            f"{result.investor_base_score:.1f}",
            f"{result.fund_performance_score:.1f}",
            f"{result.collateral_score:.1f}",
            f"{result.liquidity_score:.1f}",
            f"{result.covenant_score:.1f}",
            f"{result.reporting_score:.1f}",
        )

    console.print(detail)

    if save:
        saved_ids = [save_credit_recommendation(result) for result in results]
        console.print(f"[green]Saved credit recommendations:[/green] {', '.join(saved_ids)}")


@app.command("credit-recommendations")
def credit_recommendations() -> None:
    """Show saved credit recommendations."""
    try:
        recommendations = get_credit_recommendations()
    except Exception as exc:
        console.print(f"[red]Could not load credit recommendations:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title="Saved Credit Recommendations")
    table.add_column("ID", style="cyan")
    table.add_column("Facility")
    table.add_column("Fund")
    table.add_column("Date")
    table.add_column("Score", justify="right")
    table.add_column("Rating")
    table.add_column("Recommendation")
    table.add_column("Risks")

    for _, row in recommendations.iterrows():
        table.add_row(
            row["recommendation_id"],
            row["facility_id"],
            row["fund_name"],
            str(row["analysis_date"]),
            f"{float(row['risk_score']):.2f}",
            row["credit_rating"],
            row["recommendation"],
            row["key_risks"],
        )

    console.print(table)


@app.command("generate-credit-memo")
def generate_credit_memo_command(
    facility_id: str = typer.Option(..., help="Facility ID, for example FAC001"),
    analysis_date: str = typer.Option("2025-12-31", help="Analysis date YYYY-MM-DD"),
) -> None:
    """Generate an institutional-style credit approval memo PDF."""
    try:
        output_path = generate_credit_approval_memo(
            facility_id=facility_id,
            analysis_date=analysis_date,
        )
    except Exception as exc:
        console.print(f"[red]Credit memo generation failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print(f"[green]Generated credit approval memo:[/green] {output_path}")


if __name__ == "__main__":
    app()
