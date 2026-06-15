# Stress Testing

This document describes the downside stress testing logic used by the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> This project uses simulated data only and is intended for portfolio demonstration purposes.

---

## 1. Purpose

Stress testing evaluates how NAV-backed and hybrid facilities perform under downside valuation scenarios.

The goal is to assess whether a facility remains within LTV limits after simulated NAV declines.

---

## 2. Current Stress Test

The current implemented stress test applies NAV shocks to eligible NAV and recalculates LTV.

Default scenarios:

- 10% NAV decline
- 20% NAV decline
- 30% NAV decline

---

## 3. Core Formula

```text
stressed_eligible_nav = eligible_nav * (1 + nav_shock_pct)

stressed_ltv = outstanding_amount / stressed_eligible_nav
```

A breach is detected when:

```text
stressed_ltv_pct > max_ltv_pct
```

---

## 4. Why This Matters

NAV and hybrid facilities are sensitive to valuation declines.

A facility may pass base-case monitoring, but still become vulnerable under a modest NAV decline.

Stress testing helps identify:

- Thin LTV headroom
- Downside exposure
- Facilities that may require closer monitoring
- Cases where collateral support is more fragile than it appears

---

## 5. Example Interpretation

A hybrid facility with:

```text
Eligible NAV: $640 million
Outstanding Amount: $180 million
Maximum LTV: 30%
```

Base-case LTV:

```text
180 / 640 = 28.1%
```

After a 10% NAV decline:

```text
180 / 576 = 31.3%
```

This creates a stressed LTV breach.

---

## 6. Review Takeaway

Stress testing adds downside-case discipline to the project.

The platform does not only calculate current availability; it also evaluates whether collateral support remains adequate under adverse valuation movement.
