# Starlink Aviation — Account Attainment & Revenue Intelligence

A data engineering and business intelligence project modeling Starlink Aviation's fleet attainment gap, revenue opportunity, and account-level risk across 8 major airline partners. Built from real FAA registry data, publicly sourced contract information, a six-script Python pipeline, and a Tableau dashboard.

**[View the Live Dashboard](https://public.tableau.com/app/profile/prajwal.hendre/viz/Book1_17533820297810/Dashboard1)**

---

## The Business Question

Starlink Aviation has signed contracts with some of the world's largest airlines. However, a signed contract is not revenue. Revenue only starts when a plane has physically installed Starlink hardware, has a valid FAA Supplemental Type Certificate, and actively billing monthly service fees. 

This project asks: **across Starlink's major airline partners, how much of the contracted revenue potential is actually being captured today, and where are the biggest gaps, risks, and opportunities?**

The answer matters because every unactivated tail number is a direct monthly revenue loss. At $12,500–$25,000 per plane per month, the gap between contracted and active aircraft represents hundreds of millions in uncaptured annual recurring revenue.

---

## Key Numbers

- **$841,200,000 potential ARR (Annual Recurring Revenue)** across 7 confirmed contracted partners and one prospective partner (American Airlines). This number represents the revenue ceiling if every contracted aircraft were fully active today.

- **$10,420,000 current MRR (Monthly Recurring Revenue)** is what is estimated to be billed today, based on per-airline attainment rates sourced from public announcements.

- **$59,680,000 monthly revenue gap** is the difference between potential and current MRR. This is revenue that is left on the table every month (see STC Bottleneck section below for why).

- **$162,000,000 prospective ARR** American Airlines is actively evaluating Starlink with a decision expected in the coming weeks. If signed, it would be one of the largest single airline contract in Starlink Aviation history, however, they are also in talks with Amazon Leo.

- **Qatar Airways: 100% attainment** The only account in the portfolio at full deployment. Every contracted plane is active and billing.

- **Southwest Airlines and Lufthansa Group: 0% attainment** Combined potential ARR of $466,350,000, with installations not yet begun. This is the next major wave of revenue coming online in 2026-2027.

---

## Methodology & Key Modeling Decisions

**Per-airline attainment rates instead of a global average**

Early estimates of Starlinks attainment rates were published at 9.3% (September 2024) applied uniformly across all airlines. Since that figure was published, this project has estimated the uniform rate with per-airline attainment rates sourced directly from public press releases and airline announcements (April 2026):

| Airline | Active Aircraft | Contracted Fleet | Attainment Rate | Source |
|---|---|---|---|---|
| United Airlines | ~300 | 1,000 | 30% | Feb 2026 press release |
| Qatar Airways | 120 | 120 | 100% | Jan 2026 announcement |
| Emirates | ~70 | 232 | 30% | 14/month since Nov 2025 |
| Alaska Air Group | ~50 | 400 | 12.5% | Hawaiian fleet active |
| IAG | ~2 | 500 | 0.4% | BA first flight Mar 2026 |
| Southwest Airlines | 0 | 300 | 0% | Starts summer 2026 |
| Lufthansa Group | 0 | 850 | 0% | Starts H2 2026 |
| American Airlines | 0 | 900 | 0% | No contract signed yet |

**Alaska Air Group**

Alaska Airlines acquired Hawaiian Airlines in September 2024. Hawaiian's final flight as an independent carrier was October 29, 2025, after which operations were integrated under Alaska Airlines' air operator certificate. I've treated them as a single account (Alaska Air Group) with a combined contracted fleet of 400 planes. Hawaiian's ~50-plane Airbus fleet represents the active installed base, while Alaska's own Starlink rollout begins in 2026. Note: FAA fleet counts reflect Alaska Airlines registrations only. Hawaiian's aircraft remain registered separately pending full FAA integration.

**Qatar Airways**

Qatar's contracted Starlink fleet of 120 planes covers their Boeing 777s, Airbus A350s, and Boeing 787s. Their total widebody fleet is approximately 207 aircraft. The remaining planes are A380s which Qatar has not committed to Starlink. Therefore, when various press releases have described Qatar's Starlink implementation rate as 58%, this is in direct relation to 120 out of 207 total widebody aircraft. Against their contracted fleet of 120, Qatar is at 100% attainment. In other words, every plane they committed to Starlink is active and billing. Looking forward, the uncontracted A380 fleet represents a significant expansion opportunity.

---

## Why the Gap Exists: The STC Bottleneck

The primary reason revenue is not being generated across accounts is the FAA Supplemental Type Certificate (STC). Before Starlink hardware can be installed on any aircraft, the FAA must certify the installation is safe for that specific aircraft model. This process takes 8–18 months and must be completed separately for every aircraft type in an airline's fleet.

For example, United Airlines operates 16+ distinct aircraft models, each requiring its own STC. As of this writing, United has STCs approved for the Embraer 175 and Boeing 737-800, with remaining models in progress. Southwest and Lufthansa have no approved STCs yet as their contracts were announced in 2026. This highlights the underlying issue: the revenue gap is not a sales problem but rather a regulatory pipeline problem.

---

## Competitive Landscape

**Delta Air Lines**

Recently, Delta Air Lines selected Amazon's Project Leo (now Amazon Leo) as its in-flight connectivity provider in early April 2026. Delta looks to equip 500 aircraft beginning in 2028. This makes Delta the only major U.S. carrier to choose a Starlink alternative, and removes $138,600,000 in potential ARR from Starlink's addressable market. Delta is excluded from this model as a result.

**American Airlines**

American Airlines is actively evaluating both Starlink and Amazon Leo, with a decision expected within weeks as of April 2026. If American signs with Starlink, it would potentially add $162,000,000 in potential ARR and represent the largest single airline contract in Starlink Aviation history. American is modeled as a prospective account with 0% current attainment and flagged as Competitive Risk.

**The broader competitive picture**

Delta's decision to choose Amazon Leo highlights a shifting landscape and threat to Starlink in the aviation connectivity market for the first time. Amazon Leo is not yet operational (its satellite network is still being built with commercial service expected in 2028) but its backing and Delta's endorsement signals that Starlink's dominance in commercial aviation is not guaranteed.

---

## Data Sources

**FAA Aircraft Registry**: `https://registry.faa.gov/database/ReleasableAircraft.zip`

Complete database of all US-registered civil aircraft, updated regularly by the FAA. Each row represents one physical aircraft identified by its N-number (tail number). This project downloads and parses the full registry, filtering to 8 target airlines and excluding false positives like training subsidiaries.

Data quality challenge: the FAA registers aircraft under full legal entity names with suffixes (UNITED AIRLINES INC, BRITISH AIRWAYS PLC) while contract data uses commercial names. A direct join will fail here. The solution I implemented was fuzzy string match using `str.contains()`. This checks whether the FAA name contains the contract name as a substring.

International airlines register their aircraft with their own national aviation authorities, not the FAA. Emirates, Qatar Airways, Lufthansa, and IAG show zero FAA-registered aircraft. This is not because they have no planes, but because those planes are registered in the UAE, Qatar, Germany, and the UK. I still wanted to modeled this explicitly rather omit it.

**Contracts Table** 

There's no public API for Starlink contract data. I built this table from airline press releases, investor announcements, and industry reporting. Each row includes contracted fleet size, monthly service rate, STC status, contract year, and an `faa_name` alias field mapping the business entity name to how it appears in FAA data. For instance, Starlink's contract is with International Airlines Group, but the planes are registered to British Airways.

---

## The Python Pipeline

I created 6 scripts to fetch and model data.

| Script | What It Does |
|---|---|
| `01_fetch_faa_data.py` | Downloads FAA registry ZIP, parses MASTER.txt, filters to target airlines, saves `faa_filtered.csv` |
| `02_build_contracts.py` | Builds contracts table from curated press release data, includes `faa_name` alias column |
| `03_attainment_model.py` | Fuzzy-matches FAA data to contracts using `str.contains()`, merges tables, saves `attainment.csv` |
| `04_revenue_model.py` | Calculates current MRR, potential MRR, revenue gap, and potential ARR per airline |
| `05_risk_flags.py` | Applies four-tier risk classification (Critical / High / Medium / Competitive Risk) using `numpy.where()` |
| `06_export_tableau.py` | Exports all final tables to `tableau/` folder for Tableau import |

### Key Technical Decisions

**Fuzzy matching over direct join**: FAA legal suffixes (Inc, PLC, Co) broke my exact joins. I used `str.contains()` to handle all suffix variants in one pass.

**`faa_name` alias column**: decouples the business entity name from the FAA lookup key. Allows the pipeline to correctly attribute British Airways tail numbers to the IAG contract without renaming either source.

**Per-airline attainment rates**: I replaced the outdated uniform 9.3% global rate with account-specific rates sourced from public announcements to paint a more accurate picture of current revenue and the gap at each account.

**Four-tier risk classification**:
- **Critical**: STC Pending, revenue gap >$10M/month
- **High**: STC Pending or revenue gap >$5M/month  
- **Competitive Risk**: Prospective account where Starlink is competing 
for the contract against Amazon Leo
- **Medium**: All other confirmed contracted accounts

---

## The Dashboard

I built my dashboard in Tableau.

**Revenue Gap**: Bar chart sorted by monthly revenue gap, colored by risk tier. Lufthansa Group leads at $14.45M/month followed by American Airlines at $13.5M/month (Competitive Risk) and United at $11.55M/month. Qatar Airways shows $0 gap because it's the only fully deployed account in the portfolio.

**Attainment Rate**: Bar chart showing per-airline Starlink activation rate sourced from public announcements as of April 2026. Qatar Airways is the benchmark at 100%. United and Emirates are mid-deployment at 30%. Southwest, Lufthansa, and American are at 0%, representing the next wave of revenue coming online in 2026-2027.

**Fleet Deployment**: Stacked bar showing active aircraft (cyan) versus remaining undeployed aircraft (navy) per airline. United has the largest absolute deployment gap at 700 planes remaining. Lufthansa Group follows at 850 planes not yet started.

**Risk Dashboard**: Heatmap grid with airlines on rows, risk tiers on columns, and revenue gap as the value. There are four tiers: Critical (red), High (orange), Medium (blue), Competitive Risk (purple). American Airlines is the only Competitive Risk account (a live deal being contested against Amazon Leo).

**Global Footprint**: Potential ARR by region. Europe dominates with Lufthansa Group and IAG. North America carries the largest competitive risk with American undecided and Southwest pre-deployment. Middle East accounts are the most advanced in activation.

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
