from pathlib import Path

import pandas as pd

RAW_DATA_DIR = Path("data/raw")


def write_csv(filename: str, records: list[dict]) -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DATA_DIR / filename
    pd.DataFrame(records).to_csv(path, index=False)
    print(f"Wrote {path}")


def generate_fund_managers() -> list[dict]:
    return [
        {
            "manager_id": "MGR001",
            "manager_name": "NorthBridge Capital Partners",
            "headquarters_country": "US",
            "total_aum_usd": 18500000000,
            "strategy_focus": "Middle-market buyout",
            "years_operating": 19,
            "prior_funds_count": 4,
            "realized_track_record_flag": True,
            "sponsor_risk_rating": "Strong",
        },
        {
            "manager_id": "MGR002",
            "manager_name": "Meridian Ventures",
            "headquarters_country": "US",
            "total_aum_usd": 4200000000,
            "strategy_focus": "Growth equity and venture capital",
            "years_operating": 11,
            "prior_funds_count": 3,
            "realized_track_record_flag": True,
            "sponsor_risk_rating": "Acceptable",
        },
        {
            "manager_id": "MGR003",
            "manager_name": "HarborStone Partners",
            "headquarters_country": "UK",
            "total_aum_usd": 31000000000,
            "strategy_focus": "Large-cap buyout",
            "years_operating": 24,
            "prior_funds_count": 6,
            "realized_track_record_flag": True,
            "sponsor_risk_rating": "Strong",
        },
    ]


def generate_funds() -> list[dict]:
    return [
        {
            "fund_id": "FND001",
            "manager_id": "MGR001",
            "fund_name": "NorthBridge Capital Partners Fund IV",
            "fund_type": "PE",
            "vintage_year": 2022,
            "fund_size_usd": 2500000000,
            "committed_capital_usd": 2400000000,
            "called_capital_usd": 960000000,
            "uncalled_capital_usd": 1440000000,
            "nav_usd": 1180000000,
            "dpi": 0.12,
            "tvpi": 1.32,
            "net_irr": 14.8,
            "investment_period_end": "2027-12-31",
            "fund_term_end": "2032-12-31",
            "base_currency": "USD",
            "fund_status": "investing",
        },
        {
            "fund_id": "FND002",
            "manager_id": "MGR002",
            "fund_name": "Meridian Ventures Growth Fund III",
            "fund_type": "VC",
            "vintage_year": 2021,
            "fund_size_usd": 850000000,
            "committed_capital_usd": 820000000,
            "called_capital_usd": 590000000,
            "uncalled_capital_usd": 230000000,
            "nav_usd": 710000000,
            "dpi": 0.05,
            "tvpi": 1.21,
            "net_irr": 11.4,
            "investment_period_end": "2026-06-30",
            "fund_term_end": "2031-06-30",
            "base_currency": "USD",
            "fund_status": "investing",
        },
        {
            "fund_id": "FND003",
            "manager_id": "MGR003",
            "fund_name": "HarborStone Buyout Fund VI",
            "fund_type": "PE",
            "vintage_year": 2019,
            "fund_size_usd": 4100000000,
            "committed_capital_usd": 4050000000,
            "called_capital_usd": 3300000000,
            "uncalled_capital_usd": 750000000,
            "nav_usd": 4650000000,
            "dpi": 0.58,
            "tvpi": 1.72,
            "net_irr": 18.9,
            "investment_period_end": "2024-12-31",
            "fund_term_end": "2029-12-31",
            "base_currency": "USD",
            "fund_status": "harvesting",
        },
    ]


def generate_investors() -> list[dict]:
    return [
        {
            "investor_id": "INV001",
            "investor_name": "North River State Retirement System",
            "investor_type": "pension",
            "country": "US",
            "external_rating": "AA",
            "internal_rating": "A+",
            "included_in_borrowing_base_flag": True,
            "investor_category": "rated_included",
            "affiliate_group": "NRRS",
            "liquidity_watch_flag": False,
            "side_letter_restriction_flag": False,
        },
        {
            "investor_id": "INV002",
            "investor_name": "Atlantic University Endowment",
            "investor_type": "endowment",
            "country": "US",
            "external_rating": "AA-",
            "internal_rating": "A",
            "included_in_borrowing_base_flag": True,
            "investor_category": "rated_included",
            "affiliate_group": "AUE",
            "liquidity_watch_flag": False,
            "side_letter_restriction_flag": False,
        },
        {
            "investor_id": "INV003",
            "investor_name": "BluePeak Insurance General Account",
            "investor_type": "insurer",
            "country": "US",
            "external_rating": "A",
            "internal_rating": "A-",
            "included_in_borrowing_base_flag": True,
            "investor_category": "rated_included",
            "affiliate_group": "BPIG",
            "liquidity_watch_flag": False,
            "side_letter_restriction_flag": False,
        },
        {
            "investor_id": "INV004",
            "investor_name": "Cedar Grove Family Office",
            "investor_type": "family_office",
            "country": "US",
            "external_rating": "NR",
            "internal_rating": "BBB",
            "included_in_borrowing_base_flag": True,
            "investor_category": "designated",
            "affiliate_group": "CGFO",
            "liquidity_watch_flag": False,
            "side_letter_restriction_flag": True,
        },
        {
            "investor_id": "INV005",
            "investor_name": "Westport Fund of Funds II",
            "investor_type": "fund_of_funds",
            "country": "UK",
            "external_rating": "NR",
            "internal_rating": "BBB+",
            "included_in_borrowing_base_flag": True,
            "investor_category": "non_rated_included",
            "affiliate_group": "WFF",
            "liquidity_watch_flag": False,
            "side_letter_restriction_flag": False,
        },
        {
            "investor_id": "INV006",
            "investor_name": "Gulf Horizon Sovereign Investment Authority",
            "investor_type": "sovereign_wealth",
            "country": "UAE",
            "external_rating": "AA",
            "internal_rating": "A+",
            "included_in_borrowing_base_flag": True,
            "investor_category": "rated_included",
            "affiliate_group": "GHSIA",
            "liquidity_watch_flag": False,
            "side_letter_restriction_flag": False,
        },
        {
            "investor_id": "INV007",
            "investor_name": "Lakeview Public Employees Pension Plan",
            "investor_type": "pension",
            "country": "Canada",
            "external_rating": "AA-",
            "internal_rating": "A",
            "included_in_borrowing_base_flag": True,
            "investor_category": "rated_included",
            "affiliate_group": "LPEP",
            "liquidity_watch_flag": False,
            "side_letter_restriction_flag": False,
        },
        {
            "investor_id": "INV008",
            "investor_name": "Sierra Foundation",
            "investor_type": "foundation",
            "country": "US",
            "external_rating": "NR",
            "internal_rating": "BBB",
            "included_in_borrowing_base_flag": True,
            "investor_category": "non_rated_included",
            "affiliate_group": "SF",
            "liquidity_watch_flag": False,
            "side_letter_restriction_flag": False,
        },
        {
            "investor_id": "INV009",
            "investor_name": "Orchard Wealth Partners",
            "investor_type": "family_office",
            "country": "US",
            "external_rating": "NR",
            "internal_rating": "BB+",
            "included_in_borrowing_base_flag": False,
            "investor_category": "excluded",
            "affiliate_group": "OWP",
            "liquidity_watch_flag": True,
            "side_letter_restriction_flag": True,
        },
        {
            "investor_id": "INV010",
            "investor_name": "Crescent Asset Management",
            "investor_type": "asset_manager",
            "country": "France",
            "external_rating": "A",
            "internal_rating": "A-",
            "included_in_borrowing_base_flag": True,
            "investor_category": "rated_included",
            "affiliate_group": "CAM",
            "liquidity_watch_flag": False,
            "side_letter_restriction_flag": False,
        },
        {
            "investor_id": "INV011",
            "investor_name": "Evergreen Healthcare Endowment",
            "investor_type": "endowment",
            "country": "US",
            "external_rating": "A",
            "internal_rating": "A-",
            "included_in_borrowing_base_flag": True,
            "investor_category": "rated_included",
            "affiliate_group": "EHE",
            "liquidity_watch_flag": False,
            "side_letter_restriction_flag": False,
        },
        {
            "investor_id": "INV012",
            "investor_name": "Redwood Fund Investors",
            "investor_type": "fund_of_funds",
            "country": "US",
            "external_rating": "NR",
            "internal_rating": "BBB-",
            "included_in_borrowing_base_flag": True,
            "investor_category": "non_rated_included",
            "affiliate_group": "RFI",
            "liquidity_watch_flag": False,
            "side_letter_restriction_flag": False,
        },
    ]


def generate_commitments() -> list[dict]:
    rows = []
    commitment_id = 1

    fund_allocations = {
        "FND001": {
            "called_pct": 0.40,
            "commitments": {
                "INV001": 420000000,
                "INV002": 300000000,
                "INV003": 280000000,
                "INV004": 160000000,
                "INV005": 240000000,
                "INV006": 390000000,
                "INV007": 310000000,
                "INV010": 300000000,
            },
        },
        "FND002": {
            "called_pct": 0.7195,
            "commitments": {
                "INV001": 120000000,
                "INV002": 90000000,
                "INV004": 75000000,
                "INV005": 85000000,
                "INV006": 135000000,
                "INV008": 65000000,
                "INV009": 50000000,
                "INV011": 110000000,
                "INV012": 90000000,
            },
        },
        "FND003": {
            "called_pct": 0.8148,
            "commitments": {
                "INV001": 675000000,
                "INV002": 440000000,
                "INV003": 525000000,
                "INV006": 700000000,
                "INV007": 490000000,
                "INV010": 580000000,
                "INV011": 390000000,
                "INV012": 250000000,
            },
        },
    }

    for fund_id, data in fund_allocations.items():
        for investor_id, commitment in data["commitments"].items():
            called = round(commitment * data["called_pct"], 2)
            uncalled = round(commitment - called, 2)
            default_status = "current"
            exclusion_reason = ""

            if investor_id == "INV009":
                default_status = "late"
                exclusion_reason = "Liquidity watch and side-letter restriction"

            rows.append(
                {
                    "commitment_id": f"CMT{commitment_id:03d}",
                    "fund_id": fund_id,
                    "investor_id": investor_id,
                    "commitment_amount_usd": commitment,
                    "called_amount_usd": called,
                    "uncalled_amount_usd": uncalled,
                    "commitment_date": "2021-06-30",
                    "default_status": default_status,
                    "exclusion_reason": exclusion_reason,
                }
            )
            commitment_id += 1

    return rows


def generate_capital_calls() -> list[dict]:
    rows = []
    call_id = 1

    call_templates = [
        ("2025-01-15", "2025-01-30", "investment"),
        ("2025-04-15", "2025-04-30", "fees"),
        ("2025-07-15", "2025-07-30", "follow_on"),
    ]

    commitments = generate_commitments()

    for commitment in commitments:
        for call_date, due_date, purpose in call_templates:
            call_amount = round(commitment["commitment_amount_usd"] * 0.015, 2)
            funded_amount = call_amount
            days_late = 0
            status = "funded"

            if commitment["investor_id"] == "INV009" and purpose == "follow_on":
                funded_amount = round(call_amount * 0.65, 2)
                days_late = 18
                status = "partially_funded"

            rows.append(
                {
                    "capital_call_id": f"CALL{call_id:03d}",
                    "fund_id": commitment["fund_id"],
                    "investor_id": commitment["investor_id"],
                    "call_date": call_date,
                    "due_date": due_date,
                    "amount_called_usd": call_amount,
                    "amount_funded_usd": funded_amount,
                    "days_late": days_late,
                    "call_purpose": purpose,
                    "status": status,
                }
            )
            call_id += 1

    return rows


def generate_nav_history() -> list[dict]:
    rows = []
    nav_id = 1

    fund_nav_series = {
        "FND001": [980, 1025, 1080, 1125, 1180, 1215, 1195, 1230],
        "FND002": [760, 735, 720, 710, 675, 650, 625, 640],
        "FND003": [3900, 4050, 4260, 4475, 4650, 4720, 4810, 4930],
    }

    dates = [
        "2024-03-31",
        "2024-06-30",
        "2024-09-30",
        "2024-12-31",
        "2025-03-31",
        "2025-06-30",
        "2025-09-30",
        "2025-12-31",
    ]

    for fund_id, nav_values_mm in fund_nav_series.items():
        previous_nav = None
        for reporting_date, nav_mm in zip(dates, nav_values_mm, strict=True):
            net_nav = nav_mm * 1_000_000
            gross_nav = round(net_nav * 1.025, 2)

            if previous_nav is None:
                qoq_change = 0.0
            else:
                qoq_change = round(((net_nav - previous_nav) / previous_nav) * 100, 4)

            rows.append(
                {
                    "nav_id": f"NAV{nav_id:03d}",
                    "fund_id": fund_id,
                    "reporting_date": reporting_date,
                    "gross_nav_usd": gross_nav,
                    "net_nav_usd": net_nav,
                    "quarter_over_quarter_nav_change_pct": qoq_change,
                    "valuation_policy": "ASC 820 fair value framework",
                    "valuation_source": "Manager quarterly report",
                    "audit_status": "unaudited" if reporting_date != "2024-12-31" else "audited",
                }
            )

            previous_nav = net_nav
            nav_id += 1

    return rows


def generate_portfolio_companies() -> list[dict]:
    rows = []
    company_id = 1

    portfolio_map = {
        "FND001": [
            ("Atlas Components", "Industrials", 165),
            ("BrightPath Logistics", "Transportation", 145),
            ("Cobalt Software", "Software", 130),
            ("Keystone Packaging", "Consumer", 115),
            ("Ridge Medical Devices", "Healthcare", 175),
            ("Summit Data Systems", "Technology", 105),
            ("Pioneer Controls", "Industrials", 95),
            ("Northstar Clinics", "Healthcare", 125),
        ],
        "FND002": [
            ("NovaAI Systems", "Software", 180),
            ("Helio Battery Labs", "Climate Tech", 120),
            ("PulsePay Networks", "Fintech", 95),
            ("GeneWorks Bio", "Healthcare", 85),
            ("Orbit Robotics", "Robotics", 70),
            ("CloudForge Security", "Cybersecurity", 65),
            ("Vector Commerce", "Software", 55),
            ("Lumina Chips", "Semiconductors", 40),
        ],
        "FND003": [
            ("Crown Industrial Services", "Industrials", 720),
            ("Mariner Health Group", "Healthcare", 640),
            ("Apex Payment Systems", "Fintech", 580),
            ("Stonegate Foods", "Consumer", 420),
            ("Helix Infrastructure", "Infrastructure", 690),
            ("Bayside Software", "Software", 530),
            ("Redwood Manufacturing", "Industrials", 475),
            ("Clearwater Labs", "Healthcare", 380),
        ],
    }

    for fund_id, companies in portfolio_map.items():
        for name, sector, fair_value_mm in companies:
            is_vc = fund_id == "FND002"
            cost_basis = round(fair_value_mm * 0.72 * 1_000_000, 2)
            fair_value = fair_value_mm * 1_000_000

            rows.append(
                {
                    "company_id": f"PC{company_id:03d}",
                    "fund_id": fund_id,
                    "company_name": name,
                    "sector": sector,
                    "geography": "US",
                    "investment_date": "2022-03-31" if fund_id != "FND003" else "2020-03-31",
                    "cost_basis_usd": cost_basis,
                    "current_fair_value_usd": fair_value,
                    "ownership_pct": 35.0 if fund_id != "FND002" else 12.5,
                    "revenue_growth_pct": 12.0 if not is_vc else 38.0,
                    "ebitda_margin_pct": 18.0 if not is_vc else -12.0,
                    "cash_runway_months": 24 if not is_vc else 10,
                    "last_round_date": "2025-06-30" if is_vc else "",
                    "last_round_type": "Series C" if is_vc else "",
                    "valuation_mark": (
                        "down"
                        if name in {"Helio Battery Labs", "Lumina Chips"}
                        else "up"
                    ),
                    "non_performing_flag": name in {"Lumina Chips"},
                }
            )
            company_id += 1

    return rows


def generate_facility_terms() -> list[dict]:
    return [
        {
            "facility_id": "FAC001",
            "fund_id": "FND001",
            "facility_type": "subscription",
            "lender_name": "Simulated Bank FSG",
            "commitment_amount_usd": 600000000,
            "outstanding_amount_usd": 275000000,
            "maturity_date": "2027-06-30",
            "pricing_bps": 225,
            "unused_fee_bps": 40,
            "advance_rate_rated_pct": 90,
            "advance_rate_non_rated_pct": 80,
            "advance_rate_designated_pct": 60,
            "nav_advance_rate_pct": 0,
            "max_ltv_pct": 0,
            "min_liquidity_usd": 25000000,
            "max_top_investor_concentration_pct": 25,
            "max_top5_investor_concentration_pct": 65,
            "max_top_portfolio_company_pct": 0,
            "max_sector_concentration_pct": 0,
            "reporting_frequency": "quarterly",
        },
        {
            "facility_id": "FAC002",
            "fund_id": "FND002",
            "facility_type": "hybrid",
            "lender_name": "Simulated Bank FSG",
            "commitment_amount_usd": 250000000,
            "outstanding_amount_usd": 180000000,
            "maturity_date": "2026-12-31",
            "pricing_bps": 325,
            "unused_fee_bps": 65,
            "advance_rate_rated_pct": 85,
            "advance_rate_non_rated_pct": 70,
            "advance_rate_designated_pct": 50,
            "nav_advance_rate_pct": 25,
            "max_ltv_pct": 30,
            "min_liquidity_usd": 15000000,
            "max_top_investor_concentration_pct": 20,
            "max_top5_investor_concentration_pct": 60,
            "max_top_portfolio_company_pct": 25,
            "max_sector_concentration_pct": 40,
            "reporting_frequency": "quarterly",
        },
        {
            "facility_id": "FAC003",
            "fund_id": "FND003",
            "facility_type": "nav",
            "lender_name": "Simulated Bank FSG",
            "commitment_amount_usd": 500000000,
            "outstanding_amount_usd": 320000000,
            "maturity_date": "2028-03-31",
            "pricing_bps": 375,
            "unused_fee_bps": 75,
            "advance_rate_rated_pct": 0,
            "advance_rate_non_rated_pct": 0,
            "advance_rate_designated_pct": 0,
            "nav_advance_rate_pct": 22.5,
            "max_ltv_pct": 30,
            "min_liquidity_usd": 30000000,
            "max_top_investor_concentration_pct": 0,
            "max_top5_investor_concentration_pct": 0,
            "max_top_portfolio_company_pct": 20,
            "max_sector_concentration_pct": 35,
            "reporting_frequency": "quarterly",
        },
    ]


def generate_covenant_terms() -> list[dict]:
    return [
        {
            "covenant_id": "COV001",
            "facility_id": "FAC001",
            "covenant_name": "Maximum Top Investor Concentration",
            "covenant_type": "concentration",
            "threshold_value": 25,
            "threshold_unit": "percent",
            "test_frequency": "quarterly",
            "breach_severity": "medium",
        },
        {
            "covenant_id": "COV002",
            "facility_id": "FAC001",
            "covenant_name": "Minimum Borrowing Base Coverage",
            "covenant_type": "financial",
            "threshold_value": 1.10,
            "threshold_unit": "x",
            "test_frequency": "quarterly",
            "breach_severity": "high",
        },
        {
            "covenant_id": "COV003",
            "facility_id": "FAC002",
            "covenant_name": "Maximum LTV",
            "covenant_type": "financial",
            "threshold_value": 30,
            "threshold_unit": "percent",
            "test_frequency": "quarterly",
            "breach_severity": "high",
        },
        {
            "covenant_id": "COV004",
            "facility_id": "FAC002",
            "covenant_name": "Maximum Top Portfolio Company Concentration",
            "covenant_type": "concentration",
            "threshold_value": 25,
            "threshold_unit": "percent",
            "test_frequency": "quarterly",
            "breach_severity": "medium",
        },
        {
            "covenant_id": "COV005",
            "facility_id": "FAC003",
            "covenant_name": "Maximum LTV",
            "covenant_type": "financial",
            "threshold_value": 30,
            "threshold_unit": "percent",
            "test_frequency": "quarterly",
            "breach_severity": "high",
        },
        {
            "covenant_id": "COV006",
            "facility_id": "FAC003",
            "covenant_name": "Maximum Sector Concentration",
            "covenant_type": "concentration",
            "threshold_value": 35,
            "threshold_unit": "percent",
            "test_frequency": "quarterly",
            "breach_severity": "medium",
        },
    ]


def generate_monitoring_events() -> list[dict]:
    return [
        {
            "event_id": "EVT001",
            "fund_id": "FND002",
            "facility_id": "FAC002",
            "event_date": "2025-09-30",
            "event_type": "NAV decline",
            "severity": "high",
            "description": (
                "Meridian Ventures reported consecutive quarterly NAV declines driven by "
                "lower marks in climate tech and semiconductor holdings."
            ),
            "recommended_action": (
                "Request updated valuation package and test hybrid borrowing base availability."
            ),
            "escalation_required_flag": True,
            "resolved_flag": False,
        },
        {
            "event_id": "EVT002",
            "fund_id": "FND002",
            "facility_id": "FAC002",
            "event_date": "2025-07-30",
            "event_type": "Late capital call funding",
            "severity": "medium",
            "description": (
                "One excluded investor partially funded a follow-on capital call "
                "after the due date."
            ),
            "recommended_action": (
                "Confirm investor remains excluded from borrowing base and monitor future "
                "funding behavior."
            ),
            "escalation_required_flag": False,
            "resolved_flag": False,
        },
        {
            "event_id": "EVT003",
            "fund_id": "FND003",
            "facility_id": "FAC003",
            "event_date": "2025-12-31",
            "event_type": "Portfolio concentration watch",
            "severity": "medium",
            "description": (
                "Top portfolio company exposure remains elevated but below hard covenant threshold."
            ),
            "recommended_action": "Continue quarterly monitoring and request exit pipeline update.",
            "escalation_required_flag": False,
            "resolved_flag": False,
        },
    ]


def generate_all() -> None:
    write_csv("fund_managers.csv", generate_fund_managers())
    write_csv("funds.csv", generate_funds())
    write_csv("investors.csv", generate_investors())
    write_csv("capital_commitments.csv", generate_commitments())
    write_csv("capital_calls.csv", generate_capital_calls())
    write_csv("nav_history.csv", generate_nav_history())
    write_csv("portfolio_companies.csv", generate_portfolio_companies())
    write_csv("facility_terms.csv", generate_facility_terms())
    write_csv("covenant_terms.csv", generate_covenant_terms())
    write_csv("monitoring_events.csv", generate_monitoring_events())


if __name__ == "__main__":
    generate_all()
