# Fund Finance Credit Underwriting & Portfolio Monitoring Platform

[![Fund Finance Credit Platform CI](https://github.com/jennasilvera/fund-finance-credit-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/jennasilvera/fund-finance-credit-platform/actions/workflows/ci.yml)


A simulated fund finance credit underwriting and portfolio monitoring platform for subscription line, NAV, and hybrid facilities.

This project models how a bank fund finance team might support underwriting, credit approval, covenant monitoring, and portfolio surveillance for private equity and venture capital fund-level financing.

> This project uses fully simulated data only. It does not contain real fund, investor, LP, GP, borrower, lender, portfolio company, or proprietary bank information.

---

## Preflight Checks

Before pushing changes or demoing the project, run:

```bash
make preflight
```

The preflight workflow checks:

- Ruff linting
- pytest test suite
- demo workflow shell syntax
- PostgreSQL connectivity
- simulated data generation
- raw data quality validation

---
## One-Command Demo

After starting PostgreSQL, run the full demonstration workflow:

```bash
docker compose up -d postgres
make demo
```

The demo workflow:

- Generates simulated fund finance data
- Validates raw CSV inputs
- Loads data into PostgreSQL
- Runs borrowing base analysis
- Runs NAV / hybrid facility analysis
- Runs covenant monitoring
- Runs credit scoring
- Generates a credit approval memo PDF

---

## Documentation

- [Underwriting Methodology](docs/UNDERWRITING_METHODOLOGY.md)
- [Portfolio Monitoring Runbook](docs/MONITORING_RUNBOOK.md)
- [Watchlist Monitoring](docs/WATCHLIST_MONITORING.md)
- [Data Dictionary](docs/DATA_DICTIONARY.md)
- [Data Quality Controls](docs/DATA_QUALITY_CONTROLS.md)
- [Control Framework](docs/CONTROL_FRAMEWORK.md)
- [Stress Testing](docs/STRESS_TESTING.md)
- [Analyst User Guide](docs/ANALYST_USER_GUIDE.md)
- [Credit Officer User Guide](docs/CREDIT_OFFICER_USER_GUIDE.md)
- [Reporting Packages](docs/REPORTING_PACKAGES.md)
- [Demo Walkthrough](docs/DEMO_WALKTHROUGH.md)
- [Sample Output Guide](docs/SAMPLE_OUTPUT_GUIDE.md)
- [Reviewer Guide](docs/REVIEWER_GUIDE.md)
- [System Architecture](docs/ARCHITECTURE.md)
- [Operations Runbook](docs/OPERATIONS_RUNBOOK.md)

---

## Project Objective

The goal of this project is to demonstrate practical credit, finance, data, and engineering skills relevant to:

- Fund Finance
- Corporate & Leveraged Finance
- Credit Analysis
- Financial Institutions Group
- Portfolio Monitoring
- Investment Banking Analyst roles
- Risk Management and Credit Officer workflows

The platform simulates the lifecycle of a fund finance transaction:

```text
Fund Manager
  ↓
Financing Request
  ↓
Credit Underwriting
  ↓
Borrowing Base Analysis
  ↓
Risk Assessment
  ↓
Credit Recommendation
  ↓
Credit Approval Memo
  ↓
Portfolio Monitoring
  ↓
Covenant Testing
  ↓
Escalation / Watchlist Review
