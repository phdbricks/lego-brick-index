# 🧱 The LEGO Brick Index

> A Big Mac Index–style purchasing power comparison using LEGO sets sold globally.

Inspired by *The Economist's* [Big Mac Index](https://github.com/TheEconomist/big-mac-data), this project tracks the official retail price of identical LEGO sets across countries to reveal currency misalignment and purchasing power disparities worldwide.

**[→ View the live index](https://yourusername.github.io/lego-brick-index)**

---

## Why LEGO?

Like the Big Mac, LEGO sets are:
- **Identical worldwide** — same pieces, same IP licensing, same box
- **Sold in official stores** across 40+ countries with transparent pricing
- **Produced in a single country** (Denmark/China) but priced locally
- **Price-stable** — sets don't change price mid-cycle, making annual snapshots reliable

Where the Big Mac index uses one product, this index uses **9 flagship sets** across 3 themes — Marvel, Star Wars, and City — to build a more robust composite basket.

---

## The Sets

### 🔴 Marvel
| Set | Number | Pieces | USD RRP |
|-----|--------|--------|---------|
| MARVEL Logo & Minifigures | 76313 | 931 | $99.99 |
| Captain America: Civil War Battle | 76314 | 759 | $99.99 |

### ⭐ Star Wars
| Set | Number | Pieces | USD RRP |
|-----|--------|--------|---------|
| R2-D2 | 75379 | 1,050 | $99.99 |
| Millennium Falcon (Midi-Scale) | 75375 | 921 | $84.99 |

### 🏙️ City
| Set | Number | Pieces | USD RRP |
|-----|--------|--------|---------|
| Police Station | 60316 | 668 | $69.99 |
| Fire Station | 60399 | 843 | $79.99 |
| Ice Cream Truck | 60314 | 327 | $49.99 |

**Selection criteria:** Sets must be available in the official LEGO online store for at least 20 of the tracked countries simultaneously. Sets are replaced when retired (usually every 2–3 years).

---

## Methodology

### Raw Index
For each country and set, we calculate the **USD-equivalent price**:

```
dollar_price = local_price / exchange_rate
```

A **composite score** is then the simple average across all 7 sets:

```
composite = mean(dollar_price_set1, ..., dollar_price_setN)
```

The **raw index** for each country is:

```
USD_raw = ((composite / composite_USA) - 1) × 100
```

A positive value means the country is **more expensive** than the US in USD terms. A negative value means it is **cheaper**.

### What this tells us
- If a country's currency is **overvalued**, LEGO will appear expensive relative to the US (high positive index)
- If a currency is **undervalued**, LEGO will appear cheap (negative index)
- Unlike a single set, the **composite basket** smooths out theme-specific pricing decisions by LEGO

### What this does NOT tell us
- LEGO does not sell in many markets (Argentina, Pakistan, Nigeria) — those are absent
- Import taxes and local VAT are baked into official prices and not removed
- Exchange rates fluctuate; we use the rate at time of data collection (January each year)

---

## Data

### Files
```
data/
  lego-brick-index-YYYY.csv   # Annual snapshot, one row per country
  codebook.csv                 # Variable definitions
```

### Codebook summary

| Variable | Description |
|---|---|
| `date` | Observation date |
| `iso_a3` | ISO 3166-1 country code |
| `currency_code` | ISO 4217 currency code |
| `local_price_XXXXX` | Official price in local currency |
| `dollar_ex` | Local units per USD |
| `dollar_price_XXXXX` | USD-equivalent price |
| `composite_index_raw` | Avg USD price across basket |
| `USD_raw_composite` | % over/under vs United States |

Full definitions: [`data/codebook.csv`](data/codebook.csv)

---

## How to Update (Annual Process)

Every January, follow these steps:

### 1. Check set availability
Visit the official LEGO store for each country and verify all 7 sets are still listed. If a set has been retired, open an issue and propose a replacement following the selection criteria above.

```
https://www.lego.com/en-{country-code}/product/{set-number}
```

### 2. Collect prices
For each country, record the **official RRP** (not sale prices) in local currency. Sources in order of priority:
1. Official LEGO store: `lego.com/en-{code}`
2. Brickset.com (shows multi-country pricing)
3. Newelementary.com (publishes full country price lists on set reveals)

### 3. Get exchange rates
Use the **IMF annual average** exchange rate for the year just ended, or `xe.com` rate on January 1st of the new year.

### 4. Create new CSV
Copy last year's file:
```bash
cp data/lego-brick-index-2025.csv data/lego-brick-index-2026.csv
```
Update the `date` column and all price/exchange columns.

### 5. Recalculate derived columns
The `dollar_price_*` and index columns must be recalculated. A helper script is provided:

```bash
python scripts/calculate_index.py data/lego-brick-index-2026.csv
```

### 6. Update the website
The `docs/index.html` file reads from the CSV at page load. Just commit and push — GitHub Pages will update automatically.

---

## Running Locally

No build step needed. Open `docs/index.html` directly in a browser, or serve with:

```bash
python -m http.server 8000
# then open http://localhost:8000/docs/
```

---

## Contributing

Pull requests welcome for:
- **New countries** with official LEGO store presence
- **Data corrections** (wrong prices, wrong exchange rates)
- **Set replacements** when tracked sets retire
- **Visualisation improvements**

Please open an issue before large changes.

---

## License

Data: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
Code: [MIT](LICENSE)

If you use this data, please credit: **LEGO Brick Index** and link to this repository.

LEGO® is a trademark of the LEGO Group. This project is not affiliated with or endorsed by the LEGO Group.

---

## Acknowledgements

- Inspired by [The Economist's Big Mac Index](https://github.com/TheEconomist/big-mac-data)
- Price data from [LEGO official stores](https://www.lego.com) and [Brickset](https://brickset.com)
- Exchange rates from [IMF World Economic Outlook](https://www.imf.org/en/Publications/WEO)
