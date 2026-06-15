from fund_finance.reporting.credit_memo import generate_credit_approval_memo


def test_credit_approval_memo_pdf_generated():
    output_path = generate_credit_approval_memo(
        facility_id="FAC001",
        analysis_date="2025-12-31",
    )

    assert output_path.exists()
    assert output_path.suffix == ".pdf"
    assert output_path.stat().st_size > 0
