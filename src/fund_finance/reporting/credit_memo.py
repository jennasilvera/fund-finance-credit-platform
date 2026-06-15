from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from sqlalchemy import text

from fund_finance.analytics.borrowing_base import calculate_subscription_borrowing_base
from fund_finance.analytics.covenant_monitoring import run_covenant_monitoring
from fund_finance.analytics.nav_facility import calculate_nav_borrowing_base
from fund_finance.analytics.risk_scoring import run_credit_scoring
from fund_finance.db.connection import get_engine

OUTPUT_DIR = Path("data/outputs/credit_memos")


def _usd(value: float) -> str:
    return f"${value:,.0f}"


def _pct(value: float) -> str:
    return f"{value:,.2f}%"


def _score(value: float) -> str:
    return f"{value:,.2f}"


def _get_facility_context(facility_id: str) -> dict:
    engine = get_engine()

    query = text(
        """
        SELECT
            ft.facility_id,
            ft.facility_type,
            ft.lender_name,
            ft.commitment_amount_usd,
            ft.outstanding_amount_usd,
            ft.maturity_date,
            ft.pricing_bps,
            ft.unused_fee_bps,
            ft.reporting_frequency,
            f.fund_id,
            f.fund_name,
            f.fund_type,
            f.vintage_year,
            f.fund_size_usd,
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
            fm.strategy_focus,
            fm.years_operating,
            fm.prior_funds_count,
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


def _get_recent_monitoring_events(facility_id: str, analysis_date: str) -> pd.DataFrame:
    engine = get_engine()

    query = text(
        """
        SELECT
            event_date,
            event_type,
            severity,
            description,
            recommended_action,
            escalation_required_flag,
            resolved_flag
        FROM monitoring_events
        WHERE facility_id = :facility_id
          AND event_date <= :analysis_date
        ORDER BY event_date DESC;
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(
            query,
            connection,
            params={"facility_id": facility_id, "analysis_date": analysis_date},
        )


def _build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="MemoTitle",
            parent=styles["Title"],
            fontSize=18,
            leading=22,
            spaceAfter=14,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeader",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            spaceBefore=12,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["BodyText"],
            fontSize=8,
            leading=10,
        )
    )

    styles.add(
        ParagraphStyle(
            name="RightSmall",
            parent=styles["Small"],
            alignment=TA_RIGHT,
        )
    )

    return styles


def _memo_table(data, col_widths=None):
    table = Table(data, colWidths=col_widths, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAEAEA")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F7F7")]),
            ]
        )
    )
    return table


def _add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawString(inch, 0.45 * inch, "Simulated credit memo - portfolio project only")
    canvas.drawRightString(7.5 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def generate_credit_approval_memo(
    facility_id: str,
    analysis_date: str = "2025-12-31",
) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    context = _get_facility_context(facility_id)
    credit = run_credit_scoring(facility_id=facility_id, analysis_date=analysis_date)
    covenants = run_covenant_monitoring(facility_id=facility_id, reporting_date=analysis_date)
    events = _get_recent_monitoring_events(facility_id=facility_id, analysis_date=analysis_date)

    subscription_result = None
    nav_result = None

    if context["facility_type"] in {"subscription", "hybrid"}:
        subscription_result = calculate_subscription_borrowing_base(
            facility_id=facility_id,
            reporting_date=analysis_date,
        )

    if context["facility_type"] in {"nav", "hybrid"}:
        nav_result = calculate_nav_borrowing_base(
            facility_id=facility_id,
            reporting_date=analysis_date,
        )

    output_path = OUTPUT_DIR / f"credit_approval_memo_{facility_id}_{analysis_date}.pdf"

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=LETTER,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )

    styles = _build_styles()
    story = []

    story.append(Paragraph("Credit Approval Memo", styles["MemoTitle"]))
    story.append(
        Paragraph(
            f"<b>Facility:</b> {facility_id} &nbsp;&nbsp; "
            f"<b>Fund:</b> {context['fund_name']} &nbsp;&nbsp; "
            f"<b>Analysis Date:</b> {analysis_date}",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Executive Summary", styles["SectionHeader"]))
    story.append(
        Paragraph(
            f"The proposed credit view for {context['fund_name']} is "
            f"<b>{credit.credit_rating}</b> with a recommendation to "
            f"<b>{credit.recommendation.replace('_', ' ').title()}</b>. "
            f"The credit score is <b>{credit.total_score:.2f}</b>. "
            f"Key strengths include: {credit.key_strengths}. "
            f"Key risks include: {credit.key_risks}.",
            styles["BodyText"],
        )
    )

    summary_data = [
        ["Metric", "Value"],
        ["Recommendation", credit.recommendation.replace("_", " ").title()],
        ["Credit Rating", credit.credit_rating],
        ["Risk Score", _score(credit.total_score)],
        ["Required Mitigants", credit.required_mitigants],
    ]
    story.append(Spacer(1, 8))
    story.append(_memo_table(summary_data, [2.1 * inch, 4.8 * inch]))

    story.append(Paragraph("2. Transaction Overview", styles["SectionHeader"]))
    transaction_data = [
        ["Field", "Value"],
        ["Facility Type", str(context["facility_type"]).title()],
        ["Lender", context["lender_name"]],
        ["Facility Commitment", _usd(float(context["commitment_amount_usd"]))],
        ["Outstanding Amount", _usd(float(context["outstanding_amount_usd"]))],
        ["Maturity Date", str(context["maturity_date"])],
        ["Pricing", f"{float(context['pricing_bps']):.0f} bps"],
        ["Unused Fee", f"{float(context['unused_fee_bps']):.0f} bps"],
        ["Reporting Frequency", str(context["reporting_frequency"]).title()],
    ]
    story.append(_memo_table(transaction_data, [2.1 * inch, 4.8 * inch]))

    story.append(Paragraph("3. Fund and Sponsor Overview", styles["SectionHeader"]))
    fund_data = [
        ["Field", "Value"],
        ["Fund Manager", context["manager_name"]],
        ["Sponsor Risk Rating", context["sponsor_risk_rating"]],
        ["Strategy Focus", context["strategy_focus"]],
        ["Years Operating", str(context["years_operating"])],
        ["Prior Funds", str(context["prior_funds_count"])],
        ["Fund Type", context["fund_type"]],
        ["Vintage Year", str(context["vintage_year"])],
        ["Fund Status", str(context["fund_status"]).title()],
        ["Committed Capital", _usd(float(context["committed_capital_usd"]))],
        ["Called Capital", _usd(float(context["called_capital_usd"]))],
        ["Uncalled Capital", _usd(float(context["uncalled_capital_usd"]))],
        ["NAV", _usd(float(context["nav_usd"]))],
        ["DPI", f"{float(context['dpi']):.2f}x"],
        ["TVPI", f"{float(context['tvpi']):.2f}x"],
        ["Net IRR", _pct(float(context["net_irr"]))],
    ]
    story.append(_memo_table(fund_data, [2.1 * inch, 4.8 * inch]))

    story.append(PageBreak())
    story.append(Paragraph("4. Borrowing Base and Collateral Analysis", styles["SectionHeader"]))

    if subscription_result is not None:
        sub_data = [
            ["Subscription Borrowing Base Metric", "Value"],
            [
                "Eligible Uncalled Commitments",
                _usd(subscription_result.eligible_uncalled_commitments_usd),
            ],
            ["Subscription Borrowing Base", _usd(subscription_result.total_borrowing_base_usd)],
            ["Outstanding Amount", _usd(subscription_result.outstanding_amount_usd)],
            ["Availability", _usd(subscription_result.availability_usd)],
            ["Utilization", _pct(subscription_result.utilization_pct)],
            [
                "Top Investor Concentration",
                _pct(subscription_result.top_investor_concentration_pct),
            ],
            [
                "Top 5 Investor Concentration",
                _pct(subscription_result.top5_investor_concentration_pct),
            ],
            ["Breach Flag", "Yes" if subscription_result.breach_flag else "No"],
        ]
        story.append(_memo_table(sub_data, [3.0 * inch, 3.9 * inch]))
        story.append(Spacer(1, 8))

    if nav_result is not None:
        nav_data = [
            ["NAV / Hybrid Borrowing Base Metric", "Value"],
            ["Latest NAV Date", nav_result.latest_nav_date],
            ["Gross NAV", _usd(nav_result.gross_nav_usd)],
            ["Eligible NAV", _usd(nav_result.eligible_nav_usd)],
            ["NAV Advance Rate", _pct(nav_result.nav_advance_rate_pct)],
            ["NAV Borrowing Base", _usd(nav_result.nav_borrowing_base_usd)],
            ["Subscription Borrowing Base", _usd(nav_result.subscription_borrowing_base_usd)],
            ["Total Borrowing Base", _usd(nav_result.total_borrowing_base_usd)],
            ["Outstanding Amount", _usd(nav_result.outstanding_amount_usd)],
            ["Availability", _usd(nav_result.availability_usd)],
            ["LTV", _pct(nav_result.ltv_pct)],
            ["Top Company Concentration", _pct(nav_result.top_portfolio_company_concentration_pct)],
            ["Top Sector Concentration", _pct(nav_result.top_sector_concentration_pct)],
            ["Breach Flag", "Yes" if nav_result.breach_flag else "No"],
        ]
        story.append(_memo_table(nav_data, [3.0 * inch, 3.9 * inch]))

    story.append(Paragraph("5. Credit Scorecard", styles["SectionHeader"]))
    score_data = [
        ["Component", "Score", "Weight"],
        ["Sponsor Quality", _score(credit.sponsor_score), "20%"],
        ["Investor Base Quality", _score(credit.investor_base_score), "20%"],
        ["Fund Performance", _score(credit.fund_performance_score), "15%"],
        ["Collateral Quality", _score(credit.collateral_score), "15%"],
        ["Liquidity", _score(credit.liquidity_score), "10%"],
        ["Covenant Headroom", _score(credit.covenant_score), "10%"],
        ["Reporting / Operational Discipline", _score(credit.reporting_score), "10%"],
        ["Total Score", _score(credit.total_score), "100%"],
    ]
    story.append(_memo_table(score_data, [3.2 * inch, 1.7 * inch, 1.3 * inch]))

    story.append(Paragraph("6. Covenant Monitoring", styles["SectionHeader"]))
    covenant_data = [["Covenant", "Threshold", "Actual", "Result", "Severity"]]

    for covenant in covenants:
        if covenant.threshold_unit == "percent":
            threshold = _pct(covenant.threshold_value)
            actual = _pct(covenant.actual_value)
        elif covenant.threshold_unit == "x":
            threshold = f"{covenant.threshold_value:.2f}x"
            actual = f"{covenant.actual_value:.2f}x"
        else:
            threshold = f"{covenant.threshold_value:.2f}"
            actual = f"{covenant.actual_value:.2f}"

        covenant_data.append(
            [
                covenant.covenant_name,
                threshold,
                actual,
                covenant.result,
                covenant.breach_severity,
            ]
        )

    story.append(
        _memo_table(
            covenant_data,
            [2.8 * inch, 1.0 * inch, 1.0 * inch, 0.9 * inch, 1.0 * inch],
        )
    )

    story.append(Paragraph("7. Monitoring Events", styles["SectionHeader"]))

    if events.empty:
        story.append(
            Paragraph(
                "No monitoring events identified as of the analysis date.",
                styles["BodyText"],
            )
        )
    else:
        event_data = [["Date", "Type", "Severity", "Description", "Escalation"]]

        for _, row in events.iterrows():
            event_data.append(
                [
                    str(row["event_date"]),
                    row["event_type"],
                    row["severity"],
                    Paragraph(str(row["description"]), styles["Small"]),
                    "Yes" if row["escalation_required_flag"] else "No",
                ]
            )

        story.append(
            _memo_table(
                event_data,
                [0.8 * inch, 1.1 * inch, 0.8 * inch, 3.4 * inch, 0.8 * inch],
            )
        )

    story.append(Paragraph("8. Final Credit Recommendation", styles["SectionHeader"]))
    story.append(
        Paragraph(
            f"<b>Recommendation:</b> {credit.recommendation.replace('_', ' ').title()}<br/>"
            f"<b>Required Mitigants:</b> {credit.required_mitigants}<br/>"
            f"<b>Analyst View:</b> The facility should be reviewed in light of the "
            f"identified collateral, covenant, liquidity, and monitoring factors. "
            f"This memo is generated from simulated data for portfolio demonstration purposes.",
            styles["BodyText"],
        )
    )

    doc.build(story, onFirstPage=_add_footer, onLaterPages=_add_footer)

    return output_path
