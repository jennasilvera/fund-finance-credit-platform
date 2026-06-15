from pathlib import Path

from fund_finance.reporting.report_index import list_credit_memos


def test_list_credit_memos_returns_empty_list_when_directory_missing(tmp_path: Path):
    missing_dir = tmp_path / "missing"

    assert list_credit_memos(missing_dir) == []


def test_list_credit_memos_finds_pdf_files(tmp_path: Path):
    memo_dir = tmp_path / "credit_memos"
    memo_dir.mkdir()

    pdf_path = memo_dir / "credit_approval_memo_FAC002.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 test")

    ignored_path = memo_dir / "notes.txt"
    ignored_path.write_text("ignore me")

    results = list_credit_memos(memo_dir)

    assert len(results) == 1
    assert results[0].filename == "credit_approval_memo_FAC002.pdf"
    assert results[0].path.endswith("credit_approval_memo_FAC002.pdf")
    assert results[0].size_bytes > 0
