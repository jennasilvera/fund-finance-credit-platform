# Control Framework

This document describes the control framework used by the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Control Objective

The platform is designed to support a controlled credit workflow for fund finance underwriting and portfolio monitoring.

The control framework is intended to ensure that:

- Source data is complete before analysis
- Primary keys are unique
- Cross-file references are valid
- Borrowing base calculations are repeatable
- NAV collateral logic is transparent
- Covenant breaches are detected
- Breaches override routine scorecard logic
- Escalation recommendations are documented
- Outputs are traceable and reviewable

---

## 2. Control Layers

The project contains multiple control layers:

| Layer | Purpose |
|---|---|
| Raw data validation | Confirms source CSV files are complete and logically consistent |
| Referential integrity checks | Confirms IDs across files connect correctly |
| Borrowing base controls | Calculates eligible collateral and detects insufficient availability |
| NAV / hybrid controls | Tests LTV, NAV collateral, and portfolio concentration |
| Covenant monitoring | Tests facility covenants against calculated values |
| Credit scoring | Produces a structured risk score and recommendation |
| Escalation override | Forces escalation when a covenant breach is detected |
| Documentation | Provides methodology, runbooks, and review guides |
| Tests and CI | Confirms core logic continues to pass after changes |

---

## 3. Raw Data Validation Controls

Before analysis, the platform validates the source files in:

```text
data/raw/
```

The command is:

```bash
fund-finance validate-data
```

The validation layer checks:

- Required files
- Required columns
- Primary key nulls
- Primary key duplicates
- Fund capital math
- Investor commitment math
- Capital call date logic
- Capital call funded amount logic
- Facility exposure logic

If validation fails, the command exits with an error.

---

## 4. Referential Integrity Controls

The platform also validates cross-file relationships.

Examples:

| Child File | Field | Parent File |
|---|---|---|
| funds | manager_id | fund_managers |
| capital_commitments | fund_id | funds |
| capital_commitments | investor_id | investors |
| capital_calls | fund_id | funds |
| capital_calls | investor_id | investors |
| nav_history | fund_id | funds |
| portfolio_companies | fund_id | funds |
| facility_terms | fund_id | funds |
| covenant_terms | facility_id | facility_terms |
| monitoring_events | facility_id | facility_terms |

This prevents orphaned records from entering analysis.

---

## 5. Borrowing Base Controls

The subscription borrowing base engine controls for:

- Investor eligibility
- Advance rate by investor category
- Excluded investors
- Uncalled commitment support
- Outstanding facility exposure
- Availability
- Utilization
- Headroom
- Investor concentration

A facility can be flagged if the calculated borrowing base does not support the outstanding exposure.

---

## 6. NAV and Hybrid Facility Controls

The NAV / hybrid engine controls for:

- Eligible NAV
- NAV advance rate
- LTV
- Portfolio company concentration
- Sector concentration
- Non-performing portfolio companies
- Combined collateral support for hybrid facilities

This allows the platform to distinguish between subscription, NAV, and hybrid collateral structures.

---

## 7. Covenant Monitoring Controls

Covenant monitoring checks facility-specific limits including:

- Maximum LTV
- Minimum liquidity
- Top investor concentration
- Top-five investor concentration
- Top portfolio company concentration
- Sector concentration
- Reporting or monitoring-related requirements

Detected breaches are saved as monitoring events.

---

## 8. Escalation Override Rule

The platform applies a conservative credit policy rule:

```text
Any covenant breach requires escalation, even if the overall scorecard remains acceptable.
```

This is important because a hard covenant breach is not merely a scoring input. It is a credit-policy exception requiring review.

---

## 9. Credit Scoring Controls

The credit scoring model evaluates:

- Fund performance
- Sponsor quality
- Investor base quality
- Facility structure
- Borrowing base support
- NAV collateral support
- Covenant and monitoring issues

The model produces:

- Risk score
- Credit rating
- Recommendation
- Key strengths
- Key risks
- Required mitigants

---

## 10. Reporting Controls

The platform currently generates a Credit Approval Memo PDF.

The memo consolidates:

- Transaction summary
- Facility terms
- Borrowing base output
- NAV / hybrid analysis
- Covenant status
- Credit score
- Monitoring events
- Final recommendation

Generated PDFs are output artifacts and are excluded from Git.

---

## 11. Testing and CI Controls

The repository includes automated tests for:

- Borrowing base calculations
- Covenant monitoring
- Risk scoring
- Report generation
- Data quality validation
- Referential integrity validation

GitHub Actions runs CI to confirm that linting and tests pass.

---

## 12. Analyst Control Checklist

Before presenting results, an analyst should confirm:

- Raw data validation passes
- Referential integrity checks pass
- Database is loaded successfully
- Borrowing base calculations have been refreshed
- NAV analysis has been refreshed where applicable
- Covenant monitoring has been run
- Credit scoring has been run
- Monitoring events have been reviewed
- Credit recommendation is consistent with control logic
- Credit memo or reporting package has been generated

---

## 13. Limitations

This project does not represent a real bank control framework.

It does not include:

- Real legal documentation review
- Bank-specific credit policy
- Regulatory capital analysis
- Internal model validation
- Permissioning and access control
- Production incident management
- Full audit log persistence

The purpose is to demonstrate practical credit analytics, control design, technical implementation, and institutional documentation.
