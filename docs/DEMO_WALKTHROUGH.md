# Demo Walkthrough

This document explains what the one-command demo workflow does and how to interpret the results.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Purpose

The demo workflow shows the full lifecycle of the Fund Finance Credit Underwriting & Portfolio Monitoring Platform:

```text
Generate Data
  ↓
Validate Data
  ↓
Load PostgreSQL
  ↓
Run Borrowing Base Analysis
  ↓
Run NAV / Hybrid Analysis
  ↓
Run Covenant Monitoring
  ↓
Run Credit Scoring
  ↓
Generate Credit Memo
```

The goal is to demonstrate that the project is not just a static analysis script. It behaves like a repeatable credit workflow.

---

## 2. Run the Demo

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Run the demo:

```bash
make demo
```

---

## 3. What the Demo Proves

The demo proves that the platform can:

- Generate synthetic fund finance datasets
- Validate raw source data before analysis
- Load structured records into PostgreSQL
- Calculate subscription borrowing base availability
- Analyze NAV and hybrid facility collateral
- Detect covenant breaches
- Apply conservative escalation logic
- Produce credit scoring recommendations
- Generate a PDF credit approval memo

---

## 4. Facilities Used in the Demo

The simulated portfolio contains three example facilities.

| Facility | Type | Purpose |
|---|---|---|
| FAC001 | Subscription Facility | Demonstrates investor-backed borrowing base support |
| FAC002 | Hybrid Facility | Demonstrates combined subscription and NAV collateral with a covenant breach |
| FAC003 | NAV Facility | Demonstrates NAV collateral support and LTV analysis |

---

## 5. Key Demo Case: FAC002

FAC002 is the most important demo case.

It is intentionally designed to show that the system does not simply approve a facility because collateral coverage exists.

FAC002 demonstrates:

- Hybrid facility structure
- NAV support
- Portfolio company concentration testing
- Covenant breach detection
- Escalation recommendation
- Credit memo generation for a more complex case

The key control principle is:

```text
A covenant breach requires escalation even when the overall credit profile appears acceptable.
```

---

## 6. Expected Workflow Output

During the demo, the terminal should show successful execution of:

```bash
python -m fund_finance.etl.generate_sample_data
fund-finance validate-data
fund-finance load-data
fund-finance row-counts
fund-finance run-subscription-borrowing-base --facility-id FAC001
fund-finance run-nav-borrowing-base --facility-id FAC002
fund-finance run-nav-borrowing-base --facility-id FAC003
fund-finance run-covenant-monitoring --facility-id ALL
fund-finance run-credit-scoring --facility-id ALL
fund-finance generate-credit-memo --facility-id FAC002
```

---

## 7. Generated Output

The credit memo PDF is written to:

```text
data/outputs/credit_memos/
```

Generated PDFs are intentionally excluded from Git because they are output artifacts.

---

## 8. Reviewer Interpretation

A technical reviewer should see:

- Modular Python package structure
- CLI-based workflow
- PostgreSQL-backed data model
- Automated testing
- CI validation
- Data quality controls
- Repeatable demo execution

A finance reviewer should see:

- Fund finance terminology
- Borrowing base logic
- NAV facility logic
- Covenant monitoring
- Credit escalation judgment
- Institutional documentation
- Credit memo output

---

## 9. Suggested Interview Explanation

A concise explanation of the demo:

> I built a simulated fund finance underwriting and monitoring platform that models subscription line, NAV, and hybrid facilities. It generates synthetic fund, investor, commitment, NAV, portfolio, facility, and covenant data; validates source quality; loads PostgreSQL; runs borrowing base and NAV collateral analysis; detects covenant breaches; produces credit recommendations; and generates a credit memo PDF. The main control principle is that covenant breaches force escalation even if the scorecard otherwise looks acceptable.

---

## 10. Limitations

The demo is intentionally simplified.

It does not include:

- Real borrower data
- Real investor data
- Legal document review
- Bank-specific credit policy
- Regulatory capital treatment
- Authentication or user permissions
- Production deployment

The project is designed to demonstrate applied credit analytics, data controls, Python engineering, SQL modeling, and institutional documentation.
