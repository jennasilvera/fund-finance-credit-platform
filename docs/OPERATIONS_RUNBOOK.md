# Operations Runbook

This document describes how to operate, troubleshoot, and validate the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Purpose

The operations runbook provides repeatable procedures for running the platform locally, validating data, loading PostgreSQL, executing analytics, generating reports, and troubleshooting common issues.

The goal is to make the project reviewable as a controlled workflow rather than a one-off script.

---

## 2. Standard Startup Procedure

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Confirm the container is running:

```bash
docker ps
```

Check database connectivity:

```bash
fund-finance check-db
```

---

## 3. Standard Full Workflow

Run the full demo workflow:

```bash
make demo
```

This executes:

- Generate synthetic data
- Validate raw data
- Load PostgreSQL
- Check row counts
- Run borrowing base analysis
- Run NAV / hybrid analysis
- Run covenant monitoring
- Run credit scoring
- Generate credit memo

---

## 4. Data Refresh Procedure

Regenerate simulated raw data:

```bash
python -m fund_finance.etl.generate_sample_data
```

Validate raw data:

```bash
fund-finance validate-data
```

Load data:

```bash
fund-finance load-data
```

Check row counts:

```bash
fund-finance row-counts
```

---

## 5. Analytics Procedure

Run subscription borrowing base analysis:

```bash
fund-finance run-subscription-borrowing-base --facility-id FAC001
```

Run NAV / hybrid analysis:

```bash
fund-finance run-nav-borrowing-base --facility-id FAC002
fund-finance run-nav-borrowing-base --facility-id FAC003
```

Run covenant monitoring:

```bash
fund-finance run-covenant-monitoring --facility-id ALL
```

Run credit scoring:

```bash
fund-finance run-credit-scoring --facility-id ALL
```

---

## 6. Reporting Procedure

Generate a credit memo:

```bash
fund-finance generate-credit-memo --facility-id FAC002
```

Generated PDFs are saved to:

```text
data/outputs/credit_memos/
```

Output reports are ignored by Git because they are generated artifacts.

---

## 7. Common Issues and Fixes

### PostgreSQL is not running

Symptom:

```text
connection refused
```

Fix:

```bash
docker compose up -d postgres
fund-finance check-db
```

### Raw data validation fails

Symptom:

```text
Data quality validation failed
```

Fix:

1. Review the validation table printed by the CLI.
2. Check the affected CSV file in `data/raw/`.
3. Regenerate sample data if needed:

```bash
python -m fund_finance.etl.generate_sample_data
fund-finance validate-data
```

### Tables are empty

Symptom:

```text
row-counts shows zero records
```

Fix:

```bash
fund-finance load-data
fund-finance row-counts
```

### Credit memo is missing

Symptom:

```text
No PDF appears in data/outputs/credit_memos/
```

Fix:

```bash
fund-finance generate-credit-memo --facility-id FAC002
ls -l data/outputs/credit_memos/
```

---

## 8. Control Expectations

Before relying on outputs, confirm:

- PostgreSQL is running
- Raw data validation passes
- Data has been loaded
- Borrowing base analysis has been refreshed
- NAV analysis has been refreshed where applicable
- Covenant monitoring has been run
- Credit scoring has been run
- Generated reports reflect current data

---

## 9. CI Procedure

Run local checks before pushing:

```bash
ruff check src tests
pytest
bash -n scripts/demo_workflow.sh
```

GitHub Actions should pass after each push.

---

## 10. Shutdown Procedure

Stop local services:

```bash
docker compose down
```

Stop and remove volumes if a full database reset is needed:

```bash
docker compose down -v
```

Then restart and reload:

```bash
docker compose up -d postgres
fund-finance load-data
```
