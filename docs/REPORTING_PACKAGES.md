# Reporting Packages

This document explains the institutional-style reports supported by the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Reporting Objective

The platform is designed to convert structured fund finance data into decision-ready credit and monitoring outputs.

Reports are intended to support:

- Initial underwriting
- Credit approval
- Investment committee review
- Covenant monitoring
- Portfolio surveillance
- Credit deterioration escalation
- Quarterly review workflows

---

## 2. Current Implemented Report

### Credit Approval Memo

The current implemented PDF report is the Credit Approval Memo.

Command:

```bash
fund-finance generate-credit-memo --facility-id FAC001
fund-finance generate-credit-memo --facility-id FAC002
```

Generated files are saved to:

```text
data/outputs/credit_memos/
```

The memo includes:

- Executive summary
- Transaction overview
- Fund and sponsor overview
- Borrowing base analysis
- NAV / hybrid collateral analysis where applicable
- Credit scorecard
- Covenant monitoring
- Monitoring events
- Final credit recommendation

---

## 3. Credit Approval Memo Purpose

The Credit Approval Memo simulates the type of package an analyst might prepare for internal credit review.

It answers:

- What is the proposed facility?
- Who is the fund manager?
- What is the fund strategy?
- What collateral supports the facility?
- What are the key risks?
- Are covenants passing?
- What is the credit recommendation?
- What mitigants are required?

---

## 4. Investment Committee Memo

The Investment Committee Memo is a planned report.

It should be more senior and concise than the full credit memo.

Recommended sections:

- Decision requested
- Transaction summary
- Strategic rationale
- Credit view
- Risk / return overview
- Key structural protections
- Downside case
- Approval conditions
- Final recommendation

Purpose:

The Investment Committee Memo should focus less on raw calculations and more on decision framing.

---

## 5. Portfolio Monitoring Report

The Portfolio Monitoring Report is a planned report.

Recommended sections:

- Facility snapshot
- Utilization
- Borrowing base availability
- NAV movement
- Investor concentration
- Portfolio concentration
- Covenant status
- Monitoring events
- Watchlist status
- Recommended actions

Purpose:

This report supports post-close surveillance and recurring portfolio review.

---

## 6. Covenant Breach Report

The Covenant Breach Report is a planned report.

Recommended sections:

- Breach summary
- Facility affected
- Covenant breached
- Threshold vs actual value
- Cause of breach
- Borrowing base impact
- Credit impact
- Required action
- Recommended escalation path

Purpose:

This report supports rapid escalation when a hard credit-control issue is detected.

---

## 7. Credit Deterioration Alert

The Credit Deterioration Alert is a planned short-form report.

Recommended sections:

- Alert type
- Severity
- Fund
- Facility
- Trigger
- Impact
- Recommended action

Example alert:

```text
Alert Type: Portfolio Concentration Breach
Severity: Medium
Facility: FAC002
Trigger: Top portfolio company concentration exceeded covenant threshold.
Impact: Facility requires credit officer review despite positive availability.
Recommendation: Escalate and request updated portfolio valuation package.
```

---

## 8. Quarterly Review Package

The Quarterly Review Package is a planned report.

Recommended sections:

- Fund performance summary
- NAV trend
- Borrowing base history
- Facility utilization
- Covenant compliance
- Monitoring events
- Credit score migration
- Watchlist movements
- Updated recommendation

Purpose:

This package simulates the recurring review process used after a facility has closed.

---

## 9. Report Control Principles

Reports should be:

- Traceable to source data
- Based on repeatable calculations
- Clear about pass / breach status
- Explicit about recommendation logic
- Conservative when covenants are breached
- Transparent about limitations

---

## 10. Future Reporting Enhancements

Planned enhancements include:

- Investment Committee Memo PDF
- Portfolio Monitoring Report PDF
- Covenant Breach Report PDF
- Credit Deterioration Alert PDF
- Quarterly Review Package PDF
- Charts for NAV, utilization, and credit score migration
- Report index generation
- Sample report screenshots for README
