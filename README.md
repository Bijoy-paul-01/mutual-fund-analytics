# Indian Mutual Fund Analytics & Ingestion Engine

Comprehensive end-to-end data analytics and quantitative evaluation pipeline for the Indian mutual fund industry. This project ingests, audits, validates, and processes mutual fund master data, daily NAV history, AUM trends, category flows, investor transactions, portfolio holdings, and benchmark indices, with live NAV integration via `mfapi.in`.

---

## 📁 Project Architecture

```
mutual-fund-analytics/
├── data/
│   ├── raw/                           # Raw immutable datasets and live API responses
│   │   ├── 01_fund_master.csv
│   │   ├── 02_nav_history.csv
│   │   ├── 03_aum_by_fund_house.csv
│   │   ├── 04_monthly_sip_inflows.csv
│   │   ├── 05_category_inflows.csv
│   │   ├── 06_industry_folio_count.csv
│   │   ├── 07_scheme_performance.csv
│   │   ├── 08_investor_transactions.csv
│   │   ├── 09_portfolio_holdings.csv
│   │   ├── 10_benchmark_indices.csv
│   │   ├── live_nav_125497.csv        # HDFC Top 100 Direct / SBI Small Cap live NAV
│   │   ├── live_nav_119551.csv        # SBI Bluechip live NAV
│   │   ├── live_nav_120503.csv        # ICICI Bluechip live NAV
│   │   ├── live_nav_118632.csv        # Nippon Large Cap live NAV
│   │   ├── live_nav_119092.csv        # Axis Bluechip live NAV
│   │   ├── live_nav_120841.csv        # Kotak Bluechip live NAV
│   │   └── live_nav_key_schemes_summary.csv
│   └── processed/                     # Cleaned, transformed, feature-engineered data
├── notebooks/
│   └── 01_data_ingestion_and_exploration.ipynb
├── sql/
│   └── schema.sql                     # Relational DDL table definitions
├── dashboard/                         # Interactive dashboards (Plotly / Streamlit)
├── reports/
│   └── data_quality_summary.md        # Automated data quality audit reports
├── .gitignore
├── requirements.txt                   # Pinned project dependencies
├── data_ingestion.py                  # Ingestion, validation & profiling script
├── live_nav_fetch.py                  # Live API NAV client (mfapi.in)
└── README.md
```

---

## 📊 Dataset Catalog (10 Provided Datasets)

| # | Dataset | Raw File | Dimensions | Primary Key / Grain | Description |
|---|---------|----------|------------|---------------------|-------------|
| 1 | **Fund Master** | `01_fund_master.csv` | 40 × 15 | `amfi_code` | Scheme metadata, expense ratio, exit load, SEBI category code, risk level |
| 2 | **NAV History** | `02_nav_history.csv` | 46,000 × 3 | `amfi_code` + `date` | Daily NAV records (1,150 trading days per scheme, 2022 to 2026) |
| 3 | **AUM by Fund House** | `03_aum_by_fund_house.csv` | 90 × 5 | `date` + `fund_house` | Quarterly assets under management across top 10 AMCs |
| 4 | **Monthly SIP Inflows** | `04_monthly_sip_inflows.csv` | 48 × 6 | `month` | Industry SIP volume, active accounts, new SIPs, and SIP AUM |
| 5 | **Category Inflows** | `05_category_inflows.csv` | 144 × 3 | `month` + `category` | Net category flows across equity, debt, liquid, and hybrid segments |
| 6 | **Industry Folio Count** | `06_industry_folio_count.csv` | 21 × 6 | `month` | Quarterly & monthly folio growth partitioned by asset class |
| 7 | **Scheme Performance** | `07_scheme_performance.csv` | 40 × 19 | `amfi_code` | 1/3/5-year CAGR returns, alpha, beta, Sharpe, Sortino, max drawdown |
| 8 | **Investor Transactions**| `08_investor_transactions.csv` | 32,778 × 13 | `investor_id` + `transaction_date` | Retail & HNI transactions, demographics, tier, income, payment mode, KYC |
| 9 | **Portfolio Holdings** | `09_portfolio_holdings.csv` | 322 × 8 | `amfi_code` + `stock_symbol` | Top equity holdings, sector weights, market capitalization |
| 10 | **Benchmark Indices** | `10_benchmark_indices.csv` | 8,050 × 3 | `date` + `index_name` | Daily closing prices for NIFTY50, NIFTY100, Midcap150, Smallcap, Gilt, Liquid |

---

## 🌐 Live NAV Ingestion Engine (`live_nav_fetch.py`)

Integrates with the live Association of Mutual Funds in India (AMFI) API endpoint (`https://api.mfapi.in/mf/<code)`:
- Target scheme: **125497** (HDFC Top 100 Direct / Direct Equity)
- 5 Key Schemes:
  - **119551**: SBI Bluechip Fund
  - **120503**: ICICI Bluechip Fund
  - **118632**: Nippon Large Cap Fund
  - **119092**: Axis Bluechip Fund
  - **120841**: Kotak Bluechip Fund

### Execution:
```bash
python live_nav_fetch.py
```
Output records are parsed into clean pandas DataFrames, normalized with `YYYY-MM-DD` timestamps, and saved under `data/raw/live_nav_<code.csv`.

---

## 🔍 Data Quality & Referential Integrity Audit

Run the automated profiling and validation pipeline:
```bash
python data_ingestion.py
```

### Key Findings:
- **Referential Integrity**: **100% Validated**. All 40 schemes in `fund_master` exist in `nav_history` with exactly 1,150 continuous daily records per scheme (zero missing, zero orphaned).
- **Fund Houses (AMCs)**: 10 unique fund houses (SBI, ICICI, HDFC, Nippon, Kotak, Axis, Aditya Birla Sun Life, UTI, Mirae Asset, DSP).
- **Categories & Sub-Categories**: 2 broad classes (`Equity`, `Debt`) distributed across 12 SEBI-defined sub-categories (`Large Cap`, `Mid Cap`, `Small Cap`, `Flexi Cap`, `ELSS`, `Liquid`, etc.).
- **Plan Spread**: Direct plans average 0.78% expense ratio vs Regular plans at 1.35% (57 bps distributor commission spread).
- **Missing Data**: 12 missing values in `monthly_sip_inflows['yoy_growth_pct']` representing the base year 2022 prior to year-over-year calculation.
- **Max Drawdowns**: Ranging from -2.23% (low-volatility Gilt) to -33.5% (High beta equity), reflecting realistic historical market corrections.
- **Transactions & KYC**: 30,146 verified transactions and 2,632 pending verification.

---

## 🚀 Setup & Installation

```bash
# Clone repository
git clone https://github.com/Bijoy-paul-01/mutual-fund-analytics.git
cd mutual-fund-analytics

# Install dependencies
pip install -r requirements.txt
```
