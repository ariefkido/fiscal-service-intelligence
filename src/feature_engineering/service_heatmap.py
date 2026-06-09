import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd

# =====================================================
# LOAD
# =====================================================

def load_topic_dataset(file_path):
    print("\nLoading topic dataset...")
    return pd.read_parquet(file_path)

# =====================================================
# BUILD HEATMAP DATASET
# =====================================================

def build_heatmap_dataset(df):
    print("\nBuilding heatmap dataset...")

    heatmap = (
        df.groupby(["periode", "tahun", "bulan", "topic"])
        .size()
        .reset_index(name="jumlah_tiket")
        .sort_values(["tahun", "bulan", "jumlah_tiket"], ascending=[True, True, False])
    )

    return heatmap

# =====================================================
# BUILD PIVOT
# =====================================================

def build_heatmap_pivot(df):
    return pd.pivot_table(
        df,
        index="topic",
        columns="periode",
        values="jumlah_tiket",
        fill_value=0,
    )

# =====================================================
# SAVE
# =====================================================

def save_outputs(output_folder, heatmap_df, pivot_df):
    output_folder.mkdir(parents=True, exist_ok=True)

    heatmap_df.to_parquet(output_folder / "heatmap_dataset.parquet", index=False)
    heatmap_df.to_csv(output_folder / "heatmap_dataset.csv", index=False, encoding="utf-8-sig")
    pivot_df.to_csv(output_folder / "heatmap_pivot.csv", encoding="utf-8-sig")

# =====================================================
# MAIN
# =====================================================

def main():
    root          = Path(__file__).resolve().parents[2]
    input_file    = root / "data" / "processed" / "topic_dataset.parquet"
    output_folder = root / "data" / "processed"

    df = load_topic_dataset(input_file)
    print(f"Total tiket : {len(df):,}")

    heatmap_df = build_heatmap_dataset(df)
    pivot_df   = build_heatmap_pivot(heatmap_df)

    save_outputs(output_folder, heatmap_df, pivot_df)

    print("\n=================================")
    print(f"Rows heatmap : {len(heatmap_df):,}")
    print("\nTop 10 records:")
    print(heatmap_df.head(10))
    print("\nOutput:")
    print(output_folder)
    print("\n=================================")


if __name__ == "__main__":
    main()