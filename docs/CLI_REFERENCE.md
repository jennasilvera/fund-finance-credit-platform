# CLI Reference

This document lists the command-line interface commands available in the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Environment Commands

### Check Database Connection

```bash
fund-finance check-db
```

Confirms PostgreSQL connectivity and lists public database tables.

---

### Show Row Counts

```bash
fund-finance row-counts
```

Displays row counts for core database tables.

---

## 2. Data Commands

### Generate Simulated Raw Data

```bash
python -m fund_finance.etl.generate_sample_data
```

Creates synthetic CSV files in:

```text
data/raw/
```

---

### Validate Raw Data

```bash
fund-finance validate-data
```

Runs raw data quality checks before loading or analysis.

Checks include:

- Required files
- Required columns
- Primary key uniqueness
- Primary key nulls
- Financial math consistency
- Facility exposure logic
- Referential integrity across files

---

### Load Data

```bash
fund-finance load-data
```

Loads raw CSV files into PostgreSQL.

---

## 3. Borrowing Base Commands

### Run Subscription Borrowing Base

```bash
fund-finance run-subscription-borrowing-base --facility-id FAC001
```

Calculates subscription facility borrowing base support using eligible uncalled commitments and advance rates.

---

### Run NAV / Hybrid Borrowing Base

```bash
fund-finance run-nav-borrowing-base --facility-id FAC002
fund-finance run-nav-borrowing-base --facility-id FAC003
```

Calculates NAV-backed or hybrid facility borrowing base support.

---

## 4. Covenant Monitoring Commands

### Run Covenant Monitoring

```bash
fund-finance run-covenant-monitoring --facility-id ALL
```

Tests facility covenants and saves monitoring events for detected breaches.

Expected demo behavior:

- FAC001 passes
- FAC002 has a top portfolio company concentration breach
- FAC003 passes

---

## 5. Credit Scoring Commands

### Run Credit Scoring

```bash
fund-finance run-credit-scoring --facility-id ALL
```

Generates facility-level credit scores, ratings, recommendations, strengths, risks, and mitigants.

---

## 6. Watchlist Monitoring Commands

### Generate Portfolio Watchlist

```bash
fund-finance generate-watchlist
```

Summarizes facilities by watchlist status using credit recommendations and monitoring events.

Watchlist statuses include:

- Routine Monitoring
- Heightened Monitoring
- Watchlist
- Critical Watchlist

---

## 7. Stress Testing Commands

### Run Manual NAV Stress Test

```bash
fund-finance run-nav-stress \
  --facility-id FAC002 \
  --eligible-nav-usd 640000000 \
  --outstanding-amount-usd 180000000 \
  --max-ltv-pct 30
```

Runs downside NAV/LTV stress scenarios using manually supplied values.

---

### Run Data-Driven Facility Stress Test

```bash
fund-finance run-facility-stress --facility-id FAC002
```

Pulls facility, outstanding amount, max LTV, and latest NAV data from PostgreSQL, then runs downside NAV/LTV stress scenarios.

---

## 8. Reporting Commands

### Generate Credit Memo

```bash
fund-finance generate-credit-memo --facility-id FAC002
```

Generates a PDF credit approval memo.

Output path:

```text
data/outputs/credit_memos/
```

---

## 9. Workflow Commands

### Run Preflight Checks

```bash
make preflight
```

Runs linting, tests, shell syntax checks, database connectivity, data generation, and raw data validation.

---

### Run Full Demo

```bash
make demo
```

Runs the full end-to-end workflow:

```text
Generate synthetic data
Validate raw data
Load PostgreSQL
Run borrowing base analysis
Run NAV / hybrid analysis
Run covenant monitoring
Run credit scoring
Generate watchlist
Run stress testing
Generate credit memo
```

---

## 10. Recommended Review Flow

For a clean local review:

```bash
docker compose up -d postgres
make preflight
make demo
```

This confirms the project can run through quality checks and the full credit workflow.

---

## 11. Audit Logging Commands

### Log an Audit Run

```bash
fund-finance log-audit-run \
  --process-name demo_workflow \
  --status success \
  --records-processed 0 \
  --records-failed 0
```

Persists a process execution record to the `audit_runs` table.

---

### Show Recent Audit Runs

```bash
fund-finance show-audit-runs
```

Displays recent audit run records from PostgreSQL.

---

## 12. Credit Memo Inventory Command

### List Generated Credit Memos

```bash
fund-finance list-credit-memos
```

Displays generated credit memo PDF outputs, including filename, path, file size, and modified timestamp.

---

## 13. Portfolio Summary Export Command

### Export Portfolio Summary CSV

```bash
fund-finance export-portfolio-summary
```

Exports a facility-level portfolio monitoring summary to:

```text
data/outputs/portfolio_summary.csv
```

The export includes facility type, commitment amount, outstanding amount, latest credit score, latest recommendation, open monitoring events, and escalation events.
