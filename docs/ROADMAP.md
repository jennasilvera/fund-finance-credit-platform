# Project Roadmap

This document outlines completed functionality and potential future enhancements for the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Current Completed Functionality

The platform currently includes:

- Synthetic fund finance data generation
- PostgreSQL schema and local Docker database
- Raw data quality validation
- Referential integrity checks
- Subscription borrowing base analysis
- NAV and hybrid facility analysis
- Covenant monitoring
- Credit scoring and recommendation logic
- Portfolio watchlist classification
- NAV / LTV stress testing
- Data-driven facility stress testing
- Credit memo PDF generation
- Credit memo inventory listing
- Portfolio summary CSV export
- Audit run logging
- One-command demo workflow
- Preflight quality checks
- Automated tests and CI
- Institutional-style documentation

---

## 2. Short-Term Enhancements

Potential next enhancements include:

- Add CLI tests for audit logging commands
- Add CLI tests for portfolio summary export
- Add automated validation that demo workflow completes successfully
- Add sample screenshots to the README
- Add a report index page summarizing generated outputs
- Add better formatting for wide terminal tables
- Add CSV export for covenant monitoring results

---

## 3. Medium-Term Enhancements

Possible medium-term extensions include:

- Quarterly portfolio monitoring report PDF
- Covenant breach report PDF
- Investment committee memo PDF
- NAV trend chart generation
- Facility utilization history chart
- Credit score migration tracking
- Watchlist history tracking
- Data quality exception report
- Scenario analysis for interest rate and liquidity stress

---

## 4. Long-Term Enhancements

Larger architecture extensions could include:

- FastAPI service layer
- Streamlit or React dashboard
- User authentication
- Role-based access control
- Cloud database deployment
- Scheduled monitoring jobs
- Full audit trail persistence for every workflow step
- Database migrations with Alembic
- Containerized end-to-end app deployment

---

## 5. Scope Discipline

The project intentionally does not attempt to reproduce a real bank credit system.

It focuses on demonstrating:

- Practical credit analytics
- Fund finance workflow understanding
- Data controls
- SQL-backed processing
- Python engineering
- CLI workflow design
- Report automation
- Documentation quality

This keeps the project credible, reviewable, and explainable.
