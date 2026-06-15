from fund_finance.analytics.watchlist import (
    WatchlistInput,
    classify_watchlist_status,
)


def test_escalation_event_forces_critical_watchlist():
    result = classify_watchlist_status(
        WatchlistInput(
            facility_id="FAC002",
            credit_rating="Acceptable",
            recommendation="Escalate",
            open_monitoring_events=1,
            escalation_events=1,
        )
    )

    assert result.watchlist_status == "Critical Watchlist"


def test_weak_credit_rating_creates_watchlist_status():
    result = classify_watchlist_status(
        WatchlistInput(
            facility_id="FAC004",
            credit_rating="Weak",
            recommendation="Monitor",
            open_monitoring_events=0,
            escalation_events=0,
        )
    )

    assert result.watchlist_status == "Watchlist"


def test_multiple_open_events_create_heightened_monitoring():
    result = classify_watchlist_status(
        WatchlistInput(
            facility_id="FAC005",
            credit_rating="Acceptable",
            recommendation="Approve with Conditions",
            open_monitoring_events=2,
            escalation_events=0,
        )
    )

    assert result.watchlist_status == "Heightened Monitoring"


def test_clean_facility_remains_routine_monitoring():
    result = classify_watchlist_status(
        WatchlistInput(
            facility_id="FAC001",
            credit_rating="Strong",
            recommendation="Approve",
            open_monitoring_events=0,
            escalation_events=0,
        )
    )

    assert result.watchlist_status == "Routine Monitoring"
