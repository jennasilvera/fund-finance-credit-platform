from fund_finance.analytics.borrowing_base import calculate_subscription_borrowing_base
from fund_finance.analytics.nav_facility import calculate_nav_borrowing_base


def test_fac001_subscription_borrowing_base_passes():
    result = calculate_subscription_borrowing_base(
        facility_id="FAC001",
        reporting_date="2025-12-31",
    )

    assert result.facility_id == "FAC001"
    assert result.facility_type == "subscription"
    assert result.total_borrowing_base_usd > result.outstanding_amount_usd
    assert result.availability_usd > 0
    assert result.breach_flag is False


def test_fac002_subscription_only_borrowing_base_is_deficient():
    result = calculate_subscription_borrowing_base(
        facility_id="FAC002",
        reporting_date="2025-12-31",
    )

    assert result.facility_id == "FAC002"
    assert result.facility_type == "hybrid"
    assert result.total_borrowing_base_usd < result.outstanding_amount_usd
    assert result.breach_flag is True


def test_fac003_nav_borrowing_base_passes():
    result = calculate_nav_borrowing_base(
        facility_id="FAC003",
        reporting_date="2025-12-31",
    )

    assert result.facility_id == "FAC003"
    assert result.facility_type == "nav"
    assert result.eligible_nav_usd > 0
    assert result.total_borrowing_base_usd > result.outstanding_amount_usd
    assert result.ltv_pct < 30
    assert result.breach_flag is False


def test_fac002_hybrid_has_portfolio_concentration_breach():
    result = calculate_nav_borrowing_base(
        facility_id="FAC002",
        reporting_date="2025-12-31",
    )

    assert result.facility_id == "FAC002"
    assert result.facility_type == "hybrid"
    assert result.total_borrowing_base_usd > result.outstanding_amount_usd
    assert result.top_portfolio_company_concentration_pct > 25
    assert result.breach_flag is True
