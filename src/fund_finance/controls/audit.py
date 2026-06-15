from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.engine import Engine

ALLOWED_AUDIT_STATUSES = {"success", "failed", "partial_success"}


@dataclass(frozen=True)
class AuditRun:
    run_id: str
    run_timestamp: datetime
    process_name: str
    input_file_hash: str | None
    records_processed: int
    records_failed: int
    status: str
    error_message: str | None


def normalize_audit_status(status: str) -> str:
    normalized = status.strip().lower().replace("-", "_").replace(" ", "_")

    if normalized not in ALLOWED_AUDIT_STATUSES:
        allowed = ", ".join(sorted(ALLOWED_AUDIT_STATUSES))
        raise ValueError(f"Invalid audit status '{status}'. Allowed values: {allowed}")

    return normalized


def create_audit_run(
    process_name: str,
    status: str,
    records_processed: int = 0,
    records_failed: int = 0,
    input_file_hash: str | None = None,
    error_message: str | None = None,
) -> AuditRun:
    if not process_name.strip():
        raise ValueError("process_name is required")

    if records_processed < 0:
        raise ValueError("records_processed cannot be negative")

    if records_failed < 0:
        raise ValueError("records_failed cannot be negative")

    return AuditRun(
        run_id=f"AUD{uuid4().hex[:12].upper()}",
        run_timestamp=datetime.now(UTC),
        process_name=process_name.strip(),
        input_file_hash=input_file_hash,
        records_processed=records_processed,
        records_failed=records_failed,
        status=normalize_audit_status(status),
        error_message=error_message,
    )


def persist_audit_run(engine: Engine, audit_run: AuditRun) -> str:
    query = text(
        """
        INSERT INTO audit_runs (
            run_id,
            run_timestamp,
            process_name,
            input_file_hash,
            records_processed,
            records_failed,
            status,
            error_message
        )
        VALUES (
            :run_id,
            :run_timestamp,
            :process_name,
            :input_file_hash,
            :records_processed,
            :records_failed,
            :status,
            :error_message
        );
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "run_id": audit_run.run_id,
                "run_timestamp": audit_run.run_timestamp,
                "process_name": audit_run.process_name,
                "input_file_hash": audit_run.input_file_hash,
                "records_processed": audit_run.records_processed,
                "records_failed": audit_run.records_failed,
                "status": audit_run.status,
                "error_message": audit_run.error_message,
            },
        )

    return audit_run.run_id


def fetch_recent_audit_runs(engine: Engine, limit: int = 10) -> list[dict[str, object]]:
    if limit <= 0:
        raise ValueError("limit must be positive")

    query = text(
        """
        SELECT
            run_id,
            run_timestamp,
            process_name,
            records_processed,
            records_failed,
            status,
            error_message
        FROM audit_runs
        ORDER BY run_timestamp DESC
        LIMIT :limit;
        """
    )

    with engine.connect() as connection:
        rows = connection.execute(query, {"limit": limit}).mappings().all()

    return [dict(row) for row in rows]
