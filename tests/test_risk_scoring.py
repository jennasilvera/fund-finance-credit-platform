from fund_finance.analytics.risk_scoring import run_all_credit_scoring, run_credit_scoring


def test_credit_scoring_returns_all_facilities():
    results = run_all_credit_scoring(analysis_date="2025-12-31")

    assert len(results) == 3

    facility_ids = {result.facility_id for result in results}

    assert facility_ids == {"FAC001", "FAC002", "FAC003"}


def test_fac002_escalates_due_to_breach():
    result = run_credit_scoring(
        facility_id="FAC002",
        analysis_date="2025-12-31",
    )

    assert result.facility_id == "FAC002"
    assert result.recommendation == "escalate"
    assert "breach" in result.key_risks.lower()


def test_fac003_has_strong_credit_profile():
    result = run_credit_scoring(
        facility_id="FAC003",
        analysis_date="2025-12-31",
    )

    assert result.facility_id == "FAC003"
    assert result.total_score >= 80
    assert result.recommendation in {"approve", "approve_with_conditions"}
