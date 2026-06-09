from pathlib import Path
import pandas as pd

ROOT      = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"


def load_data():
    heatmap   = pd.read_parquet(PROCESSED / "heatmap_dataset.parquet")
    ikpa      = pd.read_parquet(PROCESSED / "ikpa_monthly.parquet")
    realisasi = pd.read_parquet(PROCESSED / "realisasi_monthly.parquet")
    return heatmap, ikpa, realisasi


def _build_correlation(heatmap, other_df, other_col):
    rows = []
    for topic in sorted(heatmap["topic"].unique()):
        topic_df = heatmap[heatmap["topic"] == topic][["periode", "jumlah_tiket"]]
        merged   = topic_df.merge(other_df[["periode", other_col]], on="periode", how="inner")
        if len(merged) < 6:
            continue
        corr = merged["jumlah_tiket"].corr(merged[other_col])
        if pd.isna(corr):
            corr = 0
        rows.append({"topic": topic, "correlation": round(corr, 4)})
    df = pd.DataFrame(rows)
    df["abs_correlation"] = df["correlation"].abs()
    return df.sort_values("abs_correlation", ascending=False)


def build_ikpa_correlation(heatmap, ikpa):
    return _build_correlation(heatmap, ikpa, "ikpa_score")


def build_realisasi_correlation(heatmap, realisasi):
    return _build_correlation(heatmap, realisasi, "realisasi_pct")


def save_output(ikpa_corr, realisasi_corr):
    ikpa_corr.to_csv(PROCESSED / "topic_ikpa_correlation.csv", index=False, encoding="utf-8-sig")
    realisasi_corr.to_csv(PROCESSED / "topic_realisasi_correlation.csv", index=False, encoding="utf-8-sig")


def main():
    print("\nLoading datasets...")
    heatmap, ikpa, realisasi = load_data()

    print("\nBuilding IKPA correlation...")
    ikpa_corr = build_ikpa_correlation(heatmap, ikpa)

    print("\nBuilding Realisasi correlation...")
    realisasi_corr = build_realisasi_correlation(heatmap, realisasi)

    save_output(ikpa_corr, realisasi_corr)

    print("\n=================================")
    print("\nTOP IKPA CORRELATION")
    print(ikpa_corr.head(10))
    print("\nTOP REALISASI CORRELATION")
    print(realisasi_corr.head(10))
    print("\n=================================")


if __name__ == "__main__":
    main()