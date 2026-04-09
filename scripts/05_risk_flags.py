import pandas as pd
import os
import numpy as np


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

master_path = os.path.join(PROCESSED_DIR, "revenue_model_data.csv")

def risk_classification():
    print('Reading in revenue_model.csv')
    revenue_df = pd.read_csv(master_path, low_memory= False)
    revenue_df['risk_flag'] = np.where(
        (revenue_df['stc_status'] == 'Prospective') & (revenue_df['revenue_gap_mrr'] > 10000000),
        'Competitive Risk',
        np.where(
            (revenue_df['stc_status'] == 'Pending') & (revenue_df['revenue_gap_mrr'] > 10000000),
            'Critical',
            np.where(
                (revenue_df['stc_status'] == 'Pending') | (revenue_df['revenue_gap_mrr'] > 5000000),
                'High',
                'Medium'
            )
        )
    )
    output_path = os.path.join(PROCESSED_DIR, 'risk_classification.csv')
    revenue_df.to_csv(output_path, index=False)
    print('risk_flags.csv saved')
    return revenue_df

if __name__ == '__main__':
    risk_classification()
