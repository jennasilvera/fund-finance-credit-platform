# System Architecture

This document describes the architecture of the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Architecture Objective

The platform is designed as a modular credit analytics system for fund finance underwriting and portfolio monitoring.

It separates:

- Data generation
- Raw data validation
- Database loading
- Analytics calculations
- Covenant monitoring
- Credit scoring
- Report generation
- CLI execution
- Testing and CI

This separation makes the project easier to test, extend, and explain to both technical and finance reviewers.

---

## 2. High-Level Architecture

```text
Synthetic Data Generator
        ↓
Raw CSV Files
        ↓
Data Quality Controls
        ↓
PostgreSQL Database
        ↓
Analytics Engines
        ↓
Covenant Monitoring
        ↓
Credit Scoring
        ↓
Credit Memo / Reports
        ↓
Analyst Review
```

---

## 3. Repository Layers

```text
fund-finance-credit-platform/
├── data/
│   └── raw/                         # Simulated source CSV files
├── docs/                            # Methodology, runbooks, guides, controls
├── scripts/                         # Demo workflow scripts
├── sql/                             # PostgreSQL schema
├── src/fund_finance/
│   ├── analytics/                   # Borrowing base, NAV, covenant, risk engines
│   ├── config/                      # Environment and settings
│   ├── controls/                    # Data quality and validation logic
│   ├── db/                          # Database connection and loading logic
│   ├── etl/                         # Synthetic data generation
│   ├── reporting/                   # PDF memo generation
│   └── cli.py                       # Typer command-line interface
└── tests/                           # Automated tests
```

---

## 4. Data Layer

The data layer contains simulated CSV source files representing:

- Fund managers
- Funds
- Investors
- Capital commitments
- Capital calls
- NAV history
- Portfolio companies
- Facility terms
- Covenant terms
- Monitoring events

The data is generated using:

```bash
python -m fund_finance.etl.generate_sample_data
```

---

## 5. Control Layer

The control layer lives in:

```text
src/fund_finance/controls/
```

The raw data validator checks:

- Required files
- Required columns
- Primary key uniqueness
- Primary key nulls
- Fund capital math
- Commitment math
- Capital call logic
- Facility exposure logic
- Referential integrity across files

Command:

```bash
fund-finance validate-data
```

This layer prevents incomplete or inconsistent source data from flowing into underwriting and monitoring calculations.

---

## 6. Database Layer

The database layer uses PostgreSQL and SQLAlchemy.

Key files:

```text
sql/schema.sql
src/fund_finance/db/connection.py
src/fund_finance/db/load.py
```

The database stores normalized fund finance entities and calculated outputs.

Core tables include:

- funds
- investors
- capital_commitments
- capital_calls
- facility_terms
- covenant_terms
- borrowing_base_snapshots
- monitoring_events
- credit_recommendations
- audit_runs

---

## 7. Analytics Layer

The analytics layer lives in:

```text
src/fund_finance/analytics/
```

It contains:

| Module | Purpose |
|---|---|
| borrowing_base.py | Calculates subscription facility borrowing base support |
| nav_facility.py | Calculates NAV and hybrid facility collateral support |
| covenant_monitoring.py | Tests facility covenants and creates monitoring events |
| risk_scoring.py | Produces credit score, rating, recommendation, strengths, risks, and mitigants |

---

## 8. Reporting Layer

The reporting layer lives in:

```text
src/fund_finance/reporting/
```

Current implemented report:

- Credit Approval Memo PDF

The memo consolidates:

- Transaction summary
- Facility structure
- Borrowing base results
- NAV / hybrid analysis
- Covenant status
- Monitoring events
- Credit scorecard
- Recommendation

Generated reports are written to:

```text
data/outputs/credit_memos/
```

---

## 9. CLI Layer

The CLI is implemented with Typer in:

```text
src/fund_finance/cli.py
```

Important commands include:

```bash
fund-finance check-db
fund-finance validate-data
fund-finance load-data
fund-finance row-counts
fund-finance run-subscription-borrowing-base --facility-id FAC001
fund-finance run-nav-borrowing-base --facility-id FAC002
fund-finance run-covenant-monitoring --facility-id ALL
fund-finance run-credit-scoring --facility-id ALL
fund-finance generate-credit-memo --facility-id FAC002
```

The CLI makes the project easy to demonstrate without manually calling Python functions.

---

## 10. Demo Workflow

The demo workflow is implemented in:

```text
scripts/demo_workflow.sh
```

It can be run with:

```bash
docker compose up -d postgres
make demo
```

The demo runs data generation, validation, loading, analytics, monitoring, scoring, and memo generation.

---

## 11. Testing and CI

The project includes tests for:

- Borrowing base logic
- Covenant monitoring
- Risk scoring
- Report generation
- Data quality validation
- Referential integrity validation

CI is configured through GitHub Actions:

```text
.github/workflows/ci.yml
```

The CI workflow helps demonstrate that the repository is not just a static project; it has repeatable automated checks.

---

## 12. Design Principles

The project follows these design principles:

- Synthetic data only
- Clear separation of layers
- Conservative credit logic
- Repeatable calculations
- Source data validation before analysis
- Covenant breaches force escalation
- Documentation explains both technical and finance logic
- Tests protect core behavior
- CLI supports reviewer-friendly demos

---

## 13. Future Architecture Enhancements

Potential extensions include:

- Persistent audit run logging
- Web dashboard
- Scenario analysis engine
- Stress testing module
- Quarterly monitoring report generator
- Covenant breach PDF report
- User authentication
- Cloud deployment
- Dockerized API service
