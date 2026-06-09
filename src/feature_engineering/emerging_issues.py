from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd
import numpy as np

from topic_engine.topic_taxonomy import TOPIC_TAXONOMY

# =====================================================
# CONFIG
# =====================================================

MIN_TICKET_VOLUME = 10
ROLLING_WINDOW    = 3

# =====================================================
# NORMALIZE
# =====================================================

def normalize_score(series):
    min_val = series.min()
    max_val = series.max()

    if max_val == min_val:
        return pd.Series([100] * len(series), index=series.index)

    return (
        (series - min_val)
        / (max_val - min_val)
        * 100
    )

# =====================================================
# LOAD
# =====================================================

def load_heatmap_dataset(file_path):
    print("\nLoading heatmap dataset...")
    return pd.read_parquet(file_path)

# =====================================================
# RISK WEIGHT
# =====================================================

def add_risk_weight(df):
    risk_map = {topic: meta["risk_weight"] for topic, meta in TOPIC_TAXONOMY.items()}
    df["risk_weight"] = df["topic"].map(risk_map).fillna(1)
    return df

# =====================================================
# ROLLING BASELINE
# =====================================================

def calculate_baseline(df):
    print("Calculating rolling baseline...")

    df = df.sort_values(["topic", "tahun", "bulan"]).copy()
    df["baseline"] = (
        df.groupby("topic")["jumlah_tiket"]
        .transform(lambda x: x.shift(1).rolling(ROLLING_WINDOW, min_periods=1).mean())
    )

    return df

# =====================================================
# GROWTH
# =====================================================

def calculate_growth(df):
    print("Calculating growth...")

    df["growth_rate"] = np.where(
        df["baseline"] > 0,
        (df["jumlah_tiket"] - df["baseline"]) / df["baseline"] * 100,
        np.nan,
    )
    df["growth_rate"] = df["growth_rate"].round(2)

    return df

# =====================================================
# SCORE
# =====================================================

def calculate_emerging_score(df):
    print("Calculating emerging score...")

    df = df.copy()
    df = df[df["topic"] != "LAINNYA"]
    df = df[df["jumlah_tiket"] >= MIN_TICKET_VOLUME]

    df["growth_score"] = df["growth_rate"].clip(lower=-100, upper=300).fillna(0)
    df["volume_score"] = np.log1p(df["jumlah_tiket"])
    df["emerging_score"] = (
        (0.60 * df["growth_score"] + 0.40 * (df["volume_score"] * 20)) * df["risk_weight"]
    )
    df["emerging_index"] = normalize_score(df["emerging_score"]).round(2)

    return df

# =====================================================
# LABEL
# =====================================================

def assign_risk_level(score):
    if pd.isna(score): return "GREEN"
    if score >= 70:  return "RED"
    if score >= 40:   return "YELLOW"
    return "GREEN"

# =====================================================
# TOP 10
# =====================================================

def build_top10_latest(df):
    latest_period = df["periode"].max()
    latest        = df[df["periode"] == latest_period].copy()

    latest["risk_level"] = latest["emerging_index"].apply(assign_risk_level)
    latest = latest.sort_values("emerging_index", ascending=False)

    return latest.head(10)

# =====================================================
# SAVE
# =====================================================

def save_outputs(output_folder, emerging_df, top10_df):
    output_folder.mkdir(parents=True, exist_ok=True)

    emerging_df.to_parquet(output_folder / "emerging_issue_dataset.parquet", index=False)
    emerging_df.to_csv(output_folder / "emerging_issue_dataset.csv", index=False, encoding="utf-8-sig")
    top10_df.to_csv(output_folder / "top10_emerging_latest.csv", index=False, encoding="utf-8-sig")

# =====================================================
# MAIN
# =====================================================

def main():
    root          = Path(__file__).resolve().parents[2]
    input_file    = root / "data" / "processed" / "heatmap_dataset.parquet"
    output_folder = root / "data" / "processed"

    df = load_heatmap_dataset(input_file)
    df = add_risk_weight(df)
    df = calculate_baseline(df)
    df = calculate_growth(df)
    df = calculate_emerging_score(df)

    top10_df = build_top10_latest(df)
    save_outputs(output_folder, df, top10_df)

    cols = ["topic", "jumlah_tiket", "baseline", "growth_rate", "risk_weight", "emerging_score", "emerging_index", "risk_level"]

    print("\n=================================")
    print("EMERGING ISSUE ANALYSIS DONE")
    print("\nTop 10 Emerging Risk Issues")
    print(top10_df[cols])
    print("\n=================================")


if __name__ == "__main__":
    main()