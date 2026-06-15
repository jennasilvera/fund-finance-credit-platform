# Data Quality Controls

This document describes the raw data validation layer used by the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Control Objective

The data quality layer validates raw CSV inputs before they are loaded into PostgreSQL or used for underwriting and monitoring analysis.

The goal is to prevent bad source data from flowing into:

- Borrowing base calculations
- NAV collateral analysis
- Covenant monitoring
- Credit scoring
- Credit memo generation
- Portfolio monitoring outputs

---

## 2. Validation Command

Run:

```bash
fund-finance validate-data
```

Expected successful output:

```text
Raw data quality validation passed.
```

If issues are detected, the command prints a table of validation failures and exits with a non-zero status code.

---

## 3. Control Categories

The validation layer currently checks:

- Required source files
- Required columns
- Primary key nulls
- Primary key duplicates
- Fund capital consistency
- Investor commitment consistency
- Capital call date logic
- Capital call funding logic
- Facility commitment and outstanding exposure logic

---

## 4. Required File Checks

The platform expects raw CSV files in:

```text
data/raw/
```

Required files include:

- fund_managers.csv
- funds.csv
- investors.csv
- capital_commitments.csv
- capital_calls.csv
- nav_history.csv
- portfolio_companies.csv
- facility_terms.csv
- covenant_terms.csv
- monitoring_events.csv

Missing files are treated as high-severity data quality issues.

---

## 5. Required Column Checks

Each file must contain the minimum columns needed by the analytics engine.

Examples:

| File | Required Columns |
|---|---|
| funds.csv | fund_id, manager_id, fund_name, committed_capital_usd, called_capital_usd, uncalled_capital_usd, nav_usd |
| investors.csv | investor_id, investor_name, investor_category, included_in_borrowing_base_flag |
| facility_terms.csv | facility_id, fund_id, facility_type, commitment_amount_usd, outstanding_amount_usd |
| covenant_terms.csv | covenant_id, facility_id, covenant_name, threshold_value |

---

## 6. Primary Key Controls

Each source file has a primary identifier.

Examples:

| Table | Primary Key |
|---|---|
| funds | fund_id |
| investors | investor_id |
| capital_commitments | commitment_id |
| capital_calls | capital_call_id |
| facility_terms | facility_id |
| covenant_terms | covenant_id |

The validation layer checks that primary keys are:

- Not null
- Unique within the file

---

## 7. Fund Capital Controls

For funds, the platform checks that:

- Called capital does not exceed committed capital
- Uncalled capital does not exceed committed capital

These checks protect subscription borrowing base calculations from inflated or inconsistent fund-level capital data.

---

## 8. Commitment Controls

For investor commitments, the platform checks that:

- Commitment amounts are positive
- Called amounts do not exceed commitment amounts
- Uncalled amounts do not exceed commitment amounts

These controls protect investor-level borrowing base eligibility.

---

## 9. Capital Call Controls

For capital calls, the platform checks that:

- Due dates are on or after call dates
- Funded amounts do not exceed called amounts

These controls help identify source data errors in LP funding behavior.

---

## 10. Facility Exposure Controls

For facility terms, the platform checks that:

- Facility commitment is positive
- Outstanding exposure does not exceed facility commitment

These checks prevent invalid exposure data from flowing into utilization, LTV, and availability calculations.

---

## 11. Conservative Failure Behavior

If data quality issues are detected, the command exits with an error.

This is intentional.

A production-style credit platform should stop the workflow when required source data is missing, duplicated, malformed, or logically inconsistent.

---

## 12. Example Issue Output

A duplicate investor ID would produce an issue similar to:

```text
Table: investors
Check: primary_key_unique
Severity: high
Message: investor_id contains duplicate values
```

---

## 13. Analyst Control Checklist

Before running underwriting or monitoring workflows, an analyst should confirm:

- Raw CSV files are present
- Required columns exist
- Primary keys are unique
- Capital balances are logically consistent
- Facility exposure does not exceed commitment
- `fund-finance validate-data` passes successfully

---

## 14. Future Enhancements

Planned enhancements include:

- Referential integrity checks across files
- Rating value validation
- Date freshness checks
- NAV reporting lag checks
- Negative value checks across all financial fields
- Audit run persistence to PostgreSQL
- Data quality exception reports
