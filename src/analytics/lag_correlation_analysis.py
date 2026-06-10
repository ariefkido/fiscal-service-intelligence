from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED    = PROJECT_ROOT / "data" / "processed"
MAX_LAG      = 3

# =====================================================
# LOAD DATA
# =====================================================

def load_data():
    heatmap   = pd.read_parquet(PROCESSED / "heatmap_dataset.parquet")
    ikpa      = pd.read_parquet(PROCESSED / "ikpa_monthly.parquet")
    realisasi = pd.read_parquet(PROCESSED / "realisasi_monthly.parquet")
    return heatmap, ikpa, realisasi

# =====================================================
# BUILD LAG CORRELATION
# =====================================================

def build_lag_correlation(heatmap, target_df, target_col):
    rows = []
    target_df = (
        target_df[["periode", target_col]]
        .copy()
        .sort_values("periode")
        .reset_index(drop=True)
    )

    for topic in sorted(heatmap["topic"].unique()):
        topic_df = (
            heatmap[heatmap["topic"] == topic][["periode", "jumlah_tiket"]]
            .copy()
            .sort_values("periode")
            .reset_index(drop=True)
        )

        for lag in range(MAX_LAG + 1):
            lag_target = target_df.copy()
            lag_target[target_col] = lag_target[target_col].shift(-lag)
            merged = topic_df.merge(lag_target, on="periode", how="inner").dropna()
            if len(merged) < 6:
                continue
            corr = merged["jumlah_tiket"].corr(merged[target_col])
            if pd.isna(corr):
                corr = 0
            rows.append({
                "target":          target_col,
                "topic":           topic,
                "lag":             lag,
                "correlation":     round(corr, 4),
                "abs_correlation": round(abs(corr), 4),
            })

    result = pd.DataFrame(rows)
    if result.empty:
        return result

    result["direction"] = result["correlation"].apply(
        lambda x: "NEGATIVE" if x < 0 else ("POSITIVE" if x > 0 else "NEUTRAL")
    )
    return result.sort_values(["abs_correlation", "lag"], ascending=[False, True]).reset_index(drop=True)

# =====================================================
# BUILD BEST LAG
# =====================================================

def build_best_lag(lag_df):

    if lag_df.empty:
        return lag_df

    # hanya lag yang benar-benar mendahului
    lag_df = lag_df[lag_df["lag"] > 0]

    return (
        lag_df
        .sort_values(
            ["abs_correlation", "lag"],
            ascending=[False, True]
        )
        .drop_duplicates(subset="topic", keep="first")
        [["target", "topic", "lag", "correlation",
          "abs_correlation", "direction"]]
        .reset_index(drop=True)
    )

# =====================================================
# SAVE OUTPUT
# =====================================================

def save_output(ikpa_lag, realisasi_lag, ikpa_best, realisasi_best):
    ikpa_lag.to_csv(      PROCESSED / "topic_ikpa_lag_correlation.csv",      index=False, encoding="utf-8-sig")
    realisasi_lag.to_csv( PROCESSED / "topic_realisasi_lag_correlation.csv", index=False, encoding="utf-8-sig")
    ikpa_best.to_csv(     PROCESSED / "topic_ikpa_best_lag.csv",             index=False, encoding="utf-8-sig")
    realisasi_best.to_csv(PROCESSED / "topic_realisasi_best_lag.csv",        index=False, encoding="utf-8-sig")

# =====================================================
# MAIN
# =====================================================

def main():
    print("\nLoading datasets...")
    heatmap, ikpa, realisasi = load_data()

    print("\nBuilding IKPA lag correlation...")
    ikpa_lag  = build_lag_correlation(heatmap, ikpa, "ikpa_score")
    ikpa_best = build_best_lag(ikpa_lag)

    print("\nBuilding Realisasi lag correlation...")
    realisasi_lag  = build_lag_correlation(heatmap, realisasi, "realisasi_pct")
    realisasi_best = build_best_lag(realisasi_lag)

    save_output(ikpa_lag, realisasi_lag, ikpa_best, realisasi_best)

    print("\nTOP IKPA LAG CORRELATION")
    print(ikpa_lag.head(20))
    print("\nBEST LAG PER TOPIC — IKPA")
    print(ikpa_best.head(10))
    print("\nTOP REALISASI LAG CORRELATION")
    print(realisasi_lag.head(20))
    print("\nBEST LAG PER TOPIC — REALISASI")
    print(realisasi_best.head(10))
    print(f"\nOutput:\n{PROCESSED}")


if __name__ == "__main__":
    main()