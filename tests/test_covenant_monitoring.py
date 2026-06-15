from fund_finance.analytics.covenant_monitoring import run_covenant_monitoring


def test_fac001_covenants_pass():
    results = run_covenant_monitoring(
        facility_id="FAC001",
        reporting_date="2025-12-31",
    )

    assert len(results) == 2
    assert all(result.result == "PASS" for result in results)


def test_fac002_detects_portfolio_concentration_breach():
    results = run_covenant_monitoring(
        facility_id="FAC002",
        reporting_date="2025-12-31",
    )

    breaches = [result for result in results if result.result == "BREACH"]

    assert len(breaches) >= 1
    assert any(
        result.covenant_name == "Maximum Top Portfolio Company Concentration"
        for result in breaches
    )


def test_fac003_covenants_pass():
    results = run_covenant_monitoring(
        facility_id="FAC003",
        reporting_date="2025-12-31",
    )

    assert len(results) == 2
    assert all(result.result == "PASS" for result in results)
