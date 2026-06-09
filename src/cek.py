import pandas as pd

df = pd.read_parquet("data/processed/topic_dataset.parquet")

print(df.columns.tolist())