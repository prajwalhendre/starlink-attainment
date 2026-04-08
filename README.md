# Starlink Aviation — Account Attainment & Revenue Intelligence

A data engineering and business intelligence project modeling Starlink Aviation's fleet attainment gap, revenue opportunity, and account-level risk across 9 major airline partners. Built from real FAA registry data, publicly sourced contract information, a six-script Python pipeline, and a Tableau dashboard.

**[View the Live Dashboard](https://public.tableau.com/app/profile/prajwal.hendre/viz/Book1_17533820297810/Dashboard1)**

---

## The Business Problem

Starlink Aviation is at approximately 9.3% global attainment. Out of every 100 aircraft contracted to receive Starlink connectivity, fewer than 10 are active and billing monthly service revenue. The gap between contracted and active aircraft represents an untapped revenue opportunity.

**Key numbers this project surfaces:**

- **$691,350,000 theoretical maximum ARR**: A bottom-up model calculated as `contracted_fleet × monthly_rate_usd × 12` per airline, using contracted fleet sizes from public press releases and rates from Starlink's published aviation
pricing. This represents the revenue ceiling if 100% of contracted aircraft were active (which they are not).

- **$52,254,538 monthly revenue gap**: The difference between that ceiling and current estimated MRR, modeled at 9.3% attainment (Starlink's publicly reported global activation rate). This is the revenue sitting uncaptured every month.

- **American Airlines: $12.2M/month gap. Delta: $10.5M/month gap**: The two largest gaps in the portfolio, both flagged Critical because their STC status is fully Pending with no approved aircraft models yet.

- **~18% attainment needed to reach $100M MRR** Back-calculated from the same model. At current contracted fleet sizes and blended rates, that requires activating roughly double the current global rate.

---

## Why the Gap Exists: The STC Bottleneck

The primary activation blocker is the FAA Supplemental Type Certificate (STC). Before Starlink hardware can be installed on any aircraft, the FAA must certify the installation is safe for that specific aircraft model. This process takes 8–18 months and must be completed separately for every aircraft type in an airline's fleet.

United Airlines operates 16+ distinct aircraft models, each requiring its own STC. As of this writing, United has STCs approved for the Embraer 175 and Boeing 737-800, with remaining models in progress. Every other airline in this dataset has all STCs pending, with the exception of Hawaiian Airlines (now part of Alaska Air Group). Hawaiian Airlines completed Starlink installation across its entire Airbus fleet and was the first major carrier to deploy Starlink commercially. The other airlines, however, highlight the underlying issue that the revenue gap is not a sales problem but rather a regulatory pipeline problem.

---

## Data Sources

**FAA Aircraft Registry**: `https://registry.faa.gov/database/ReleasableAircraft.zip`

Complete database of all US-registered civil aircraft, updated regularly by the FAA. Each row represents one physical aircraft identified by its N-number (tail number). This project downloads and parses the full registry, filtering to 9 target airlines and excluding false positives like training subsidiaries.

Data quality challenge: the FAA registers aircraft under full legal entity names with suffixes (UNITED AIRLINES INC, BRITISH AIRWAYS PLC) while contract data uses commercial names. A direct join will fail here. The solution I implemented was fuzzy string match using `str.contains()`. This checks whether the FAA name contains the contract name as a substring.

International airlines register their aircraft with their own national aviation authorities, not the FAA. Emirates, Qatar Airways, Lufthansa, and IAG show zero FAA-registered aircraft. This is not because they have no planes, but because those planes are registered in the UAE, Qatar, Germany, and the UK. I still wanted to modeled this explicitly rather omit it.

**Contracts Table** (manually curated from public press releases)

No public API exists for Starlink contract data. This table was built from airline press releases, investor announcements, and industry reporting. Each row includes contracted fleet size, monthly service rate, STC status, contract year, and an `faa_name` alias field mapping the business entity name to how it appears in FAA data. IAG is the clearest example (the contract is with International Airlines Group, but the planes are registered to British Airways).

---

## The Python Pipeline

I created 6 scripts to fetch and model data.

| Script | What It Does |
|---|---|
| `01_fetch_faa_data.py` | Downloads FAA registry ZIP, parses MASTER.txt, filters to target airlines, saves `faa_filtered.csv` |
| `02_build_contracts.py` | Builds contracts table from curated press release data, includes `faa_name` alias column |
| `03_attainment_model.py` | Fuzzy-matches FAA data to contracts using `str.contains()`, merges tables, saves `attainment.csv` |
| `04_revenue_model.py` | Calculates current MRR, potential MRR, revenue gap, and potential ARR per airline |
| `05_risk_flags.py` | Applies three-tier risk classification (Critical / High / Medium) using `numpy.where()` |
| `06_export_tableau.py` | Exports all final tables to `tableau/` folder for Tableau import |

### Key Technical Decisions

**Fuzzy matching over direct join**: FAA legal suffixes (Inc, PLC, Co) break exact joins. `str.contains()` checks whether the FAA name includes the contract name as a substring, handling all suffix variants in one pass.

**`faa_name` alias column**: decouples the business entity name from the FAA lookup key. Allows the pipeline to correctly attribute British Airways tail numbers to the IAG contract without renaming either source.

---

## The Dashboard

I built my dashboard in Tableau.

**Revenue Gap**: Bar chart sorted by monthly revenue gap, colored by risk tier, with a reference line at $8,333,333 (the monthly equivalent of $100M ARR). American and Delta sit significantly above the target line.

**Fleet Overview**: Stacked bar showing contracted fleet versus FAA-registered fleet. International carriers collapse to near-zero on the FAA axis, making the data source limitation explicit.

**Attainment %**: Calculated field `[Faa Fleet] / [Contracted Fleet]` per airline. United Airlines appears at ~390% because its FAA fleet (1,187 planes) is nearly four times its contracted Starlink fleet (300 planes) — illustrating significant account expansion opportunity. A 9.3% global attainment reference line provides the benchmark.

**Risk Dashboard**: Heatmap grid with airlines on rows, risk tiers on columns, and revenue gap as color intensity.

**Global Footprint**: Potential ARR by region. North America dominates with the Critical accounts. Europe and the Middle East are High-tier with meaningful revenue potential but no FAA validation data.

---

## How to Run
```bash
# Clone the repo
git clone https://github.com/prajwalhendre/starlink-attainment
cd starlink-attainment

# Install dependencies
pip install pandas numpy requests

# Run scripts in order
python scripts/01_fetch_faa_data.py
python scripts/02_build_contracts.py
python scripts/03_attainment_model.py
python scripts/04_revenue_model.py
python scripts/05_risk_flags.py
python scripts/06_export_tableau.py
```

Script 01 downloads ~50MB from the FAA server and may take 30–60 seconds. All other scripts run in under a second.

---

## Project Structure
```
starlink_attainment/
├── data/
│   ├── manual/           ← contracts.csv (curated from press releases)
│   └── processed/        ← intermediate CSVs (gitignored)
├── scripts/
│   ├── 01_fetch_faa_data.py
│   ├── 02_build_contracts.py
│   ├── 03_attainment_model.py
│   ├── 04_revenue_model.py
│   ├── 05_risk_flags.py
│   └── 06_export_tableau.py
├── tableau/              ← Tableau-ready CSVs
│   ├── attainment.csv
│   ├── revenue_model.csv
│   └── risk_classification.csv
└── README.md
```

---

## Tech Stack

Python 3 (pandas, numpy, requests) · Tableau Public · FAA Aircraft Registry · Public airline press releases

---

*Prajwal Hendre · April 2026*
