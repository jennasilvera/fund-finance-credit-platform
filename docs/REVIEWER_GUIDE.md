# Reviewer Guide

This guide is designed for recruiters, hiring managers, bankers, credit analysts, and technical reviewers evaluating the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. What This Project Is

This is a simulated fund finance credit platform for underwriting and monitoring:

- Subscription line facilities
- NAV facilities
- Hybrid fund finance facilities

It combines credit analysis, portfolio monitoring, data controls, PostgreSQL modeling, Python analytics, reporting automation, and CI-tested software engineering.

---

## 2. What This Project Is Not

This project is not:

- A real bank system
- A real underwriting model
- A proprietary credit policy engine
- A legal documentation review tool
- A production deployment
- A source of real fund, LP, GP, borrower, lender, or portfolio data

All data is synthetic.

---

## 3. Fastest Way to Review

Start with these files:

1. `README.md`
2. `docs/DEMO_WALKTHROUGH.md`
3. `docs/SAMPLE_OUTPUT_GUIDE.md`
4. `docs/ARCHITECTURE.md`
5. `docs/CONTROL_FRAMEWORK.md`
6. `docs/UNDERWRITING_METHODOLOGY.md`

Then review the main code modules:

```text
src/fund_finance/controls/data_quality.py
src/fund_finance/analytics/borrowing_base.py
src/fund_finance/analytics/nav_facility.py
src/fund_finance/analytics/covenant_monitoring.py
src/fund_finance/analytics/risk_scoring.py
src/fund_finance/reporting/credit_memo.py
src/fund_finance/cli.py
```

---

## 4. Recommended Local Review Flow

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Run preflight checks:

```bash
make preflight
```

Run the full demo:

```bash
make demo
```

The demo should generate data, validate it, load PostgreSQL, run analytics, detect a covenant breach, continue through expected escalation, run credit scoring, and generate a credit memo PDF.

---

## 5. Key Case to Review: FAC002

FAC002 is the strongest demonstration case.

It is a hybrid facility with both subscription and NAV collateral support.

The important behavior:

```text
Collateral coverage exists.
A portfolio concentration covenant is breached.
The platform flags the breach.
The recommendation escalates despite broader collateral support.
```

This shows the project is applying credit-control logic, not just producing calculations.

---

## 6. Finance Concepts Demonstrated

The project demonstrates:

- Fund-level financing
- Subscription line borrowing base analysis
- LP eligibility
- Advance rates
- Uncalled capital
- NAV collateral support
- LTV analysis
- Portfolio company concentration
- Sector concentration
- Covenant monitoring
- Monitoring events
- Credit recommendation logic
- Credit memo generation

---

## 7. Technical Concepts Demonstrated

The project demonstrates:

- Python package structure
- PostgreSQL schema design
- SQLAlchemy database connectivity
- pandas-based data validation
- Typer CLI design
- PDF report generation
- Docker Compose service orchestration
- pytest testing
- Ruff linting
- GitHub Actions CI
- Bash workflow scripts
- Repository documentation discipline

---

## 8. Control Concepts Demonstrated

The project includes controls for:

- Required raw data files
- Required source columns
- Primary key uniqueness
- Primary key null checks
- Financial math consistency
- Facility exposure consistency
- Referential integrity across files
- Borrowing base sufficiency
- Covenant breach detection
- Escalation override logic
- CI-based regression protection

---

## 9. What Strong Reviewers Should Notice

A strong reviewer should notice that the project is not just a notebook.

It has:

- Repeatable commands
- Structured data model
- Validated input layer
- Multiple analytics engines
- CLI workflow
- Automated tests
- Documentation for users and reviewers
- PDF reporting output
- Expected breach behavior handled in the demo workflow

---

## 10. How to Judge the Project

This project should be judged on:

- Clarity of credit logic
- Quality of controls
- Completeness of workflow
- Practicality of the CLI demo
- Readability of code
- Repository organization
- Documentation quality
- Ability to explain both finance and engineering decisions

It should not be judged as a complete production banking platform.

---

## 11. Suggested Review Checklist

Before concluding review, confirm:

- CI badge is passing
- `make preflight` passes locally
- `make demo` completes
- FAC002 covenant breach is detected
- Credit scoring continues after expected breach
- Credit memo PDF is generated
- Documentation links in README work
- Synthetic-data disclaimer is visible
- Tests cover core behavior

---

## 12. Project Maturity Summary

The project demonstrates an end-to-end controlled analytics workflow:

```text
Synthetic source data
  ↓
Data quality validation
  ↓
PostgreSQL load
  ↓
Borrowing base and NAV analytics
  ↓
Covenant monitoring
  ↓
Credit scoring
  ↓
Credit memo reporting
  ↓
Reviewer documentation
```

This makes the repository suitable as a portfolio project for fund finance, credit analytics, portfolio monitoring, banking technology, trading operations, risk, and data-focused finance roles.
