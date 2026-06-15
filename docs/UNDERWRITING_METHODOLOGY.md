# Underwriting Methodology

This document explains the credit methodology used by the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

The methodology is designed to simulate how an analyst might evaluate subscription line, NAV, and hybrid fund finance facilities using structured data, transparent credit logic, and repeatable controls.

> This is a simulated portfolio project. The methodology is simplified and should not be interpreted as real bank credit policy.

---

## 1. Credit Workflow

The platform follows a simplified fund finance credit workflow:

```text
Fund Manager
  ↓
Financing Request
  ↓
Facility Type Identification
  ↓
Collateral Analysis
  ↓
Borrowing Base Calculation
  ↓
Concentration Analysis
  ↓
Covenant Testing
  ↓
Credit Scorecard
  ↓
Credit Recommendation
  ↓
Monitoring / Escalation
```

---

## 2. Facility Types

### Subscription Line Facility

A subscription line facility is primarily supported by uncalled investor commitments.

The platform evaluates:

- Investor eligibility
- Uncalled capital
- Investor category
- Internal and external ratings
- Side-letter restrictions
- Default or late-payment status
- Concentration limits
- Advance rates
- Borrowing base availability
- Utilization and headroom

### NAV Facility

A NAV facility is primarily supported by the value of the fund's investment portfolio.

The platform evaluates:

- Latest reported NAV
- Eligible portfolio company value
- Portfolio company concentration
- Sector concentration
- Valuation marks
- Non-performing portfolio exposure
- NAV advance rate
- LTV
- Availability and headroom

### Hybrid Facility

A hybrid facility combines subscription borrowing base support and NAV collateral support.

The platform evaluates both collateral pools and then applies covenant testing to determine whether the facility should pass, be monitored, or be escalated.

---

## 3. Subscription Borrowing Base Methodology

The subscription borrowing base follows this sequence:

```text
Start with investor uncalled commitments
  ↓
Remove excluded investors
  ↓
Remove defaulting or restricted investors
  ↓
Apply top investor concentration cap
  ↓
Apply category-specific advance rates
  ↓
Calculate total borrowing base
  ↓
Compare borrowing base to outstanding amount
```

Investor categories receive different advance rates:

| Investor Category | Treatment |
|---|---|
| Rated Included | Highest advance rate |
| Non-Rated Included | Moderate advance rate |
| Designated | Lower advance rate |
| Excluded | 0% advance rate |

Investors may be excluded due to:

- Side-letter restrictions
- Liquidity watch status
- Excluded investor category
- Default or late-payment behavior
- Borrowing base eligibility flag

---

## 4. NAV Borrowing Base Methodology

The NAV borrowing base follows this sequence:

```text
Start with portfolio company fair value
  ↓
Calculate portfolio concentration
  ↓
Apply top company concentration logic
  ↓
Apply valuation / performance haircuts
  ↓
Calculate eligible NAV
  ↓
Apply NAV advance rate
  ↓
Calculate NAV borrowing base
  ↓
Compare to outstanding amount and LTV threshold
```

Portfolio company haircuts are applied for:

- Down-marked investments
- Non-performing companies
- Elevated concentration risk

---

## 5. Covenant Monitoring Methodology

The platform tests facility covenants based on facility type.

Subscription facility covenants may include:

- Maximum top investor concentration
- Minimum borrowing base coverage

NAV and hybrid facility covenants may include:

- Maximum LTV
- Maximum top portfolio company concentration
- Maximum sector concentration

Each covenant test produces:

- Facility ID
- Covenant name
- Threshold
- Actual value
- Pass / breach result
- Severity
- Recommended action

When a covenant breach is detected, the system creates a monitoring event.

---

## 6. Credit Scorecard

The platform uses a transparent scorecard rather than a black-box model.

| Component | Weight |
|---|---:|
| Sponsor Quality | 20% |
| Investor Base Quality | 20% |
| Fund Performance | 15% |
| Collateral Quality | 15% |
| Liquidity | 10% |
| Covenant Headroom | 10% |
| Reporting / Operational Discipline | 10% |

The scorecard produces a total score between 0 and 100.

---

## 7. Credit Rating Bands

| Score Range | Rating |
|---:|---|
| 85–100 | Strong |
| 70–84 | Acceptable |
| 55–69 | Watchlist |
| 40–54 | Weak |
| Below 40 | Problem Credit |

---

## 8. Recommendation Logic

The recommendation engine can return:

- Approve
- Approve with Conditions
- Monitor
- Escalate
- Decline

A key control rule is built into the system:

> Any covenant breach triggers escalation, even if the quantitative credit score remains acceptable.

This mirrors real credit workflows where scorecards inform judgment but do not override hard credit-policy exceptions.

---

## 9. Monitoring and Escalation

Monitoring events are created for issues such as:

- NAV decline
- Late capital call funding
- Portfolio concentration watch
- Covenant breach

Each monitoring event includes:

- Event type
- Severity
- Description
- Recommended action
- Escalation flag
- Resolution status

---

## 10. Limitations

This project is intentionally simplified. It does not fully model:

- Fund legal documentation
- LP side-letter complexity
- Sovereign immunity analysis
- ERISA issues
- FX exposure
- Tax structuring
- Multi-currency borrowing bases
- Legal enforceability of capital call rights
- Full valuation policy review
- Real bank credit approval policy

The purpose is to demonstrate structured credit thinking, analytics, data engineering, testing, and reporting.
