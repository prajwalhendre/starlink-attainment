import os
import pandas as pd

#base dir of the file where we can find grandparent file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#assigning the finished script to /starlink_attainment/data/manual loc
MANUAL_DIR = os.path.join(BASE_DIR, "data", "manual")

#making directories
os.makedirs(MANUAL_DIR, exist_ok = True)

#data needs to be static because sourced from news reports and press releases
def build_contracts():
    data = {
        "airline_name" : ['United Airlines', 'Delta Air Lines', 'American Airlines', 'Southwest Airlines', 'Alaska Airlines', 'Hawaiian Airlines', 'Qatar Airways', 'Emirates', 'Lufthansa', 'International Airlines Group'],
        "faa_name" : ['United Airlines', 'Delta Air Lines', 'American Airlines', 'Southwest Airlines', 'Alaska Airlines', 'Hawaiian Airlines', 'Qatar Airways', 'Emirates', 'Lufthansa', 'British Airways'],
        "region" : ['North America', 'North America', 'North America', 'North America', 'North America', 'North America', 'Middle East', 'Middle East', 'Europe', 'Europe'],
        "contracted_fleet" : [300, 700, 900, 817, 200, 50, 100, 100, 300, 300],
        "monthly_rate_usd" : [16500, 16500, 15000, 12500, 14000, 14000, 25000, 25000, 17000, 15000],
        "stc_status" : ['Partial', 'Pending', 'Pending', 'Pending', 'Pending', 'Pending', 'Pending', 'Pending', 'Pending', 'Pending'], 
        "contract_year": [2024, 2024, 2024, 2024, 2024, 2023, 2023, 2023, 2023, 2023]
    }

    df = pd.DataFrame(data)
    output_path = os.path.join(MANUAL_DIR, "contracts.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} airlines to {output_path}")
    return df 

if __name__ == '__main__':
    build_contracts()
    