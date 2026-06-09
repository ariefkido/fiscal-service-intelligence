import pandas as pd

df = pd.read_parquet(
    "data/processed/emerging_issue_dataset.parquet"
)

print(df.columns.tolist())