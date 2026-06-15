# Data Dictionary

This document defines the core datasets used by the Fund Finance Credit Underwriting & Portfolio Monitoring Platform.

> All data is simulated and used for portfolio demonstration purposes only.

---

## 1. fund_managers

Stores sponsor / GP-level information.

| Column | Description |
|---|---|
| manager_id | Unique fund manager identifier |
| manager_name | Fund manager / sponsor name |
| headquarters_country | Sponsor headquarters country |
| total_aum_usd | Simulated assets under management |
| strategy_focus | Primary investment strategy |
| years_operating | Sponsor operating history |
| prior_funds_count | Number of prior funds |
| realized_track_record_flag | Whether the sponsor has realized historical performance |
| sponsor_risk_rating | Simulated internal sponsor quality rating |

---

## 2. funds

Stores fund-level underwriting data.

| Column | Description |
|---|---|
| fund_id | Unique fund identifier |
| manager_id | Linked fund manager |
| fund_name | Fund name |
| fund_type | PE, VC, Growth, Private Credit, or Infrastructure |
| vintage_year | Fund vintage year |
| fund_size_usd | Total fund size |
| committed_capital_usd | Total committed capital |
| called_capital_usd | Capital already called |
| uncalled_capital_usd | Remaining uncalled capital |
| nav_usd | Latest fund NAV |
| dpi | Distributions to paid-in capital |
| tvpi | Total value to paid-in capital |
| net_irr | Net internal rate of return |
| fund_status | Fund lifecycle stage |

---

## 3. investors

Stores limited partner / investor profile data.

| Column | Description |
|---|---|
| investor_id | Unique investor identifier |
| investor_name | Investor name |
| investor_type | Pension, endowment, insurer, sovereign wealth, family office, etc. |
| country | Investor country |
| external_rating | External credit rating if available |
| internal_rating | Simulated internal investor rating |
| included_in_borrowing_base_flag | Whether investor may be included in borrowing base |
| investor_category | Rated included, non-rated included, designated, or excluded |
| affiliate_group | Affiliate grouping for concentration review |
| liquidity_watch_flag | Indicates liquidity concern |
| side_letter_restriction_flag | Indicates potential restriction affecting eligibility |

---

## 4. capital_commitments

Stores investor commitments to each fund.

| Column | Description |
|---|---|
| commitment_id | Unique commitment identifier |
| fund_id | Linked fund |
| investor_id | Linked investor |
| commitment_amount_usd | Original investor commitment |
| called_amount_usd | Capital already called |
| uncalled_amount_usd | Remaining uncalled commitment |
| commitment_date | Commitment date |
| default_status | Current, late, or defaulted |
| exclusion_reason | Reason investor is excluded from borrowing base if applicable |

---

## 5. capital_calls

Stores capital call funding behavior.

| Column | Description |
|---|---|
| capital_call_id | Unique capital call identifier |
| fund_id | Linked fund |
| investor_id | Linked investor |
| call_date | Capital call date |
| due_date | Funding due date |
| amount_called_usd | Amount requested |
| amount_funded_usd | Amount actually funded |
| days_late | Days funded after due date |
| call_purpose | Investment, fees, expenses, debt repayment, or follow-on |
| status | Funded, late, partially funded, or defaulted |

---

## 6. nav_history

Stores quarterly NAV data.

| Column | Description |
|---|---|
| nav_id | Unique NAV record identifier |
| fund_id | Linked fund |
| reporting_date | NAV reporting date |
| gross_nav_usd | Gross asset value |
| net_nav_usd | Net asset value |
| quarter_over_quarter_nav_change_pct | QoQ NAV movement |
| valuation_policy | Simulated valuation framework |
| valuation_source | Source of valuation data |
| audit_status | Audited, unaudited, or manager estimate |

---

## 7. portfolio_companies

Stores portfolio company collateral data for NAV facilities.

| Column | Description |
|---|---|
| company_id | Unique portfolio company identifier |
| fund_id | Linked fund |
| company_name | Portfolio company name |
| sector | Industry sector |
| geography | Primary geography |
| cost_basis_usd | Original investment cost |
| current_fair_value_usd | Current marked value |
| ownership_pct | Fund ownership percentage |
| revenue_growth_pct | Simulated growth metric |
| ebitda_margin_pct | Simulated profitability metric |
| cash_runway_months | VC-style liquidity runway metric |
| valuation_mark | Up, flat, or down |
| non_performing_flag | Indicates underperforming asset |

---

## 8. facility_terms

Stores financing facility terms.

| Column | Description |
|---|---|
| facility_id | Unique facility identifier |
| fund_id | Linked fund |
| facility_type | Subscription, NAV, or hybrid |
| lender_name | Simulated lender |
| commitment_amount_usd | Facility commitment |
| outstanding_amount_usd | Current drawn balance |
| maturity_date | Facility maturity |
| pricing_bps | Spread in basis points |
| unused_fee_bps | Undrawn fee |
| advance_rate_rated_pct | Advance rate for rated included investors |
| advance_rate_non_rated_pct | Advance rate for non-rated investors |
| advance_rate_designated_pct | Advance rate for designated investors |
| nav_advance_rate_pct | NAV advance rate |
| max_ltv_pct | Maximum permitted LTV |
| min_liquidity_usd | Minimum liquidity requirement |
| max_top_investor_concentration_pct | Top investor concentration limit |
| max_top5_investor_concentration_pct | Top-five investor concentration limit |
| max_top_portfolio_company_pct | Top company concentration limit |
| max_sector_concentration_pct | Sector concentration limit |
| reporting_frequency | Required reporting cadence |

---

## 9. covenant_terms

Stores facility covenant definitions.

| Column | Description |
|---|---|
| covenant_id | Unique covenant identifier |
| facility_id | Linked facility |
| covenant_name | Covenant name |
| covenant_type | Financial, reporting, eligibility, concentration, or liquidity |
| threshold_value | Covenant threshold |
| threshold_unit | Percent, x, USD, or other unit |
| test_frequency | Monthly, quarterly, or annual |
| breach_severity | Low, medium, high, or event of default |

---

## 10. borrowing_base_snapshots

Stores calculated borrowing base outputs.

| Column | Description |
|---|---|
| snapshot_id | Unique snapshot identifier |
| facility_id | Linked facility |
| reporting_date | Snapshot date |
| eligible_uncalled_commitments_usd | Eligible uncalled commitments |
| eligible_nav_usd | Eligible NAV collateral |
| total_borrowing_base_usd | Total borrowing base |
| outstanding_amount_usd | Current drawn amount |
| availability_usd | Remaining availability |
| utilization_pct | Utilization percentage |
| headroom_pct | Borrowing base headroom |
| breach_flag | Whether the facility breaches borrowing base logic |

---

## 11. monitoring_events

Stores credit monitoring and escalation events.

| Column | Description |
|---|---|
| event_id | Unique event identifier |
| fund_id | Linked fund |
| facility_id | Linked facility |
| event_date | Event date |
| event_type | NAV decline, covenant breach, late funding, etc. |
| severity | Low, medium, high, or critical |
| description | Event description |
| recommended_action | Analyst recommended action |
| escalation_required_flag | Whether escalation is required |
| resolved_flag | Whether issue is resolved |

---

## 12. credit_recommendations

Stores credit scorecard outputs and recommendations.

| Column | Description |
|---|---|
| recommendation_id | Unique recommendation identifier |
| facility_id | Linked facility |
| analysis_date | Analysis date |
| risk_score | Total credit score |
| credit_rating | Strong, acceptable, watchlist, weak, or problem credit |
| recommendation | Approve, approve with conditions, monitor, escalate, or decline |
| key_strengths | Main credit strengths |
| key_risks | Main credit risks |
| required_mitigants | Required mitigants or monitoring actions |
| analyst_name | Simulated analyst name |

---

## 13. audit_runs

Reserved for process audit logging.

| Column | Description |
|---|---|
| run_id | Unique process run identifier |
| run_timestamp | Process timestamp |
| process_name | Pipeline or control name |
| input_file_hash | Input file hash |
| records_processed | Records processed |
| records_failed | Records failed |
| status | Success, failed, or partial success |
| error_message | Error message if applicable |
