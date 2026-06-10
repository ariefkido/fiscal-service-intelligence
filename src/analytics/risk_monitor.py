from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED    = PROJECT_ROOT / "data" / "processed"

# =====================================================
# CONFIG
# =====================================================

HAI_WEIGHT       = 0.50
IKPA_WEIGHT      = 0.30
REALISASI_WEIGHT = 0.20
TOP_N_EMERGING   = 5

# =====================================================
# LOAD DATA
# =====================================================

def load_data():
    emerging  = pd.read_parquet(PROCESSED / "emerging_issue_dataset.parquet")
    ikpa      = pd.read_parquet(PROCESSED / "ikpa_monthly.parquet")
    realisasi = pd.read_parquet(PROCESSED / "realisasi_monthly.parquet")
    return emerging, ikpa, realisasi

# =====================================================
# NORMALIZE 0-100
# =====================================================

def normalize_series(series):
    min_val = series.min()
    max_val = series.max()

    if max_val == min_val:
        return pd.Series([0] * len(series), index=series.index)

    return (series - min_val) / (max_val - min_val) * 100

# =====================================================
# HAI RISK
# =====================================================

def build_hai_risk(emerging_df):
    df = emerging_df.copy()
    df["emerging_score"] = df["emerging_score"].clip(lower=0)

    top_scores = (
        df.sort_values(["periode", "emerging_score"], ascending=[True, False])
        .groupby("periode")
        .head(TOP_N_EMERGING)
    )

    hai = top_scores.groupby("periode", as_index=False)["emerging_score"].mean()
    hai["hai_risk"] = normalize_series(hai["emerging_score"])

    return hai[["periode", "hai_risk"]]

# =====================================================
# IKPA RISK
# =====================================================

def build_ikpa_risk(df):
    ikpa = df.copy()
    ikpa["ikpa_risk"] = 100 - ikpa["ikpa_score"]
    return ikpa[["periode", "ikpa_score", "ikpa_risk"]]

# =====================================================
# REALISASI RISK
# =====================================================

def build_realisasi_risk(df):
    realisasi = df.copy()
    realisasi["target_pct"]     = realisasi["bulan"] / 12 * 100
    realisasi["gap"]            = (realisasi["target_pct"] - realisasi["realisasi_pct"]).clip(lower=0)
    realisasi["realisasi_risk"] = normalize_series(realisasi["gap"])
    return realisasi[["periode", "realisasi_pct", "realisasi_risk"]]

# =====================================================
# RISK SCORE
# =====================================================

def calculate_risk_score(df):
    df["risk_score"] = (
        HAI_WEIGHT       * df["hai_risk"]
        + IKPA_WEIGHT      * df["ikpa_risk"]
        + REALISASI_WEIGHT * df["realisasi_risk"]
    ).round(2)

    return df

# =====================================================
# DYNAMIC LABEL
# =====================================================

def assign_dynamic_labels(df):
    p75 = df["risk_score"].quantile(0.75)
    p90 = df["risk_score"].quantile(0.90)

    def label(score):
        if score >= p90: return "RED"
        if score >= p75: return "YELLOW"
        return "GREEN"

    df["risk_level"]       = df["risk_score"].apply(label)
    df["threshold_yellow"] = round(p75, 2)
    df["threshold_red"]    = round(p90, 2)

    return df

# =====================================================
# BUILD MONITOR
# =====================================================

def build_monitor(hai_df, ikpa_df, realisasi_df):
    df = (
        hai_df
        .merge(ikpa_df,      on="periode", how="inner")
        .merge(realisasi_df, on="periode", how="inner")
    )

    df = calculate_risk_score(df)
    df = assign_dynamic_labels(df)

    df["tahun"] = df["periode"].str[:4].astype(int)
    df["bulan"] = df["periode"].str[-2:].astype(int)

    return df.sort_values("periode")

# =====================================================
# SAVE OUTPUT
# =====================================================

def save_outputs(output_folder, df):
    output_folder.mkdir(parents=True, exist_ok=True)

    df.to_parquet(output_folder / "risk_monitor_dataset.parquet", index=False)
    df.to_csv(    output_folder / "risk_monitor_dataset.csv",     index=False, encoding="utf-8-sig")

# =====================================================
# MAIN
# =====================================================

def main():
    emerging, ikpa, realisasi = load_data()

    hai_risk       = build_hai_risk(emerging)
    ikpa_risk      = build_ikpa_risk(ikpa)
    realisasi_risk = build_realisasi_risk(realisasi)
    risk_df        = build_monitor(hai_risk, ikpa_risk, realisasi_risk)

    save_outputs(PROCESSED, risk_df)

    print("\nRISK MONITOR DONE\n")
    print(risk_df[["periode", "risk_score", "risk_level"]].tail(12))
    print("\nRisk Distribution\n")
    print(risk_df["risk_level"].value_counts())
    print(f"\nOutput:\n{PROCESSED}")


if __name__ == "__main__":
    main()