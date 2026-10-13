#!/usr/bin/env python3
"""
live_nav_fetch.py
-----------------
Fetches live & historical Net Asset Value (NAV) data from mfapi.in API
for specified AMFI mutual fund scheme codes, parses the JSON payload,
and stores the output as raw CSV files.

Target Schemes:
- 125497: HDFC Top 100 Direct (Dataset reference code)
- 119551: SBI Bluechip Fund
- 120503: ICICI Pru Bluechip Fund
- 118632: Nippon India Large Cap Fund
- 119092: Axis Bluechip Fund
- 120841: Kotak Bluechip Fund
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional
import requests
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Base API URL
MFAPI_BASE_URL = "https://api.mfapi.in/mf"

# Key Schemes Dictionary
KEY_SCHEMES = {
    125497: "HDFC Top 100 Direct / Direct Equity",
    119551: "SBI Bluechip Fund",
    120503: "ICICI Bluechip Fund",
    118632: "Nippon Large Cap Fund",
    119092: "Axis Bluechip Fund",
    120841: "Kotak Bluechip Fund",
}


def fetch_scheme_nav(amfi_code: int, timeout: int = 15) -> Optional[Dict[str, Any]]:
    """
    Fetch scheme metadata and NAV history from mfapi.in by AMFI code.
    """
    url = f"{MFAPI_BASE_URL}/{amfi_code}"
    logger.info(f"Fetching NAV data from: {url}")
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        if not data or "data" not in data:
            logger.warning(f"No NAV series returned for code {amfi_code}")
            return None
        return data
    except requests.RequestException as e:
        logger.error(f"Failed to fetch NAV for AMFI code {amfi_code}: {e}")
        return None


def parse_and_save_scheme(
    data: Dict[str, Any],
    output_dir: str,
    prefix: str = "live_nav"
) -> Optional[pd.DataFrame]:
    """
    Parse JSON response from mfapi.in and save historical NAV records as CSV.
    """
    meta = data.get("meta", {})
    records = data.get("data", [])
    amfi_code = meta.get("scheme_code")
    scheme_name = meta.get("scheme_name", "Unknown Scheme")

    if not records:
        logger.warning(f"No records to save for scheme {amfi_code}")
        return None

    df = pd.DataFrame(records)
    # Expected columns in mfapi: date (DD-MM-YYYY), nav (string/float)
    df["amfi_code"] = amfi_code
    df["scheme_name"] = scheme_name
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

    # Standardize date format to YYYY-MM-DD
    df["date_raw"] = df["date"]
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce").dt.strftime("%Y-%m-%d")

    # Reorder columns
    cols = ["amfi_code", "scheme_name", "date", "nav", "date_raw"]
    df = df[cols]

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{prefix}_{amfi_code}.csv"
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    logger.info(f"Saved {len(df)} records for {scheme_name} (Code: {amfi_code}) to: {filepath}")

    return df


def fetch_all_key_schemes(output_dir: str = "data/raw") -> Dict[str, Any]:
    """
    Fetch live NAV for HDFC Top 100 Direct (125497) and the 5 key schemes.
    Saves individual CSVs and an aggregated summary CSV.
    """
    results = {}
    summary_rows = []
    all_nav_dfs = []

    print("\n" + "=" * 70)
    print("FETCHING LIVE NAV FROM MFAPI.IN")
    print("=" * 70)

    for code, label in KEY_SCHEMES.items():
        print(f"\n--> Fetching AMFI Code: {code} ({label})...")
        payload = fetch_scheme_nav(code)
        if payload:
            df = parse_and_save_scheme(payload, output_dir=output_dir)
            if df is not None and not df.empty:
                latest = df.iloc[0]
                prev = df.iloc[1] if len(df) > 1 else latest
                net_chg = round(float(latest["nav"]) - float(prev["nav"]), 4)
                pct_chg = round((net_chg / float(prev["nav"])) * 100, 2) if float(prev["nav"]) != 0 else 0.0

                summary_rows.append({
                    "amfi_code": code,
                    "target_scheme": label,
                    "api_scheme_name": payload.get("meta", {}).get("scheme_name"),
                    "fund_house": payload.get("meta", {}).get("fund_house"),
                    "latest_date": latest["date"],
                    "latest_nav": latest["nav"],
                    "prev_nav": prev["nav"],
                    "net_change": net_chg,
                    "pct_change": pct_chg,
                    "total_historical_records": len(df)
                })
                all_nav_dfs.append(df)
                results[code] = {"status": "SUCCESS", "records": len(df), "latest_nav": latest["nav"]}
        else:
            results[code] = {"status": "FAILED"}

    summary_df = pd.DataFrame(summary_rows)
    summary_path = os.path.join(output_dir, "live_nav_key_schemes_summary.csv")
    summary_df.to_csv(summary_path, index=False)

    print("\n" + "=" * 70)
    print("LIVE NAV SUMMARY TABLE")
    print("=" * 70)
    print(summary_df[["amfi_code", "target_scheme", "latest_date", "latest_nav", "pct_change", "total_historical_records"]].to_string(index=False))
    print(f"\nSummary successfully saved to: {summary_path}")

    return {
        "results": results,
        "summary": summary_df
    }


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_dir = os.path.join(base_dir, "data", "raw")
    fetch_all_key_schemes(output_dir=raw_dir)
