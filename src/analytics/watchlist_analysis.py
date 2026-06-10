from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED    = PROJECT_ROOT / "data" / "processed"

# =====================================================
# LOAD DATA
# =====================================================

def load_data():
    emerging   = pd.read_parquet(PROCESSED / "emerging_issue_dataset.parquet")
    complexity = pd.read_parquet(PROCESSED / "complexity_radar.parquet")
    ikpa       = pd.read_csv(PROCESSED / "topic_ikpa_best_lag.csv")
    realisasi  = pd.read_csv(PROCESSED / "topic_realisasi_best_lag.csv")
    return emerging, complexity, ikpa, realisasi

# =====================================================
# NORMALIZE
# =====================================================

def normalize(series):
    series          = np.log1p(series.clip(lower=0))
    min_val, max_val = series.min(), series.max()
    if max_val == min_val:
        return pd.Series(0, index=series.index)
    return (series - min_val) / (max_val - min_val) * 100

# =====================================================
# BUILD WATCHLIST
# =====================================================

def build_watchlist(emerging, complexity, ikpa, realisasi):
    emerging_latest = (
        emerging
        .sort_values("periode")
        .groupby("topic")
        .tail(1)
        [["topic", "emerging_index"]]
    )

    impact = (
        ikpa[["topic", "abs_correlation"]]
        .rename(columns={"abs_correlation": "ikpa_impact"})
        .merge(
            realisasi[["topic", "abs_correlation"]].rename(columns={"abs_correlation": "realisasi_impact"}),
            on="topic",
            how="outer",
        )
    )
    impact["impact_score"] = impact[["ikpa_impact", "realisasi_impact"]].fillna(0).mean(axis=1)

    df = (
        complexity[["topic", "complexity_score"]]
        .merge(emerging_latest, on="topic", how="left")
        .merge(impact[["topic", "impact_score"]], on="topic", how="left")
        .fillna(0)
    )

    df["emerging_norm"]   = normalize(df["emerging_index"])
    df["complexity_norm"] = normalize(df["complexity_score"])
    df["impact_norm"]     = normalize(df["impact_score"])

    df["watchlist_score"] = (
        df["emerging_norm"]   * 0.30
        + df["complexity_norm"] * 0.40
        + df["impact_norm"]     * 0.30
    )

    df["priority"] = pd.cut(
        df["watchlist_score"],
        bins=[-1, 35, 55, 75, 100],
        labels=["LOW", "MEDIUM", "HIGH", "CRITICAL"],
    )

    return df.sort_values("watchlist_score", ascending=False).reset_index(drop=True)

# =====================================================
# SAVE OUTPUT
# =====================================================

def save_output(df):
    df.to_parquet(PROCESSED / "watchlist_topics.parquet", index=False)
    df.to_csv(    PROCESSED / "watchlist_topics.csv",     index=False, encoding="utf-8-sig")

# =====================================================
# MAIN
# =====================================================

def main():
    print("\nLoading datasets...")
    emerging, complexity, ikpa, realisasi = load_data()

    watchlist = build_watchlist(emerging, complexity, ikpa, realisasi)
    save_output(watchlist)

    print("\nTOP WATCHLIST")
    print(watchlist.head(15))
    print(f"\nOutput:\n{PROCESSED}")


if __name__ == "__main__":
    main()