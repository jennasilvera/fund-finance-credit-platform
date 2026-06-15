from dataclasses import dataclass


@dataclass(frozen=True)
class FacilityStressInput:
    facility_id: str
    facility_type: str
    eligible_nav_usd: float
    outstanding_amount_usd: float
    max_ltv_pct: float


@dataclass(frozen=True)
class StressScenarioResult:
    facility_id: str
    scenario_name: str
    nav_shock_pct: float
    stressed_eligible_nav_usd: float
    outstanding_amount_usd: float
    stressed_ltv_pct: float
    max_ltv_pct: float
    ltv_headroom_pct: float
    breach_flag: bool


def run_nav_ltv_stress(
    facility: FacilityStressInput,
    nav_shock_pcts: tuple[float, ...] = (-0.10, -0.20, -0.30),
) -> list[StressScenarioResult]:
    if facility.eligible_nav_usd <= 0:
        raise ValueError("eligible_nav_usd must be positive")

    if facility.outstanding_amount_usd < 0:
        raise ValueError("outstanding_amount_usd cannot be negative")

    if facility.max_ltv_pct <= 0:
        raise ValueError("max_ltv_pct must be positive")

    results = []

    for nav_shock_pct in nav_shock_pcts:
        stressed_eligible_nav = facility.eligible_nav_usd * (1 + nav_shock_pct)

        if stressed_eligible_nav <= 0:
            stressed_ltv_pct = float("inf")
        else:
            stressed_ltv_pct = (
                facility.outstanding_amount_usd / stressed_eligible_nav
            ) * 100

        ltv_headroom_pct = facility.max_ltv_pct - stressed_ltv_pct

        results.append(
            StressScenarioResult(
                facility_id=facility.facility_id,
                scenario_name=f"{abs(nav_shock_pct):.0%} NAV decline",
                nav_shock_pct=nav_shock_pct,
                stressed_eligible_nav_usd=stressed_eligible_nav,
                outstanding_amount_usd=facility.outstanding_amount_usd,
                stressed_ltv_pct=stressed_ltv_pct,
                max_ltv_pct=facility.max_ltv_pct,
                ltv_headroom_pct=ltv_headroom_pct,
                breach_flag=stressed_ltv_pct > facility.max_ltv_pct,
            )
        )

    return results
