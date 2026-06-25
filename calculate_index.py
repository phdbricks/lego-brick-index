#!/usr/bin/env python3
"""
LEGO Brick Index — Annual Calculator
=====================================
Reads a raw CSV with local prices and exchange rates,
calculates all USD-equivalent and index columns,
and overwrites the file with the full dataset.

Usage:
    python scripts/calculate_index.py data/lego-brick-index-2026.csv
"""

import csv
import sys
from pathlib import Path

# Sets included in the composite basket
SET_COLUMNS = [
    "local_price_76313_marvel",
    "local_price_75379_r2d2",
    "local_price_75375_falcon",
    "local_price_76314_civilwar",
    "local_price_60316_police",
    "local_price_60399_fire",
    "local_price_60314_truck",
]

SET_TO_DOLLAR_MAP = {
    "local_price_76313_marvel": "dollar_price_76313",
    "local_price_75379_r2d2":   "dollar_price_75379",
    "local_price_75375_falcon":  "dollar_price_75375",
    "local_price_76314_civilwar":"dollar_price_76314",
    "local_price_60316_police":  "dollar_price_60316",
    "local_price_60399_fire":    "dollar_price_60399",
    "local_price_60314_truck":   "dollar_price_60314",
}


def calculate(input_path: str) -> None:
    path = Path(input_path)
    if not path.exists():
        print(f"Error: file not found — {input_path}")
        sys.exit(1)

    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            rows.append(row)

    if not rows:
        print("Error: CSV is empty.")
        sys.exit(1)

    # Step 1: calculate dollar prices for each row
    for row in rows:
        ex_raw = row.get("dollar_ex", "")
        if not ex_raw or str(ex_raw).strip() == "":
            # no-data country — skip calculations
            for _, dollar_col in SET_TO_DOLLAR_MAP.items():
                row[dollar_col] = ""
            row["composite_index_raw"] = ""
            continue
        ex = float(ex_raw)
        dollar_prices = []
        for local_col, dollar_col in SET_TO_DOLLAR_MAP.items():
            local_val = row.get(local_col)
            if local_val and local_val.strip():
                dollar_val = round(float(local_val) / ex, 2)
                row[dollar_col] = dollar_val
                dollar_prices.append(dollar_val)
            else:
                row[dollar_col] = ""

        # Composite: mean of available dollar prices
        if dollar_prices:
            row["composite_index_raw"] = round(sum(dollar_prices) / len(dollar_prices), 2)
        else:
            row["composite_index_raw"] = ""

    # Step 2: find USA baseline
    usa_rows = [r for r in rows if r["iso_a3"] == "USA"]
    if not usa_rows:
        print("Error: No row with iso_a3 == 'USA' found. Cannot compute USD_raw_composite.")
        sys.exit(1)

    usa_composite = float(usa_rows[0]["composite_index_raw"])
    print(f"USA baseline composite: ${usa_composite:.2f}")

    # Step 3: compute USD_raw_composite for all rows
    for row in rows:
        comp = row.get("composite_index_raw")
        if comp:
            raw = round(((float(comp) / usa_composite) - 1) * 100, 2)
            row["USD_raw_composite"] = raw
        else:
            row["USD_raw_composite"] = ""

    # Step 4: write back
    # Ensure all new dollar_price columns are in fieldnames
    new_fields = list(SET_TO_DOLLAR_MAP.values()) + ["composite_index_raw", "USD_raw_composite"]
    full_fields = list(fieldnames)
    for f in new_fields:
        if f not in full_fields:
            full_fields.append(f)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=full_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Updated {len(rows)} rows in {path}")
    print("\nTop 5 most expensive:")
    sorted_rows = sorted(rows, key=lambda r: float(r["USD_raw_composite"]) if r["USD_raw_composite"] else -999, reverse=True)
    for r in sorted_rows[:5]:
        print(f"  {r['country']:20s}  {float(r['USD_raw_composite']):+.1f}%  (${float(r['composite_index_raw']):.2f})")

    print("\nTop 5 cheapest:")
    for r in sorted_rows[-5:]:
        if r["USD_raw_composite"] == "":
            continue
        print(f"  {r['country']:20s}  {float(r['USD_raw_composite']):+.1f}%  (${float(r['composite_index_raw']):.2f})")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/calculate_index.py <path-to-csv>")
        sys.exit(1)
    calculate(sys.argv[1])
