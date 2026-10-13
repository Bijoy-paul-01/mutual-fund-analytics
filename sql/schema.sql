-- Mutual Fund Analytics - Database Schema Definition
-- Compatible with SQLite, PostgreSQL, DuckDB, MySQL

-- 1. Fund Master Table
CREATE TABLE IF NOT EXISTS fund_master (
    amfi_code INTEGER PRIMARY KEY,
    fund_house VARCHAR(100) NOT NULL,
    scheme_name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    plan VARCHAR(20) NOT NULL,
    launch_date DATE,
    benchmark VARCHAR(100),
    expense_ratio_pct DECIMAL(5, 2),
    exit_load_pct DECIMAL(5, 2),
    min_sip_amount INTEGER,
    min_lumpsum_amount INTEGER,
    fund_manager VARCHAR(100),
    risk_category VARCHAR(50),
    sebi_category_code VARCHAR(20)
);

-- 2. Daily NAV History Table
CREATE TABLE IF NOT EXISTS nav_history (
    amfi_code INTEGER NOT NULL,
    date DATE NOT NULL,
    nav DECIMAL(12, 4) NOT NULL,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES fund_master (amfi_code)
);

-- 3. Quarterly AUM by Fund House
CREATE TABLE IF NOT EXISTS aum_by_fund_house (
    date DATE NOT NULL,
    fund_house VARCHAR(100) NOT NULL,
    aum_lakh_crore DECIMAL(10, 2),
    aum_crore BIGINT,
    num_schemes INTEGER,
    PRIMARY KEY (date, fund_house)
);

-- 4. Monthly SIP Inflows
CREATE TABLE IF NOT EXISTS monthly_sip_inflows (
    month VARCHAR(7) PRIMARY KEY, -- YYYY-MM
    sip_inflow_crore INTEGER,
    active_sip_accounts_crore DECIMAL(8, 2),
    new_sip_accounts_lakh DECIMAL(8, 2),
    sip_aum_lakh_crore DECIMAL(8, 2),
    yoy_growth_pct DECIMAL(6, 2)
);

-- 5. Monthly Category Inflows
CREATE TABLE IF NOT EXISTS category_inflows (
    month VARCHAR(7) NOT NULL,
    category VARCHAR(50) NOT NULL,
    net_inflow_crore DECIMAL(12, 2),
    PRIMARY KEY (month, category)
);

-- 6. Industry Folio Count
CREATE TABLE IF NOT EXISTS industry_folio_count (
    month VARCHAR(7) PRIMARY KEY,
    total_folios_crore DECIMAL(8, 2),
    equity_folios_crore DECIMAL(8, 2),
    debt_folios_crore DECIMAL(8, 2),
    hybrid_folios_crore DECIMAL(8, 2),
    others_folios_crore DECIMAL(8, 2)
);

-- 7. Scheme Performance & Risk Ratios
CREATE TABLE IF NOT EXISTS scheme_performance (
    amfi_code INTEGER PRIMARY KEY,
    scheme_name VARCHAR(255) NOT NULL,
    fund_house VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    plan VARCHAR(20),
    return_1yr_pct DECIMAL(6, 2),
    return_3yr_pct DECIMAL(6, 2),
    return_5yr_pct DECIMAL(6, 2),
    benchmark_3yr_pct DECIMAL(6, 2),
    alpha DECIMAL(6, 2),
    beta DECIMAL(6, 2),
    sharpe_ratio DECIMAL(6, 2),
    sortino_ratio DECIMAL(6, 2),
    std_dev_ann_pct DECIMAL(6, 2),
    max_drawdown_pct DECIMAL(6, 2),
    aum_crore BIGINT,
    expense_ratio_pct DECIMAL(5, 2),
    morningstar_rating INTEGER,
    risk_grade VARCHAR(50),
    FOREIGN KEY (amfi_code) REFERENCES fund_master (amfi_code)
);

-- 8. Investor Transactions
CREATE TABLE IF NOT EXISTS investor_transactions (
    investor_id VARCHAR(50) NOT NULL,
    transaction_date DATE NOT NULL,
    amfi_code INTEGER NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount_inr BIGINT NOT NULL,
    state VARCHAR(50),
    city VARCHAR(50),
    city_tier VARCHAR(10),
    age_group VARCHAR(20),
    gender VARCHAR(10),
    annual_income_lakh DECIMAL(8, 2),
    payment_mode VARCHAR(20),
    kyc_status VARCHAR(20),
    FOREIGN KEY (amfi_code) REFERENCES fund_master (amfi_code)
);

-- 9. Portfolio Holdings
CREATE TABLE IF NOT EXISTS portfolio_holdings (
    amfi_code INTEGER NOT NULL,
    stock_symbol VARCHAR(50) NOT NULL,
    stock_name VARCHAR(150),
    sector VARCHAR(100),
    weight_pct DECIMAL(6, 2),
    market_value_cr DECIMAL(12, 2),
    current_price_inr DECIMAL(10, 2),
    portfolio_date DATE,
    PRIMARY KEY (amfi_code, stock_symbol),
    FOREIGN KEY (amfi_code) REFERENCES fund_master (amfi_code)
);

-- 10. Benchmark Indices
CREATE TABLE IF NOT EXISTS benchmark_indices (
    date DATE NOT NULL,
    index_name VARCHAR(50) NOT NULL,
    close_value DECIMAL(12, 2),
    PRIMARY KEY (date, index_name)
);
