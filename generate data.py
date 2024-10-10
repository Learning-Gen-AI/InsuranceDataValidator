import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate 1000 records
n_records = 1000

# Generate data
data = {
    'policy_id': [f'POL-{i:06d}' for i in range(1, n_records + 1)],
    'customer_name': [fake.name() for _ in range(n_records)],
    'age': np.random.randint(18, 80, n_records),
    'gender': np.random.choice(['M', 'F', 'Other'], n_records),
    'policy_type': np.random.choice(['Auto', 'Home', 'Life', 'Health'], n_records),
    'premium': np.random.uniform(500, 5000, n_records).round(2),
    'coverage_amount': np.random.uniform(50000, 1000000, n_records).round(2),
    'start_date': [fake.date_between(start_date='-5y', end_date='today') for _ in range(n_records)],
    'end_date': [fake.date_between(start_date='today', end_date='+5y') for _ in range(n_records)],
    'is_active': np.random.choice([True, False], n_records, p=[0.9, 0.1]),
    'risk_score': np.random.randint(1, 101, n_records),
    'claim_history': np.random.poisson(lam=1, size=n_records),
    'annual_income': np.random.uniform(20000, 200000, n_records).round(2),
    'zip_code': [fake.zipcode() for _ in range(n_records)],
    'agent_id': [f'AGT-{random.randint(1, 100):03d}' for _ in range(n_records)]
}

# Create DataFrame
df = pd.DataFrame(data)

# Introduce some inconsistencies and errors
random_indices = np.random.choice(df.index, 50, replace=False)
df.loc[random_indices, 'customer_name'] = df.loc[random_indices, 'customer_name'].str.upper()

df.loc[np.random.choice(df.index, 30, replace=False), 'gender'] = np.nan
df.loc[np.random.choice(df.index, 20, replace=False), 'premium'] = np.nan
df.loc[np.random.choice(df.index, 10, replace=False), 'zip_code'] = 'INVALID'

# Save to CSV
df.to_csv(r'C:\Store\Projects\IAA\2024 10 10 Data cleaning\insurance_dummy_data.csv', index=False)

print(df.head())
print(f"\nDataset shape: {df.shape}")
print(f"\nColumn names: {', '.join(df.columns)}")