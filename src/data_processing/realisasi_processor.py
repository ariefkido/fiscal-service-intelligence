from pathlib import Path
import pandas as pd
import re

PROJECT_ROOT  = Path(__file__).resolve().parents[2]
INPUT_FOLDER  = PROJECT_ROOT / "data" / "raw" / "Dataset Realisasi Anggaran 2020-2022"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"

# =====================================================
# MONTH MAPPING
# =====================================================

MONTH_MAP = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4,
    "MEI": 5, "JUN": 6, "JUL": 7, "AGS": 8,
    "SEP": 9, "OKT": 10, "NOV": 11, "DES": 12,
}

# =====================================================
# EXTRACT YEAR
# =====================================================

def extract_year(filename):
    match = re.search(r"(20\d{2})", filename)

    if not match:
        raise ValueError(f"Tahun tidak ditemukan: {filename}")

    return int(match.group(1))

# =====================================================
# PROCESS SINGLE FILE
# =====================================================

def process_single_file(file_path):
    print(f"Processing {file_path.name}")

    df = pd.read_excel(file_path)

    if len(df) == 0:
        raise ValueError(f"File kosong: {file_path.name}")

    row  = df.iloc[0]
    pagu = float(row["PAGU_DIPA"])
    year = extract_year(file_path.name)

    cumulative = 0
    records    = []

    for month_name, month_num in MONTH_MAP.items():
        value = pd.to_numeric(row[month_name], errors="coerce")
        value = float(value) if not pd.isna(value) else 0.0

        cumulative += value
        pct         = cumulative / pagu * 100

        records.append({
            "periode":             f"{year}-{month_num:02d}",
            "tahun":               year,
            "bulan":               month_num,
            "realisasi_bulan":     round(value, 2),
            "realisasi_kumulatif": round(cumulative, 2),
            "realisasi_pct":       round(pct, 2),
        })

    return pd.DataFrame(records)

# =====================================================
# PROCESS ALL FILES
# =====================================================

def process_all_files():
    files = sorted(INPUT_FOLDER.glob("*.xlsx"))

    if not files:
        raise FileNotFoundError(f"Tidak ada file:\n{INPUT_FOLDER}")

    all_df = []
    for file in files:
        try:
            all_df.append(process_single_file(file))
        except Exception as e:
            print(f"[ERROR] {file.name}")
            print(e)

    return pd.concat(all_df, ignore_index=True)

# =====================================================
# VALIDATION
# =====================================================

def validate_dataset(df):
    print("\nValidating dataset...")
    print(f"Rows          : {len(df)}")
    print(f"Min Realisasi : {df['realisasi_pct'].min():.2f}%")
    print(f"Max Realisasi : {df['realisasi_pct'].max():.2f}%")

# =====================================================
# SAVE OUTPUT
# =====================================================

def save_outputs(df):
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    df.to_parquet(OUTPUT_FOLDER / "realisasi_monthly.parquet", index=False)
    df.to_csv(    OUTPUT_FOLDER / "realisasi_monthly.csv",     index=False, encoding="utf-8-sig")

# =====================================================
# MAIN
# =====================================================

def main():
    df = process_all_files()
    df = df.sort_values(["tahun", "bulan"])

    validate_dataset(df)
    save_outputs(df)

    print("\nREALISASI PROCESSING DONE")
    print(df.head())
    print(f"\nOutput:\n{OUTPUT_FOLDER}")


if __name__ == "__main__":
    main()