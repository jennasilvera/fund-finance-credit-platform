from dataclasses import dataclass


@dataclass(frozen=True)
class WatchlistInput:
    facility_id: str
    credit_rating: str | None
    recommendation: str | None
    open_monitoring_events: int
    escalation_events: int


@dataclass(frozen=True)
class WatchlistResult:
    facility_id: str
    watchlist_status: str
    rationale: str


def classify_watchlist_status(item: WatchlistInput) -> WatchlistResult:
    credit_rating = (item.credit_rating or "").lower()
    recommendation = (item.recommendation or "").lower()

    if item.escalation_events > 0 or "escalate" in recommendation:
        return WatchlistResult(
            facility_id=item.facility_id,
            watchlist_status="Critical Watchlist",
            rationale="Escalation event or escalation recommendation is present.",
        )

    if "problem" in credit_rating or "weak" in credit_rating or "decline" in recommendation:
        return WatchlistResult(
            facility_id=item.facility_id,
            watchlist_status="Watchlist",
            rationale="Credit rating or recommendation indicates elevated credit risk.",
        )

    if item.open_monitoring_events >= 2 or "monitor" in recommendation:
        return WatchlistResult(
            facility_id=item.facility_id,
            watchlist_status="Heightened Monitoring",
            rationale="Open monitoring events or monitor recommendation require closer review.",
        )

    return WatchlistResult(
        facility_id=item.facility_id,
        watchlist_status="Routine Monitoring",
        rationale="No material open escalation or watchlist trigger detected.",
    )
