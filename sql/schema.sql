-- Fund Finance Credit Underwriting & Portfolio Monitoring Platform
-- PostgreSQL schema
-- Simulated data only. No real fund, investor, borrower, or bank data.

DROP TABLE IF EXISTS audit_runs CASCADE;
DROP TABLE IF EXISTS credit_recommendations CASCADE;
DROP TABLE IF EXISTS monitoring_events CASCADE;
DROP TABLE IF EXISTS borrowing_base_snapshots CASCADE;
DROP TABLE IF EXISTS covenant_terms CASCADE;
DROP TABLE IF EXISTS facility_terms CASCADE;
DROP TABLE IF EXISTS portfolio_companies CASCADE;
DROP TABLE IF EXISTS nav_history CASCADE;
DROP TABLE IF EXISTS capital_calls CASCADE;
DROP TABLE IF EXISTS capital_commitments CASCADE;
DROP TABLE IF EXISTS investors CASCADE;
DROP TABLE IF EXISTS funds CASCADE;
DROP TABLE IF EXISTS fund_managers CASCADE;

CREATE TABLE fund_managers (
    manager_id VARCHAR(20) PRIMARY KEY,
    manager_name TEXT NOT NULL,
    headquarters_country TEXT NOT NULL,
    total_aum_usd NUMERIC(18,2) CHECK (total_aum_usd >= 0),
    strategy_focus TEXT NOT NULL,
    years_operating INTEGER CHECK (years_operating >= 0),
    prior_funds_count INTEGER CHECK (prior_funds_count >= 0),
    realized_track_record_flag BOOLEAN NOT NULL DEFAULT FALSE,
    sponsor_risk_rating TEXT NOT NULL
);

CREATE TABLE funds (
    fund_id VARCHAR(20) PRIMARY KEY,
    manager_id VARCHAR(20) NOT NULL REFERENCES fund_managers(manager_id),
    fund_name TEXT NOT NULL,
    fund_type TEXT NOT NULL CHECK (fund_type IN ('PE', 'VC', 'Growth', 'Private Credit', 'Infrastructure')),
    vintage_year INTEGER NOT NULL,
    fund_size_usd NUMERIC(18,2) CHECK (fund_size_usd >= 0),
    committed_capital_usd NUMERIC(18,2) CHECK (committed_capital_usd >= 0),
    called_capital_usd NUMERIC(18,2) CHECK (called_capital_usd >= 0),
    uncalled_capital_usd NUMERIC(18,2) CHECK (uncalled_capital_usd >= 0),
    nav_usd NUMERIC(18,2) CHECK (nav_usd >= 0),
    dpi NUMERIC(8,4) CHECK (dpi >= 0),
    tvpi NUMERIC(8,4) CHECK (tvpi >= 0),
    net_irr NUMERIC(8,4),
    investment_period_end DATE,
    fund_term_end DATE,
    base_currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    fund_status TEXT NOT NULL CHECK (fund_status IN ('fundraising', 'investing', 'harvesting', 'extension', 'liquidating')),
    CHECK (called_capital_usd <= committed_capital_usd),
    CHECK (uncalled_capital_usd <= committed_capital_usd)
);

CREATE TABLE investors (
    investor_id VARCHAR(20) PRIMARY KEY,
    investor_name TEXT NOT NULL,
    investor_type TEXT NOT NULL CHECK (
        investor_type IN (
            'pension',
            'sovereign_wealth',
            'endowment',
            'insurer',
            'fund_of_funds',
            'family_office',
            'hnw',
            'foundation',
            'asset_manager'
        )
    ),
    country TEXT NOT NULL,
    external_rating TEXT,
    internal_rating TEXT NOT NULL,
    included_in_borrowing_base_flag BOOLEAN NOT NULL DEFAULT TRUE,
    investor_category TEXT NOT NULL CHECK (
        investor_category IN (
            'rated_included',
            'non_rated_included',
            'designated',
            'excluded'
        )
    ),
    affiliate_group TEXT,
    liquidity_watch_flag BOOLEAN NOT NULL DEFAULT FALSE,
    side_letter_restriction_flag BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE capital_commitments (
    commitment_id VARCHAR(20) PRIMARY KEY,
    fund_id VARCHAR(20) NOT NULL REFERENCES funds(fund_id),
    investor_id VARCHAR(20) NOT NULL REFERENCES investors(investor_id),
    commitment_amount_usd NUMERIC(18,2) NOT NULL CHECK (commitment_amount_usd > 0),
    called_amount_usd NUMERIC(18,2) NOT NULL CHECK (called_amount_usd >= 0),
    uncalled_amount_usd NUMERIC(18,2) NOT NULL CHECK (uncalled_amount_usd >= 0),
    commitment_date DATE NOT NULL,
    default_status TEXT NOT NULL CHECK (default_status IN ('current', 'late', 'defaulted')),
    exclusion_reason TEXT,
    CHECK (called_amount_usd <= commitment_amount_usd),
    CHECK (uncalled_amount_usd <= commitment_amount_usd)
);

CREATE TABLE capital_calls (
    capital_call_id VARCHAR(20) PRIMARY KEY,
    fund_id VARCHAR(20) NOT NULL REFERENCES funds(fund_id),
    investor_id VARCHAR(20) NOT NULL REFERENCES investors(investor_id),
    call_date DATE NOT NULL,
    due_date DATE NOT NULL,
    amount_called_usd NUMERIC(18,2) NOT NULL CHECK (amount_called_usd >= 0),
    amount_funded_usd NUMERIC(18,2) NOT NULL CHECK (amount_funded_usd >= 0),
    days_late INTEGER NOT NULL DEFAULT 0 CHECK (days_late >= 0),
    call_purpose TEXT NOT NULL CHECK (
        call_purpose IN ('investment', 'fees', 'expenses', 'debt_repayment', 'follow_on')
    ),
    status TEXT NOT NULL CHECK (
        status IN ('funded', 'late', 'partially_funded', 'defaulted')
    ),
    CHECK (due_date >= call_date),
    CHECK (amount_funded_usd <= amount_called_usd)
);

CREATE TABLE nav_history (
    nav_id VARCHAR(20) PRIMARY KEY,
    fund_id VARCHAR(20) NOT NULL REFERENCES funds(fund_id),
    reporting_date DATE NOT NULL,
    gross_nav_usd NUMERIC(18,2) NOT NULL CHECK (gross_nav_usd >= 0),
    net_nav_usd NUMERIC(18,2) NOT NULL CHECK (net_nav_usd >= 0),
    quarter_over_quarter_nav_change_pct NUMERIC(8,4),
    valuation_policy TEXT,
    valuation_source TEXT,
    audit_status TEXT NOT NULL CHECK (
        audit_status IN ('audited', 'unaudited', 'manager_estimate')
    )
);

CREATE TABLE portfolio_companies (
    company_id VARCHAR(20) PRIMARY KEY,
    fund_id VARCHAR(20) NOT NULL REFERENCES funds(fund_id),
    company_name TEXT NOT NULL,
    sector TEXT NOT NULL,
    geography TEXT NOT NULL,
    investment_date DATE NOT NULL,
    cost_basis_usd NUMERIC(18,2) NOT NULL CHECK (cost_basis_usd >= 0),
    current_fair_value_usd NUMERIC(18,2) NOT NULL CHECK (current_fair_value_usd >= 0),
    ownership_pct NUMERIC(8,4) CHECK (ownership_pct >= 0 AND ownership_pct <= 100),
    revenue_growth_pct NUMERIC(8,4),
    ebitda_margin_pct NUMERIC(8,4),
    cash_runway_months INTEGER CHECK (cash_runway_months >= 0),
    last_round_date DATE,
    last_round_type TEXT,
    valuation_mark TEXT CHECK (valuation_mark IN ('up', 'flat', 'down')),
    non_performing_flag BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE facility_terms (
    facility_id VARCHAR(20) PRIMARY KEY,
    fund_id VARCHAR(20) NOT NULL REFERENCES funds(fund_id),
    facility_type TEXT NOT NULL CHECK (facility_type IN ('subscription', 'nav', 'hybrid')),
    lender_name TEXT NOT NULL,
    commitment_amount_usd NUMERIC(18,2) NOT NULL CHECK (commitment_amount_usd > 0),
    outstanding_amount_usd NUMERIC(18,2) NOT NULL CHECK (outstanding_amount_usd >= 0),
    maturity_date DATE NOT NULL,
    pricing_bps NUMERIC(10,2) CHECK (pricing_bps >= 0),
    unused_fee_bps NUMERIC(10,2) CHECK (unused_fee_bps >= 0),
    advance_rate_rated_pct NUMERIC(8,4) CHECK (advance_rate_rated_pct >= 0 AND advance_rate_rated_pct <= 100),
    advance_rate_non_rated_pct NUMERIC(8,4) CHECK (advance_rate_non_rated_pct >= 0 AND advance_rate_non_rated_pct <= 100),
    advance_rate_designated_pct NUMERIC(8,4) CHECK (advance_rate_designated_pct >= 0 AND advance_rate_designated_pct <= 100),
    nav_advance_rate_pct NUMERIC(8,4) CHECK (nav_advance_rate_pct >= 0 AND nav_advance_rate_pct <= 100),
    max_ltv_pct NUMERIC(8,4) CHECK (max_ltv_pct >= 0 AND max_ltv_pct <= 100),
    min_liquidity_usd NUMERIC(18,2) CHECK (min_liquidity_usd >= 0),
    max_top_investor_concentration_pct NUMERIC(8,4),
    max_top5_investor_concentration_pct NUMERIC(8,4),
    max_top_portfolio_company_pct NUMERIC(8,4),
    max_sector_concentration_pct NUMERIC(8,4),
    reporting_frequency TEXT NOT NULL CHECK (reporting_frequency IN ('monthly', 'quarterly', 'semiannual', 'annual')),
    CHECK (outstanding_amount_usd <= commitment_amount_usd)
);

CREATE TABLE covenant_terms (
    covenant_id VARCHAR(20) PRIMARY KEY,
    facility_id VARCHAR(20) NOT NULL REFERENCES facility_terms(facility_id),
    covenant_name TEXT NOT NULL,
    covenant_type TEXT NOT NULL CHECK (
        covenant_type IN ('financial', 'reporting', 'eligibility', 'concentration', 'liquidity')
    ),
    threshold_value NUMERIC(18,4) NOT NULL,
    threshold_unit TEXT NOT NULL,
    test_frequency TEXT NOT NULL CHECK (test_frequency IN ('monthly', 'quarterly', 'annual')),
    breach_severity TEXT NOT NULL CHECK (
        breach_severity IN ('low', 'medium', 'high', 'event_of_default')
    )
);

CREATE TABLE borrowing_base_snapshots (
    snapshot_id VARCHAR(20) PRIMARY KEY,
    facility_id VARCHAR(20) NOT NULL REFERENCES facility_terms(facility_id),
    reporting_date DATE NOT NULL,
    eligible_uncalled_commitments_usd NUMERIC(18,2) NOT NULL DEFAULT 0,
    eligible_nav_usd NUMERIC(18,2) NOT NULL DEFAULT 0,
    total_borrowing_base_usd NUMERIC(18,2) NOT NULL DEFAULT 0,
    outstanding_amount_usd NUMERIC(18,2) NOT NULL DEFAULT 0,
    availability_usd NUMERIC(18,2) NOT NULL DEFAULT 0,
    utilization_pct NUMERIC(8,4),
    headroom_pct NUMERIC(8,4),
    breach_flag BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE monitoring_events (
    event_id VARCHAR(20) PRIMARY KEY,
    fund_id VARCHAR(20) NOT NULL REFERENCES funds(fund_id),
    facility_id VARCHAR(20) NOT NULL REFERENCES facility_terms(facility_id),
    event_date DATE NOT NULL,
    event_type TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    description TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    escalation_required_flag BOOLEAN NOT NULL DEFAULT FALSE,
    resolved_flag BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE credit_recommendations (
    recommendation_id VARCHAR(20) PRIMARY KEY,
    facility_id VARCHAR(20) NOT NULL REFERENCES facility_terms(facility_id),
    analysis_date DATE NOT NULL,
    risk_score NUMERIC(8,4) NOT NULL CHECK (risk_score >= 0 AND risk_score <= 100),
    credit_rating TEXT NOT NULL,
    recommendation TEXT NOT NULL CHECK (
        recommendation IN ('approve', 'approve_with_conditions', 'decline', 'monitor', 'escalate')
    ),
    key_strengths TEXT,
    key_risks TEXT,
    required_mitigants TEXT,
    analyst_name TEXT NOT NULL
);

CREATE TABLE audit_runs (
    run_id VARCHAR(50) PRIMARY KEY,
    run_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    process_name TEXT NOT NULL,
    input_file_hash TEXT,
    records_processed INTEGER NOT NULL DEFAULT 0,
    records_failed INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL CHECK (status IN ('success', 'failed', 'partial_success')),
    error_message TEXT
);
