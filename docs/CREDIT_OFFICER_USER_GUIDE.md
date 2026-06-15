# Credit Officer User Guide

This guide explains how a credit officer or senior risk reviewer would interpret outputs from the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Credit Officer Review Objective

The credit officer reviews whether the facility should be approved, monitored, escalated, amended, reduced, or declined.

The platform supports review of:

- Borrowing base sufficiency
- Investor eligibility
- LP concentration
- NAV collateral quality
- LTV
- Portfolio concentration
- Covenant compliance
- Monitoring events
- Credit scorecard output
- Analyst recommendation
- Required mitigants

---

## 2. Key Questions for Review

A credit officer should ask:

1. Is the facility supported by eligible collateral?
2. Is the borrowing base sufficient relative to outstanding exposure?
3. Are any investors excluded, restricted, late, or defaulting?
4. Is the fund overly reliant on one investor or group of investors?
5. Is the NAV collateral diversified and supportable?
6. Are portfolio company or sector concentrations elevated?
7. Are any covenants breached?
8. Is the credit score consistent with the recommendation?
9. Are there open monitoring events?
10. Are the required mitigants strong enough?

---

## 3. Subscription Facility Review

For subscription facilities, focus on:

- Eligible uncalled commitments
- Investor quality
- Investor category mix
- Side-letter restrictions
- Capital call payment behavior
- Top investor concentration
- Top-five investor concentration
- Borrowing base headroom

A subscription facility may appear well supported by total uncalled capital, but the credit officer should focus only on eligible borrowing base collateral.

---

## 4. NAV Facility Review

For NAV facilities, focus on:

- Eligible NAV
- LTV
- Portfolio company concentration
- Sector concentration
- Down-marked assets
- Non-performing assets
- Valuation support
- Exit and liquidity assumptions

NAV facilities are more sensitive to valuation quality and portfolio concentration than subscription facilities.

---

## 5. Hybrid Facility Review

For hybrid facilities, review both collateral sources:

- Subscription borrowing base support
- NAV collateral support
- Combined borrowing base
- LTV
- Investor concentration
- Portfolio concentration

Hybrid facilities can appear stronger after including NAV support, but may still require escalation if a concentration covenant is breached.

---

## 6. Covenant Breach Interpretation

A covenant breach should override routine approval logic.

Even when a credit score remains acceptable, a breach should trigger:

- Credit officer review
- Source data confirmation
- Calculation review
- Sponsor / fund manager follow-up
- Additional monitoring
- Potential amendment or waiver analysis

The project applies this principle directly: any covenant breach produces an escalation recommendation.

---

## 7. Recommendation Review

The platform may return:

| Recommendation | Meaning |
|---|---|
| Approve | Credit profile is strong and no material breach is detected |
| Approve with Conditions | Credit is acceptable but requires specific mitigants |
| Monitor | Credit profile is weakening and requires closer review |
| Escalate | Covenant breach or material concern requires credit officer review |
| Decline | Risk profile is not acceptable under the simulated framework |

---

## 8. Mitigant Review

Potential mitigants include:

- More frequent borrowing base reporting
- Updated NAV package
- Additional valuation support
- Investor exclusion from borrowing base
- Reduced availability
- Restriction on additional drawings
- Paydown requirement
- Watchlist placement
- Amendment or waiver process

A good mitigant should directly address the identified risk.

---

## 9. Example Credit Officer Interpretation

FAC002 is a useful example.

The hybrid facility benefits from both subscription borrowing base support and NAV collateral support. However, the top portfolio company concentration exceeds the simulated covenant threshold.

Credit officer interpretation:

- Facility has collateral support.
- Availability alone is not sufficient to approve.
- Portfolio concentration creates elevated single-name risk.
- Covenant breach requires escalation.
- Additional drawings should be reviewed carefully.
- Updated NAV and portfolio commentary should be requested.

---

## 10. Credit Officer Checklist

Before accepting an analyst recommendation, confirm:

- Facility type is correctly identified
- Borrowing base logic matches the facility type
- Excluded investors receive no borrowing base value
- Concentration calculations are reviewed
- NAV collateral is supportable
- Covenant tests are complete
- Breaches are escalated
- Monitoring events are reviewed
- Required mitigants are specific
- Credit memo supports the recommendation

---

## 11. Limitations

This project does not replace real credit judgment or real bank policy.

It does not model:

- Legal documentation
- Jurisdiction-specific enforceability
- LP sovereign immunity
- FX risk
- Tax structuring
- Regulatory capital
- Full due diligence
- Negotiated facility documentation

It is designed to demonstrate credit thinking, controls, analytics, documentation, and technical execution.
