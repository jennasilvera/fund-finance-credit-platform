# Audit Logging

This document describes the audit run logging layer used by the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Purpose

Audit logging records controlled workflow executions in the `audit_runs` table.

The goal is to make the platform more traceable by recording:

- Process name
- Timestamp
- Records processed
- Records failed
- Status
- Optional error message

---

## 2. Log an Audit Run

Use:

```bash
fund-finance log-audit-run \
  --process-name demo_workflow \
  --status success \
  --records-processed 0 \
  --records-failed 0
```

---

## 3. Show Recent Audit Runs

Use:

```bash
fund-finance show-audit-runs
```

This prints the most recent audit run records from PostgreSQL.

---

## 4. Supported Status Values

Supported statuses are:

- success
- failed
- partial_success

---

## 5. Control Value

Audit logging helps demonstrate that workflows are not only analytical, but also traceable and reviewable.

In a production-style credit platform, recurring processes should leave evidence that they ran, what they processed, and whether they succeeded.
