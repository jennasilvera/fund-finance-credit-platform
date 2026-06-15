import pytest

from fund_finance.analytics.stress_testing import (
    FacilityStressInput,
    run_nav_ltv_stress,
)


def test_nav_ltv_stress_detects_no_breach_when_headroom_is_strong():
    facility = FacilityStressInput(
        facility_id="FAC003",
        facility_type="nav",
        eligible_nav_usd=1_000_000_000,
        outstanding_amount_usd=100_000_000,
        max_ltv_pct=30.0,
    )

    results = run_nav_ltv_stress(facility, nav_shock_pcts=(-0.10, -0.20))

    assert len(results) == 2
    assert results[0].stressed_ltv_pct == pytest.approx(11.1111, rel=0.001)
    assert results[1].stressed_ltv_pct == pytest.approx(12.5)
    assert all(not result.breach_flag for result in results)


def test_nav_ltv_stress_detects_breach_under_downside_case():
    facility = FacilityStressInput(
        facility_id="FAC002",
        facility_type="hybrid",
        eligible_nav_usd=640_000_000,
        outstanding_amount_usd=180_000_000,
        max_ltv_pct=30.0,
    )

    results = run_nav_ltv_stress(facility, nav_shock_pcts=(-0.10, -0.20))

    assert results[0].breach_flag is True
    assert results[0].stressed_ltv_pct > 30.0
    assert results[0].ltv_headroom_pct < 0
    assert results[1].breach_flag is True


def test_nav_ltv_stress_rejects_invalid_nav():
    facility = FacilityStressInput(
        facility_id="FAC_BAD",
        facility_type="nav",
        eligible_nav_usd=0,
        outstanding_amount_usd=100_000_000,
        max_ltv_pct=30.0,
    )

    with pytest.raises(ValueError, match="eligible_nav_usd must be positive"):
        run_nav_ltv_stress(facility)
