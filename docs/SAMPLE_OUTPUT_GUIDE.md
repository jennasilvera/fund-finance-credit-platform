# Sample Output Guide

This document explains the key outputs produced by the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Purpose

The sample output guide helps reviewers understand what the platform produces when the demo workflow is run.

The platform does not only load data. It produces decision-oriented outputs for:

- Borrowing base analysis
- NAV / hybrid collateral analysis
- Covenant monitoring
- Credit scoring
- Monitoring events
- Credit memo generation

---

## 2. Run the Demo

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Run the full workflow:

```bash
make demo
```

Or run preflight checks first:

```bash
make preflight
```

---

## 3. Row Count Output

After loading raw data, the platform prints row counts for the main database tables.

Expected tables include:

| Table | Purpose |
|---|---|
| fund_managers | Sponsor / GP-level data |
| funds | Fund-level data |
| investors | LP / investor profile data |
| capital_commitments | Investor commitments |
| capital_calls | Capital call behavior |
| nav_history | Quarterly NAV history |
| portfolio_companies | Portfolio company collateral data |
| facility_terms | Facility structure and limits |
| covenant_terms | Facility covenant definitions |
| monitoring_events | Credit monitoring events |

This confirms that the synthetic dataset has been loaded into PostgreSQL.

---

## 4. FAC001 Subscription Borrowing Base Output

FAC001 demonstrates a subscription facility supported by eligible uncalled LP commitments.

Key output fields:

| Metric | Meaning |
|---|---|
| Eligible Uncalled Commitments | Capital commitments eligible for borrowing base inclusion |
| Total Borrowing Base | Advance-rate-adjusted collateral value |
| Outstanding Amount | Current drawn facility amount |
| Availability | Remaining borrowing capacity |
| Utilization | Outstanding amount divided by borrowing base |
| Headroom | Cushion above outstanding exposure |
| Top Investor Concentration | Largest LP exposure percentage |
| Breach Flag | Whether the facility breaches borrowing base logic |

Expected interpretation:

FAC001 should show sufficient borrowing base support and no breach.

---

## 5. FAC002 Hybrid Facility Output

FAC002 is the most important sample case.

It demonstrates a hybrid facility supported by both:

- Subscription borrowing base collateral
- NAV collateral

Key output fields:

| Metric | Meaning |
|---|---|
| Eligible NAV | NAV that can support the facility |
| NAV Borrowing Base | NAV collateral after advance rate |
| Subscription Borrowing Base | LP commitment-based support |
| Total Borrowing Base | Combined collateral support |
| LTV | Outstanding exposure divided by eligible NAV |
| Top Company Concentration | Largest portfolio company concentration |
| Breach Flag | Whether any borrowing base or concentration issue is detected |

Expected interpretation:

FAC002 has collateral support, but its top portfolio company concentration triggers a breach.

This is intentional. It demonstrates conservative credit logic.

---

## 6. FAC003 NAV Facility Output

FAC003 demonstrates a NAV facility supported by portfolio asset value.

Key output fields:

| Metric | Meaning |
|---|---|
| Gross NAV | Total portfolio value before eligibility adjustment |
| Eligible NAV | NAV included in collateral support |
| NAV Borrowing Base | Advance-rate-adjusted NAV support |
| LTV | Exposure relative to eligible NAV |
| Top Sector Concentration | Largest sector exposure |
| Breach Flag | Whether NAV or concentration limits are breached |

Expected interpretation:

FAC003 should show strong collateral support and no breach.

---

## 7. Covenant Monitoring Output

The covenant monitoring command tests facility-specific thresholds.

Command:

```bash
fund-finance run-covenant-monitoring --facility-id ALL
```

The output includes:

| Field | Meaning |
|---|---|
| Facility | Facility being tested |
| Covenant | Covenant name |
| Threshold | Required covenant limit |
| Actual | Calculated actual value |
| Result | PASS or BREACH |
| Severity | Simulated breach severity |
| Recommended Action | Suggested credit response |

Expected interpretation:

FAC002 should show a top portfolio company concentration breach.

The demo workflow treats this breach as expected and continues to credit scoring and memo generation.

---

## 8. Credit Scoring Output

The credit scoring command produces a structured recommendation.

Command:

```bash
fund-finance run-credit-scoring --facility-id ALL
```

The output includes:

- Facility ID
- Fund name
- Facility type
- Risk score
- Credit rating
- Recommendation
- Key strengths
- Key risks
- Required mitigants

Expected interpretation:

FAC002 should require escalation because a covenant breach overrides routine scorecard comfort.

---

## 9. Credit Memo Output

Generate a credit memo:

```bash
fund-finance generate-credit-memo --facility-id FAC002
```

Generated files are saved to:

```text
data/outputs/credit_memos/
```

The credit memo consolidates:

- Facility overview
- Fund overview
- Borrowing base analysis
- NAV / hybrid analysis
- Covenant monitoring
- Credit scorecard
- Monitoring events
- Final recommendation

Generated PDFs are excluded from Git because they are output artifacts.

---

## 10. Most Important Output Story

The most important output story is FAC002.

FAC002 shows that the system does not simply approve a facility because there is collateral availability.

Instead:

```text
Collateral support exists.
A concentration covenant is breached.
The breach triggers escalation.
The credit memo reflects the escalated risk.
```

This is the core credit-control logic demonstrated by the project.

---

## 11. Reviewer Takeaway

A reviewer should understand that the platform produces more than calculations.

It produces a controlled workflow:

```text
Data validation
  ↓
Database load
  ↓
Collateral analytics
  ↓
Covenant testing
  ↓
Credit scoring
  ↓
Escalation logic
  ↓
Credit memo reporting
```

That is the institutional value of the project.
