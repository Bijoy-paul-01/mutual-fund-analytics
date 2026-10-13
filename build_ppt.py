import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    BG_DARK = RGBColor(15, 23, 42)        # Slate 900
    CARD_BG = RGBColor(30, 41, 59)        # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)    # Slate 700
    TEXT_WHITE = RGBColor(248, 250, 252)  # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184)  # Slate 400
    ACCENT_TEAL = RGBColor(20, 184, 166)  # Teal 500
    ACCENT_BLUE = RGBColor(56, 189, 248)  # Sky 400
    ACCENT_GOLD = RGBColor(250, 204, 21)  # Amber 400
    ACCENT_GREEN = RGBColor(34, 197, 94)  # Green 500

    def add_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="MUTUAL FUND QUANTITATIVE ANALYTICS"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_TEAL

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.8))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    add_background(s1)

    # Accent decorative banner
    banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.8))
    banner.fill.solid()
    banner.fill.fore_color.rgb = ACCENT_TEAL
    banner.line.fill.background()

    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "DAY 1 PROJECT BRIEFING"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_BLUE

    p1 = tf1.add_paragraph()
    p1.text = "Indian Mutual Fund Analytics\n& Live Ingestion Engine"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_before = Pt(10)
    p1.space_after = Pt(15)

    p2 = tf1.add_paragraph()
    p2.text = "Comprehensive Data Pipeline, Multi-Dataset Ingestion, AMFI Code Referential Integrity & mfapi.in Live Integration"
    p2.font.size = Pt(16)
    p2.font.color.rgb = TEXT_MUTED

    # Bottom pill / metadata
    meta_box = s1.shapes.add_textbox(Inches(1.2), Inches(5.8), Inches(11.0), Inches(0.8))
    tf_m = meta_box.text_frame
    pm = tf_m.paragraphs[0]
    pm.text = "Author: Bijoy Paul  |  Repository: github.com/Bijoy-paul-01/mutual-fund-analytics  |  Commit: Day 1: Data ingestion complete"
    pm.font.size = Pt(12)
    pm.font.color.rgb = ACCENT_TEAL

    # ==========================================
    # SLIDE 2: ARCHITECTURE & REPO STRUCTURE
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_background(s2)
    add_header(s2, "Production Folder Architecture & Git Foundation")

    # 3 Cards
    cards_data = [
        ("Directory Structure", "Modular standard for financial engineering:", [
            "data/raw/: Immutable CSVs & API responses",
            "data/processed/: Cleansed & transformed data",
            "notebooks/: Interactive Jupyter notebooks",
            "sql/: DDL schema definitions (schema.sql)",
            "dashboard/ & reports/: Visuals and quality audits"
        ], ACCENT_BLUE),
        ("Version Control", "GitHub repository established:", [
            "Repository: Bijoy-paul-01/mutual-fund-analytics",
            "Branch: main (configured with remote origin)",
            "Commit: 'Day 1: Data ingestion complete'",
            "Gitkeep tracking for scaffolded directories",
            "Comprehensive .gitignore for Python/Jupyter"
        ], ACCENT_TEAL),
        ("Dependencies", "requirements.txt installed & pinned:", [
            "pandas & numpy: High-performance dataframes",
            "matplotlib & seaborn: Statistical visual plotting",
            "plotly: Dynamic interactive financial charts",
            "sqlalchemy: Relational persistence layer",
            "requests: High-resilience REST API clients"
        ], ACCENT_GOLD)
    ]

    card_w = Inches(3.64)
    card_h = Inches(4.8)
    card_top = Inches(1.8)

    for i, (title, sub, bullets, acc_col) in enumerate(cards_data):
        left = Inches(0.8 + i * 4.0)
        c = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, card_top, card_w, card_h)
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        tb = s2.shapes.add_textbox(left + Inches(0.25), card_top + Inches(0.25), card_w - Inches(0.5), card_h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(18)
        p_t.font.bold = True
        p_t.font.color.rgb = acc_col

        p_s = tf.add_paragraph()
        p_s.text = sub
        p_s.font.size = Pt(12)
        p_s.font.color.rgb = TEXT_MUTED
        p_s.space_after = Pt(14)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = "• " + b
            pb.font.size = Pt(12)
            pb.font.color.rgb = TEXT_WHITE
            pb.space_after = Pt(8)

    # ==========================================
    # SLIDE 3: 10 CORE DATASETS CATALOG
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_background(s3)
    add_header(s3, "Comprehensive Ingestion of 10 Datasets")

    # Table
    rows = 11
    cols = 5
    t_left = Inches(0.8)
    t_top = Inches(1.7)
    t_w = Inches(11.7)
    t_h = Inches(5.1)

    table_shape = s3.shapes.add_table(rows, cols, t_left, t_top, t_w, t_h)
    tbl = table_shape.table

    # Column widths
    tbl.columns[0].width = Inches(0.7)
    tbl.columns[1].width = Inches(2.8)
    tbl.columns[2].width = Inches(1.8)
    tbl.columns[3].width = Inches(2.6)
    tbl.columns[4].width = Inches(3.8)

    headers = ["#", "Dataset Name", "Dimensions", "Primary Grain", "Domain Context"]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(13, 148, 136) # Teal
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    ds_rows = [
        ("1", "fund_master.csv", "40 × 15", "amfi_code", "Scheme metadata, TER, exit load, SEBI classification"),
        ("2", "nav_history.csv", "46,000 × 3", "amfi_code + date", "Daily continuous NAV series (1,150 days/fund)"),
        ("3", "aum_by_fund_house.csv", "90 × 5", "date + fund_house", "Quarterly AUM trends across top 10 AMCs"),
        ("4", "monthly_sip_inflows.csv", "48 × 6", "month", "Industry SIP inflows, active folios & AUM scale"),
        ("5", "category_inflows.csv", "144 × 3", "month + category", "Segmented monthly capital net inflows"),
        ("6", "industry_folio_count.csv", "21 × 6", "month", "Asset-class folio growth (Equity, Debt, Hybrid)"),
        ("7", "scheme_performance.csv", "40 × 19", "amfi_code", "Alpha, Beta, Sharpe, Sortino, Max Drawdown"),
        ("8", "investor_transactions.csv", "32,778 × 13", "investor_id + date", "Retail/HNI ticket sizes, tiers, payment, KYC"),
        ("9", "portfolio_holdings.csv", "322 × 8", "amfi_code + symbol", "Stock level allocations & sector concentration"),
        ("10", "benchmark_indices.csv", "8,050 × 3", "date + index_name", "Closing levels for NIFTY50, Midcap150, etc.")
    ]

    for i, row in enumerate(ds_rows, 1):
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if i % 2 == 0 else RGBColor(23, 37, 84)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_WHITE if j != 2 else ACCENT_BLUE

    # ==========================================
    # SLIDE 4: FUND MASTER & AMFI ARCHITECTURE
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_background(s4)
    add_header(s4, "Fund Master Architecture & AMFI Scheme Code Structure")

    # 4 metric boxes at top
    metrics = [
        ("10", "Top Fund Houses (AMCs)", "SBI, HDFC, ICICI, Nippon, Kotak, Axis..."),
        ("2", "Broad Asset Classes", "Equity (34 schemes) & Debt (6 schemes)"),
        ("12", "SEBI Sub-Categories", "Large Cap, Mid Cap, Small Cap, Liquid, Gilt..."),
        ("5", "Risk Grade Levels", "Low to Very High risk classification")
    ]
    for i, (val, title, desc) in enumerate(metrics):
        m_left = Inches(0.8 + i * 3.0)
        c = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, m_left, Inches(1.8), Inches(2.7), Inches(1.4))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        tb = s4.shapes.add_textbox(m_left + Inches(0.15), Inches(1.9), Inches(2.4), Inches(1.2))
        tf = tb.text_frame
        p_val = tf.paragraphs[0]
        p_val.text = val
        p_val.font.size = Pt(28)
        p_val.font.bold = True
        p_val.font.color.rgb = ACCENT_TEAL

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = TEXT_MUTED

    # Bottom comparison card
    b_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.6), Inches(11.7), Inches(3.2))
    b_card.fill.solid()
    b_card.fill.fore_color.rgb = CARD_BG
    b_card.line.color.rgb = CARD_BORDER

    tb_b = s4.shapes.add_textbox(Inches(1.1), Inches(3.8), Inches(11.1), Inches(2.8))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True

    p_bt = tf_b.paragraphs[0]
    p_bt.text = "AMFI Scheme Code Architecture & Direct vs. Regular Plan Spread"
    p_bt.font.size = Pt(16)
    p_bt.font.bold = True
    p_bt.font.color.rgb = ACCENT_BLUE

    points = [
        "6-Digit Unique Identifier: Every scheme is assigned a unique AMFI numeric code acting as the immutable relational primary key.",
        "Twin Plan Structure: Identical underlying portfolios operate with two distinct scheme codes: Regular Plan (broker/distributor channel) and Direct Plan (AMC direct).",
        "Expense Ratio Spread (TER Disparity): In our dataset, Regular Plans average 1.35% TER vs. Direct Plans at 0.78% TER — creating a 0.57% (57 bps) annual commission delta.",
        "SEBI Standard Codes: Full traceability to SEBI category definitions (EC01 for Large Cap, EC02 for Mid Cap, EC03 for Small Cap, DC01 for Liquid)."
    ]
    for pt in points:
        p = tf_b.add_paragraph()
        p.text = "✔  " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(8)

    # ==========================================
    # SLIDE 5: LIVE NAV FETCHING (mfapi.in)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_background(s5)
    add_header(s5, "Real-Time NAV Integration Engine (mfapi.in API)")

    # Left text card
    left_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(4.5), Inches(5.0))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = CARD_BORDER

    tb_l = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.1), Inches(4.6))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl_t = tf_l.paragraphs[0]
    pl_t.text = "live_nav_fetch.py Client"
    pl_t.font.size = Pt(18)
    pl_t.font.bold = True
    pl_t.font.color.rgb = ACCENT_TEAL

    pl_desc = [
        "Target API: https://api.mfapi.in/mf/<amfi_code>",
        "Primary Scheme: 125497 (HDFC Top 100 Direct / Direct Equity)",
        "Key Schemes: SBI Bluechip, ICICI Bluechip, Nippon Large Cap, Axis Bluechip, Kotak Bluechip",
        "Features:",
        "• Robust HTTP request handling with timeouts & retry logic",
        "• Parsing nested JSON metadata & daily NAV timeseries",
        "• Standardizing date format to YYYY-MM-DD",
        "• Outputting individual raw CSVs + combined summary CSV"
    ]
    for d in pl_desc:
        p = tf_l.add_paragraph()
        p.text = d
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_WHITE if "•" in d or ":" in d else TEXT_MUTED
        p.space_before = Pt(6)

    # Right table for fetched live NAVs
    rt_rows = 7
    rt_cols = 5
    r_table = s5.shapes.add_table(rt_rows, rt_cols, Inches(5.6), Inches(1.8), Inches(6.9), Inches(5.0))
    rt = r_table.table
    rt.columns[0].width = Inches(1.1)
    rt.columns[1].width = Inches(2.1)
    rt.columns[2].width = Inches(1.2)
    rt.columns[3].width = Inches(1.3)
    rt.columns[4].width = Inches(1.2)

    r_headers = ["Code", "Target Scheme", "Live Date", "Latest NAV", "Total Days"]
    for j, h in enumerate(r_headers):
        cell = rt.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(14, 116, 144)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    live_rows = [
        ("125497", "HDFC Top 100 Direct", "2026-10-12", "₹ 206.53", "3,183"),
        ("119551", "SBI Bluechip", "2026-10-12", "₹ 106.85", "3,327"),
        ("120503", "ICICI Bluechip", "2026-10-12", "₹ 105.09", "3,399"),
        ("118632", "Nippon Large Cap", "2026-10-12", "₹ 94.57", "3,390"),
        ("119092", "Axis Bluechip", "2026-10-12", "₹ 6,336.04", "3,656"),
        ("120841", "Kotak Bluechip", "2026-10-12", "₹ 240.19", "3,393")
    ]
    for i, row in enumerate(live_rows, 1):
        for j, val in enumerate(row):
            cell = rt.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = ACCENT_GOLD if j == 3 else TEXT_WHITE

    # ==========================================
    # SLIDE 6: DATA QUALITY AUDIT & ANOMALIES
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_background(s6)
    add_header(s6, "Data Quality Audit & Anomaly Detection Findings")

    findings = [
        ("1. Missing YoY Growth in SIP Inflows", "Context: 12 missing values in 'monthly_sip_inflows'", [
            "Months 2022-01 through 2022-12 show NaN for yoy_growth_pct.",
            "Root Cause: The dataset begins in Jan 2022; calculating 1-year YoY percentage requires 2021 base-year data.",
            "Action: Impute programmatically once rolling 12-month lag is established."
        ], ACCENT_GOLD),
        ("2. Negative Drawdowns in Performance", "Context: 40 schemes with negative max_drawdown_pct", [
            "Values range from -2.23% (low-risk Gilt) to -33.5% (high-beta equity).",
            "Root Cause: Drawdowns represent peak-to-trough drops; mathematical sign is natively negative.",
            "Action: Preserve negative sign for risk metrics or use abs() for reporting."
        ], ACCENT_BLUE),
        ("3. KYC Verification Status in Transactions", "Context: 2,632 transactions marked 'Pending'", [
            "30,146 verified transactions (91.97%) vs. 2,632 pending transactions (8.03%).",
            "Root Cause: Realistic simulation of investor onboarding lag.",
            "Action: Separate confirmed settled AUM from provisional transactions."
        ], ACCENT_TEAL)
    ]

    for i, (title, sub, bullets, acc_col) in enumerate(findings):
        top = Inches(1.8 + i * 1.7)
        c = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.5))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        tb = s6.shapes.add_textbox(Inches(1.0), top + Inches(0.1), Inches(11.3), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title + "  —  " + sub
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = acc_col

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = "• " + b
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_WHITE
            pb.space_before = Pt(2)

    # ==========================================
    # SLIDE 7: REFERENTIAL INTEGRITY VALIDATION
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_background(s7)
    add_header(s7, "AMFI Scheme Code Referential Integrity Validation")

    # Big Badge
    badge = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.6))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(6, 78, 59) # Emerald 900
    badge.line.color.rgb = RGBColor(16, 185, 129)

    tb_badge = s7.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(1.2))
    tf_badge = tb_badge.text_frame
    p_b1 = tf_badge.paragraphs[0]
    p_b1.text = "✔  REFERENTIAL INTEGRITY: 100% VALIDATED"
    p_b1.font.size = Pt(22)
    p_b1.font.bold = True
    p_b1.font.color.rgb = ACCENT_GREEN

    p_b2 = tf_badge.add_paragraph()
    p_b2.text = "Every single AMFI scheme code defined in fund_master (40/40) exists in nav_history with zero orphan records and zero omissions."
    p_b2.font.size = Pt(13)
    p_b2.font.color.rgb = TEXT_WHITE
    p_b2.space_before = Pt(6)

    # 3 validation boxes
    v_boxes = [
        ("40 / 40 Schemes", "Complete Alignment", "All 40 master scheme codes have complete continuous trading histories in nav_history.", ACCENT_TEAL),
        ("1,150 Records / Scheme", "Uniform Trading Depth", "Exactly 1,150 business days per scheme from 2022-01-03 to 2026-05-29 (46,000 total rows).", ACCENT_BLUE),
        ("0 Orphan Records", "Clean Foreign Keys", "Zero spurious AMFI codes in nav_history or transaction tables; 100% relational integrity.", ACCENT_GOLD)
    ]
    for i, (title, sub, desc, acc_col) in enumerate(v_boxes):
        left = Inches(0.8 + i * 4.0)
        c = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(3.7), Inches(3.64), Inches(2.9))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        tb = s7.shapes.add_textbox(left + Inches(0.2), Inches(3.9), Inches(3.24), Inches(2.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = acc_col

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(10)

    # ==========================================
    # SLIDE 8: DELIVERABLES & NEXT STEPS
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_background(s8)
    add_header(s8, "Day 1 Summary & Quantitative Roadmap")

    # Left Box - Deliverables Completed
    c_del = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9))
    c_del.fill.solid()
    c_del.fill.fore_color.rgb = CARD_BG
    c_del.line.color.rgb = CARD_BORDER

    tb_del = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.5))
    tf_del = tb_del.text_frame
    tf_del.word_wrap = True

    p_dt = tf_del.paragraphs[0]
    p_dt.text = "Day 1 Deliverables Completed"
    p_dt.font.size = Pt(18)
    p_dt.font.bold = True
    p_dt.font.color.rgb = ACCENT_GREEN

    d_items = [
        "data_ingestion.py: Automated loader, profiler & audit reporter",
        "live_nav_fetch.py: Live REST client querying mfapi.in API",
        "requirements.txt: Dependencies pinned & verified",
        "sql/schema.sql: 10 relational DDL tables defined",
        "reports/data_quality_summary.md: Formal markdown audit",
        "notebooks/01_data_ingestion_and_exploration.ipynb",
        "Git Commit & Push: 'Day 1: Data ingestion complete' on origin/main"
    ]
    for it in d_items:
        p = tf_del.add_paragraph()
        p.text = "✔  " + it
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(8)

    # Right Box - Next Steps (Day 2+)
    c_nxt = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.9))
    c_nxt.fill.solid()
    c_nxt.fill.fore_color.rgb = CARD_BG
    c_nxt.line.color.rgb = CARD_BORDER

    tb_nxt = s8.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.2), Inches(4.5))
    tf_nxt = tb_nxt.text_frame
    tf_nxt.word_wrap = True

    p_nt = tf_nxt.paragraphs[0]
    p_nt.text = "Upcoming Analytics Roadmap"
    p_nt.font.size = Pt(18)
    p_nt.font.bold = True
    p_nt.font.color.rgb = ACCENT_BLUE

    n_items = [
        "Feature Engineering: Calculate rolling Sharpe, Sortino, Treynor & Jensen's Alpha",
        "SIP Performance Modeling: Simulate recurring investments across market regimes",
        "Factor Attribution: Multi-factor regression vs. NIFTY50 & BSE SmallCap indices",
        "SQL Analytics: Write complex analytical queries for manager track-records",
        "Interactive Dashboard: Plotly / Streamlit frontend for fund comparison & screening"
    ]
    for it in n_items:
        p = tf_nxt.add_paragraph()
        p.text = "➔  " + it
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(10)

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out_file = r"C:\Users\bijoy\.gemini\antigravity\scratch\mutual-fund-analytics\reports\Day1_Mutual_Fund_Analytics.pptx"
    create_deck(out_file)
