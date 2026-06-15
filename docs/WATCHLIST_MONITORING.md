# Watchlist Monitoring

This document describes the portfolio watchlist logic used by the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Purpose

The watchlist module turns monitoring events and credit recommendations into a clear portfolio status.

The goal is to help an analyst or credit officer quickly identify which facilities require routine monitoring, heightened monitoring, watchlist review, or escalation.

---

## 2. CLI Usage

Run:

```bash
fund-finance generate-watchlist
```

This command reads from PostgreSQL and summarizes:

- Facility ID
- Fund name
- Facility type
- Latest credit score
- Latest credit rating
- Latest recommendation
- Open monitoring events
- Escalation events
- Watchlist status
- Rationale

---

## 3. Watchlist Categories

| Status | Meaning |
|---|---|
| Routine Monitoring | No material open escalation or watchlist trigger detected |
| Heightened Monitoring | Open monitoring events or monitor recommendation require closer review |
| Watchlist | Credit rating or recommendation indicates elevated credit risk |
| Critical Watchlist | Escalation event or escalation recommendation is present |

---

## 4. Control Principle

Watchlist logic is intentionally conservative.

A facility with an escalation event or escalation recommendation is automatically classified as Critical Watchlist.

This reinforces the project’s broader control principle:

```text
Hard credit-control issues should not be buried inside a numerical score.
```

---

## 5. Example Interpretation

FAC002 should be classified as a higher-risk monitoring case after covenant monitoring and credit scoring are run.

This is because the facility has a concentration covenant breach and an escalation recommendation.
