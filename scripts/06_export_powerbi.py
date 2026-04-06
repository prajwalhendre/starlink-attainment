import pandas as pd
import os

#standardized directory set up
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
POWERBI_DIR = os.path.join(BASE_DIR, 'powerbi')

os.makedirs(POWERBI_DIR, exist_ok = True)

def powerbi_export():
    print('Importing csv files')
    attainment_master_path = os.path.join(PROCESSED_DIR, 'attainment.csv')
    revenue_model_master_path = os.path.join(PROCESSED_DIR, 'revenue_model_data.csv')
    risk_classification_master_path = os.path.join(PROCESSED_DIR, 'risk_classification.csv')

    attainment_df = pd.read_csv(attainment_master_path, low_memory=False)
    revenue_model_df = pd.read_csv(revenue_model_master_path, low_memory = False)
    risk_classification_df = pd.read_csv(risk_classification_master_path, low_memory=False)

    attainment_output_path = os.path.join(POWERBI_DIR, 'attainment.csv')
    revenue_output_path = os.path.join(POWERBI_DIR, 'revenue_model.csv')
    risk_classification_output_path = os.path.join(POWERBI_DIR, 'risk_classification.csv')
    
    print('Exporting csv files')
    attainment_df.to_csv(attainment_output_path, index = False)
    revenue_model_df.to_csv(revenue_output_path, index=False)
    risk_classification_df.to_csv(risk_classification_output_path, index=False)
    
    print('Export complete')
    return 0

if __name__ == '__main__':
    powerbi_export()