import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
revenue_data_master_path = os.path.join(PROCESSED_DIR, 'attainment.csv')


#js basic calcs for revenue model that are gonna be used in powerbi
def build_revenue_model():
    print('Build revenue model...')
    revenue_df = pd.read_csv(revenue_data_master_path, low_memory = False)
    revenue_df['current_mrr'] = 0.093 * revenue_df['contracted_fleet'] * revenue_df['monthly_rate_usd']
    revenue_df["potential_mrr"] = revenue_df['contracted_fleet'] * revenue_df['monthly_rate_usd']
    revenue_df["revenue_gap_mrr"] = revenue_df['potential_mrr'] - revenue_df['current_mrr']
    revenue_df['potential_arr'] = revenue_df['potential_mrr'] * 12
    output_path = os.path.join(PROCESSED_DIR, "revenue_model_data.csv")
    revenue_df.to_csv(output_path, index=False)

    print(f"Saved revenue model to {output_path}")
    print(f"Total potential ARR: ${revenue_df['potential_arr'].sum():,.0f}")
    print(f"Total current MRR: ${revenue_df['current_mrr'].sum():,.0f}")
    print(f"Total revenue gap MRR: ${revenue_df['revenue_gap_mrr'].sum():,.0f}")

    return revenue_df

if __name__ == '__main__':
    build_revenue_model()
