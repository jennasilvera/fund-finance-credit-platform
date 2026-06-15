import pytest

from fund_finance.controls.audit import create_audit_run, normalize_audit_status


def test_normalize_audit_status_accepts_valid_values():
    assert normalize_audit_status("success") == "success"
    assert normalize_audit_status("partial success") == "partial_success"
    assert normalize_audit_status("FAILED") == "failed"


def test_normalize_audit_status_rejects_invalid_value():
    with pytest.raises(ValueError, match="Invalid audit status"):
        normalize_audit_status("unknown")


def test_create_audit_run_builds_valid_record():
    audit_run = create_audit_run(
        process_name="demo_workflow",
        status="success",
        records_processed=10,
        records_failed=0,
    )

    assert audit_run.run_id.startswith("AUD")
    assert audit_run.process_name == "demo_workflow"
    assert audit_run.status == "success"
    assert audit_run.records_processed == 10
    assert audit_run.records_failed == 0


def test_create_audit_run_rejects_negative_counts():
    with pytest.raises(ValueError, match="records_processed cannot be negative"):
        create_audit_run(
            process_name="bad_process",
            status="success",
            records_processed=-1,
        )
