# Analyst User Guide

This guide explains how an analyst would use the Fund Finance Credit Underwriting & Portfolio Monitoring Platform to run underwriting, monitoring, covenant testing, credit scoring, and report generation workflows.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Analyst Workflow Overview

The platform supports the following analyst workflow:

```text
Start PostgreSQL
  ↓
Generate simulated fund finance data
  ↓
Load data into PostgreSQL
  ↓
Run borrowing base analysis
  ↓
Run NAV / hybrid collateral analysis
  ↓
Run covenant monitoring
  ↓
Run credit scoring
  ↓
Generate credit memo PDF
  ↓
Review outputs and escalation logic
```

---

## 2. Start the Database

Start the local PostgreSQL container:

```bash
docker compose up -d postgres
```

Check that the database is available:

```bash
fund-finance check-db
```

---

## 3. Generate Sample Data

Generate simulated fund, investor, NAV, portfolio, facility, and covenant data:

```bash
python -m fund_finance.etl.generate_sample_data
```

This creates CSV files in:

```text
data/raw/
```

---

## 4. Load Data

Load the generated CSV files into PostgreSQL:

```bash
fund-finance load-data
```

Check row counts:

```bash
fund-finance row-counts
```

Expected loaded tables include:

- fund_managers
- funds
- investors
- capital_commitments
- capital_calls
- nav_history
- portfolio_companies
- facility_terms
- covenant_terms
- monitoring_events

---

## 5. Run Subscription Borrowing Base Analysis

Run the subscription borrowing base engine for FAC001:

```bash
fund-finance run-subscription-borrowing-base --facility-id FAC001
```

The output shows:

- Eligible uncalled commitments
- Total borrowing base
- Outstanding amount
- Availability
- Utilization
- Headroom
- Investor concentration
- Breach flag

---

## 6. Run NAV / Hybrid Borrowing Base Analysis

Run hybrid facility analysis:

```bash
fund-finance run-nav-borrowing-base --facility-id FAC002
```

Run NAV facility analysis:

```bash
fund-finance run-nav-borrowing-base --facility-id FAC003
```

The output shows:

- Eligible NAV
- NAV borrowing base
- Subscription borrowing base if hybrid
- Total borrowing base
- LTV
- Portfolio company concentration
- Sector concentration
- Breach flag

---

## 7. Run Covenant Monitoring

Run covenant monitoring for all facilities:

```bash
fund-finance run-covenant-monitoring --facility-id ALL
```

The command tests each facility covenant and identifies pass / breach status.

If a breach is detected, the platform creates a monitoring event and recommends an escalation action.

---

## 8. Run Credit Scoring

Run credit scoring for all facilities:

```bash
fund-finance run-credit-scoring --facility-id ALL
```

The credit scoring output includes:

- Facility ID
- Fund name
- Facility type
- Total score
- Credit rating
- Recommendation
- Key risks
- Score component breakdown

The recommendation can be:

- Approve
- Approve with Conditions
- Monitor
- Escalate
- Decline

---

## 9. Generate Credit Approval Memo

Generate a clean facility memo:

```bash
fund-finance generate-credit-memo --facility-id FAC001
```

Generate a more interesting breached hybrid facility memo:

```bash
fund-finance generate-credit-memo --facility-id FAC002
```

Generated PDFs are saved to:

```text
data/outputs/credit_memos/
```

Generated PDFs are ignored by Git because they are output artifacts.

---

## 10. Suggested Demo Flow

For a recruiter, banker, or interviewer, use this flow:

```bash
docker compose up -d postgres
python -m fund_finance.etl.generate_sample_data
fund-finance load-data
fund-finance run-subscription-borrowing-base --facility-id FAC001
fund-finance run-nav-borrowing-base --facility-id FAC002
fund-finance run-covenant-monitoring --facility-id ALL
fund-finance run-credit-scoring --facility-id ALL
fund-finance generate-credit-memo --facility-id FAC002
```

This demonstrates the full underwriting and monitoring workflow.

---

## 11. Example Interpretation

FAC001 demonstrates a subscription facility with sufficient borrowing base support.

FAC002 demonstrates a hybrid facility where NAV support improves collateral coverage, but portfolio company concentration still triggers a covenant breach and escalation.

FAC003 demonstrates a NAV facility with acceptable LTV and collateral support.

This creates a realistic credit story: the system does not only calculate availability; it also detects covenant issues and forces escalation when required.

---

## 12. Analyst Review Checklist

Before presenting outputs, confirm:

- Data loaded successfully
- Borrowing base results are generated
- NAV analysis is generated where applicable
- Covenant monitoring has been run
- Monitoring events have been reviewed
- Credit recommendations have been saved
- PDF memo has been generated
- Tests and CI are passing
