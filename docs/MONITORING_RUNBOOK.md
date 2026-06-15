# Portfolio Monitoring Runbook

This runbook explains how the Fund Finance Credit Underwriting & Portfolio Monitoring Platform supports post-close monitoring of subscription line, NAV, and hybrid fund finance facilities.

> This is a simulated portfolio project. The runbook demonstrates credit monitoring logic, escalation discipline, and analyst workflow structure.

---

## 1. Monitoring Objective

The purpose of monitoring is to identify credit deterioration after a facility has been underwritten and approved.

The platform monitors:

- Borrowing base availability
- Facility utilization
- NAV movement
- Investor concentration
- Portfolio company concentration
- Sector concentration
- LTV
- Covenant compliance
- Capital call performance
- Monitoring events
- Credit recommendation changes

---

## 2. Monitoring Frequency

| Monitoring Item | Frequency |
|---|---|
| Borrowing base refresh | Monthly or quarterly |
| NAV update | Quarterly |
| Covenant testing | Quarterly |
| Capital call review | After each capital call |
| Credit score refresh | Quarterly |
| Watchlist review | As needed |
| Credit memo refresh | Annual or event-driven |

---

## 3. Standard Monitoring Workflow

```text
Load latest fund and facility data
  ↓
Refresh borrowing base
  ↓
Refresh NAV and portfolio collateral analysis
  ↓
Run covenant monitoring
  ↓
Identify breaches or deterioration
  ↓
Generate monitoring events
  ↓
Refresh credit score
  ↓
Escalate if required
  ↓
Document recommended action
```

---

## 4. Key Monitoring Metrics

### Subscription Facilities

- Eligible uncalled commitments
- Excluded investor exposure
- Top investor concentration
- Top-five investor concentration
- Borrowing base availability
- Utilization percentage
- Capital call late-payment behavior

### NAV Facilities

- Latest NAV
- Eligible NAV
- LTV
- Top portfolio company concentration
- Sector concentration
- Down-marked investments
- Non-performing investments

### Hybrid Facilities

- Subscription borrowing base
- NAV borrowing base
- Combined availability
- Covenant headroom
- Collateral migration from LP support to portfolio NAV support

---

## 5. Escalation Triggers

The system escalates when it detects:

- Covenant breach
- Borrowing base deficiency
- LTV above threshold
- Top portfolio company concentration above threshold
- Sector concentration above threshold
- Investor concentration above threshold
- NAV deterioration
- Late or partial capital call funding
- Open high-severity monitoring event

---

## 6. Covenant Breach Response

When a covenant breach is detected, the analyst should:

1. Confirm source data and calculation logic.
2. Identify the breached covenant.
3. Compare threshold vs actual value.
4. Determine whether the issue is temporary or structural.
5. Generate a monitoring event.
6. Escalate to credit officer if required.
7. Recommend action.

Possible actions include:

- Request updated NAV package
- Request borrowing base certificate
- Restrict additional drawings
- Require paydown
- Exclude affected collateral
- Move facility to watchlist
- Prepare amendment or waiver request

---

## 7. Credit Deterioration Indicators

Examples of deterioration include:

- Reduced borrowing base headroom
- Rising utilization
- Declining NAV
- Lower eligible NAV
- Higher LTV
- Increased concentration
- Investor downgrade or liquidity watch
- Delayed capital call funding
- Open unresolved monitoring events

---

## 8. Analyst Checklist

Before completing a monitoring review, confirm:

- Raw data has been loaded
- Borrowing base calculations have been refreshed
- NAV analysis has been refreshed where applicable
- Covenant monitoring has been run
- Monitoring events have been reviewed
- Credit score has been refreshed
- Escalation recommendation is documented
- Output reports have been generated if needed

---

## 9. Example CLI Workflow

```bash
fund-finance load-data
fund-finance run-subscription-borrowing-base --facility-id FAC001
fund-finance run-nav-borrowing-base --facility-id FAC002
fund-finance run-nav-borrowing-base --facility-id FAC003
fund-finance run-covenant-monitoring --facility-id ALL
fund-finance run-credit-scoring --facility-id ALL
fund-finance generate-credit-memo --facility-id FAC002
```

---

## 10. Control Principle

The platform follows a conservative credit-control rule:

> A covenant breach requires escalation even when the overall scorecard remains acceptable.

This reflects the distinction between analytical credit scoring and hard credit-policy exceptions.
