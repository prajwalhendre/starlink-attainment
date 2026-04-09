import os
import pandas as pd

#base dir of the file where we can find grandparent file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#assigning the finished script to /starlink_attainment/data/manual loc
MANUAL_DIR = os.path.join(BASE_DIR, "data", "manual")

#making directories
os.makedirs(MANUAL_DIR, exist_ok = True)

#data needs to be static because sourced from news reports and press releases
# i got attainment_rate from public announcements (april 2026)
# United: 300 active/1000 contracted (Feb 2026 press release)
# Qatar: 120/120 complete (Jan 2026 announcement, they have not fully committed to their widebody (whole) fleet but rather just 777s, A350s, and 787s (not A380s)
# Emirates: ~70/232 at 14/month since Nov 2025
# Alaska Air Group: ~50 active (Hawaiian fleet)/400 contracted
# IAG: 2 active/500 (BA first flight March 19 2026)
# Southwest, Lufthansa, American (potential): 0 active, installations not yet begun
def build_contracts():
    data = {
        "airline_name" : ['United Airlines', 'American Airlines', 'Southwest Airlines', 'Alaska Air Group', 'Qatar Airways', 'Emirates', 'Lufthansa Group', 'International Airlines Group'],
        "faa_name" : ['United Airlines', 'American Airlines', 'Southwest Airlines', 'Alaska Airlines', 'Qatar Airways', 'Emirates', 'Lufthansa', 'British Airways'],
        "region" : ['North America', 'North America', 'North America', 'North America', 'Middle East', 'Middle East', 'Europe', 'Europe'],
        "contracted_fleet" : [1000, 900, 300, 400, 120, 232, 850, 500],
        "monthly_rate_usd" : [16500, 15000, 12500, 14000, 25000, 25000, 17000, 15000],
        "stc_status" : ['Partial', 'Prospective', 'Pending', 'Partial', 'Partial', 'Partial', 'Pending', 'Partial'],
        "contract_year": [2024, 2024, 2026, 2024, 2024, 2025, 2026, 2025],
        "attainment_rate" : [0.30, 0.00, 0.00, 0.125, 1.00, 0.30, 0.00, 0.004]
    }


    df = pd.DataFrame(data)
    output_path = os.path.join(MANUAL_DIR, "contracts.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} airlines to {output_path}")
    return df 

if __name__ == '__main__':
    build_contracts()
    