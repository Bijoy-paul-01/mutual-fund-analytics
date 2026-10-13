# Mutual Fund Analytics - Day 1: Data Ingestion & Quality Summary

## 1. Executive Summary
- **Status**: All 10 CSV datasets loaded and validated successfully.
- **AMFI Scheme Master Coverage**: 40 schemes.
- **NAV History Series**: 46,000 daily NAV records (1,150 trading days per scheme from Jan 2022 to May 2026).
- **Referential Integrity**: 100% VALIDATED (0 missing, 0 orphaned).

## 2. Ingested Datasets Overview
| # | Dataset Key | Raw File | Rows | Columns | Primary Key / Grain |
|---|-------------|----------|------|---------|---------------------|
| 1 | `fund_master` | `01_fund_master.csv` | 40 | 15 | amfi_code (Scheme & Plan level) |
| 2 | `nav_history` | `02_nav_history.csv` | 46,000 | 3 | amfi_code + date (Daily NAV per scheme) |
| 3 | `aum_by_fund_house` | `03_aum_by_fund_house.csv` | 90 | 5 | date + fund_house (Quarterly AMC AUM) |
| 4 | `monthly_sip_inflows` | `04_monthly_sip_inflows.csv` | 48 | 6 | month (Industry monthly SIP metrics) |
| 5 | `category_inflows` | `05_category_inflows.csv` | 144 | 3 | month + category (Category monthly flows) |
| 6 | `industry_folio_count` | `06_industry_folio_count.csv` | 21 | 6 | month (Total and asset-class folios) |
| 7 | `scheme_performance` | `07_scheme_performance.csv` | 40 | 19 | amfi_code (Trailing risk & return metrics) |
| 8 | `investor_transactions` | `08_investor_transactions.csv` | 32,778 | 13 | investor_id + transaction_date + amfi_code |
| 9 | `portfolio_holdings` | `09_portfolio_holdings.csv` | 322 | 8 | amfi_code + stock_symbol (Stock allocations) |
| 10 | `benchmark_indices` | `10_benchmark_indices.csv` | 8,050 | 3 | date + index_name (Daily index closing) |

## 3. Fund Master Architecture
- **Total Fund Houses (AMCs)**: 10 (Aditya Birla Sun Life MF, Axis Mutual Fund, DSP Mutual Fund, HDFC Mutual Fund, ICICI Prudential MF, Kotak Mahindra MF, Mirae Asset MF, Nippon India MF, SBI Mutual Fund, UTI Mutual Fund)
- **Broad Categories**: Debt, Equity
- **Sub-Categories**: ELSS, Flexi Cap, Gilt, Index, Index/ETF, Large & Mid Cap, Large Cap, Liquid, Mid Cap, Short Duration, Small Cap, Value
- **Risk Spectrum**: High, Low, Moderate, Moderately High, Very High
- **AMFI Code Format**: Standardized 6-digit numeric codes assigning distinct identifiers to Direct and Regular plans.

## 4. Anomalies & Data Quality Observations
1. **`monthly_sip_inflows` YoY Growth Missing Values**: 12 records (Jan 2022 to Dec 2022) have `NaN` for `yoy_growth_pct` due to absent 2021 historical base.
2. **`scheme_performance` Max Drawdowns**: All 40 schemes exhibit negative values for `max_drawdown_pct` (ranging from -2.23% to -33.5%), consistent with financial drawdown definitions.
3. **`investor_transactions` KYC Status**: 2,632 out of 32,778 transactions are in `Pending` status; requires filtering in KYC-compliant workflows.
4. **Live API Mapping Note**: Scheme codes in the educational dataset map to specific curated schemes, whereas live AMFI database reflects live AMC registrations. Handled gracefully in `live_nav_fetch.py`.

## 5. Referential Integrity Check
- `fund_master` to `nav_history`: **100% Matched**.
- Missing schemes in NAV history: **0**.
- Orphan NAV history codes: **0**.