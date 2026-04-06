import pandas as pd
import os

#using dir for repeatability later down the line
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONTRACTS_DIR = os.path.join(BASE_DIR, 'data', 'manual')

FAA_DIR = os.path.join(BASE_DIR, 'data', 'processed')



def merge_faa_and_contracts():
    #same master path to join paths for repeatability
    contracts_master_path = os.path.join(CONTRACTS_DIR, 'contracts.csv')
    faa_master_path = os.path.join(FAA_DIR, 'faa_filtered.csv')
    #ingesting script 1 and 2 data
    contracts_data = pd.read_csv(contracts_master_path, dtype = str, low_memory=False)
    faa_data = pd.read_csv(faa_master_path, dtype=str, low_memory = False)

    #grouping faa data by airline to see how many planes per airline 
    faa_data_grouped = faa_data.groupby('NAME').agg(faa_fleet = ('N-NUMBER', 'count')).reset_index()

    #standardizing so we can join them on to each other
    contracts_data['faa_name'] = contracts_data['faa_name'].str.lower()
    faa_data_grouped['airlines'] = faa_data_grouped['NAME'].str.lower()

    #because of faa data incorporating suffixes (inc, plc, etc.) to airline data, can't join directly
    results = []
    for _, row in contracts_data.iterrows():
        #loop goes through the contracts table one airline at a time and 
        mask = faa_data_grouped['airlines'].str.contains(row['faa_name'], na=False)
        matched = faa_data_grouped[mask]

        if len(matched) > 0:
            faa_count = matched['faa_fleet'].values[0]
        else:
            faa_count = 0
        
        results.append({
            'airline_name': row['airline_name'],
            'faa_fleet' : faa_count
        })


    faa_counts = pd.DataFrame(results)
    df = pd.merge(contracts_data, faa_counts, on = 'airline_name', how = 'outer')

    print(f"Attainment table built: {len(df)} airlines")
    print(df[['airline_name', 'contracted_fleet', 'faa_fleet']].to_string(index=False))

    PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
    os.makedirs(PROCESSED_DIR, exist_ok = True)
    output_path = os.path.join(PROCESSED_DIR, "attainment.csv")

    df.to_csv(output_path, index=False)
    print(f"Saved attainment data to {output_path}")
    return df

if __name__ == '__main__':
    merge_faa_and_contracts()