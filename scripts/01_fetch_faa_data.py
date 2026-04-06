import requests
import zipfile
import io
import pandas as pd
import os
import platform

#base directory of project (/starlink_attainment)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#saving faa file to the /starlink_attainment/data/raw location
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
#to be used in the future for /starlink_attainment/data/processed
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

#making directories
os.makedirs(RAW_DIR, exist_ok = True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

FAA_URL = "https://registry.faa.gov/database/ReleasableAircraft.zip"

def download_faa_registry():
    print('Downloading FAA registry...')
    try:
        #needed for FAA to identify request like a real browser rather than script lmao
        headers = {"User-Agent": f"Mozilla/5.0 ({platform.system()} {platform.release()})"}
        #storing faa info in zipped file in raw bytes
        response = requests.get(FAA_URL, headers = headers)
        #shows error if status != 200
        response.raise_for_status()
        #io.BytesIO converts response from http package to raw zip bytes
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        #dumping contents in data/raw/
        zip_file.extractall(RAW_DIR)
        print(f"Extracted to {RAW_DIR}")
    except Exception as e:
        print(f"Something went wrong: {e}")

def load_and_filter_faa():
    print("Loading FAA master file...")
    #creating path for master.txt file
    master_path = os.path.join(RAW_DIR, "MASTER.txt")
    #loading master.txt into df
    df = pd.read_csv(master_path, dtype=str, low_memory=False)
    #for column names
    df.columns = df.columns.str.strip()
    #for data
    df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

    airlines = [
        "UNITED AIRLINES",
        "DELTA AIR LINES",
        "AMERICAN AIRLINES",
        "SOUTHWEST AIRLINES",
        "QATAR AIRWAYS",
        "EMIRATES",
        "LUFTHANSA",
        "BRITISH AIRWAYS",
        "HAWAIIAN AIRLINES",
        "ALASKA AIRLINES"
    ]
    #used to check filtering all at once in one joined string as opposed to one by one
    mask = df["NAME"].str.contains("|".join(airlines), case=False, na=False)
    #used to get rid of False positives (AFRICAN AMERICAN AIRLINES and LUFTHANSA AVIATION TRAINING USA INC)
    exclusions = ['AFRICAN AMERICAN AIRLINES', "LUFTHANSA AVIATION TRAINING USA INC"]
    mask_exclude = ~df["NAME"].str.contains('|'.join(exclusions), case=False, na=False)
    df_filtered = df[mask & mask_exclude]

    #keeping only useful info
    df_filtered = df_filtered[["N-NUMBER", "NAME", "MFR MDL CODE", "STATE", "YEAR MFR"]]

    output_path = os.path.join(PROCESSED_DIR, "faa_filtered.csv")
    df_filtered.to_csv(output_path, index=False)
    print(f"Saved {len(df_filtered)} to {output_path}")

    return df_filtered

if __name__ == '__main__':
    download_faa_registry()
    load_and_filter_faa()