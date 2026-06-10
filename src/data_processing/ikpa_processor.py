from pathlib import Path
import pandas as pd
import re

PROJECT_ROOT  = Path(__file__).resolve().parents[2]
INPUT_FOLDER  = PROJECT_ROOT / "data" / "raw" / "Dataset IKPA 2020-2022"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"

# =====================================================
# EXTRACT PERIODE
# =====================================================

def extract_period(filename):
    match = re.search(r"(\d{4})(\d{2})", filename)

    if not match:
        raise ValueError(f"Gagal membaca periode: {filename}")

    tahun = int(match.group(1))
    bulan = int(match.group(2))

    return tahun, bulan

# =====================================================
# PROCESS FILE
# =====================================================

def process_file(file_path):
    tahun, bulan = extract_period(file_path.name)
    print(f"Processing {file_path.name}")

    df = pd.read_excel(file_path, header=None)

    headers       = df.iloc[2].fillna("").astype(str).tolist()
    data          = df.iloc[4:].copy()
    data.columns  = headers
    data          = data.dropna(how="all")

    nilai_col = None
    for col in data.columns:
        if "nilai akhir" in str(col).lower():
            nilai_col = col
            break

    if nilai_col is None:
        raise ValueError("Kolom Nilai Akhir tidak ditemukan")

    nilai_akhir = pd.to_numeric(data[nilai_col], errors="coerce").dropna()

    if len(nilai_akhir) == 0:
        raise ValueError("Nilai IKPA kosong")

    ikpa_score = float(nilai_akhir.iloc[0])

    return {
        "periode":    f"{tahun}-{bulan:02d}",
        "tahun":      tahun,
        "bulan":      bulan,
        "ikpa_score": round(ikpa_score, 2),
    }

# =====================================================
# PROCESS ALL FILES
# =====================================================

def process_all_files():
    files = sorted(INPUT_FOLDER.glob("*.xlsx"))
    print("\nLoading IKPA files...")

    rows = []
    for file in files:
        try:
            rows.append(process_file(file))
        except Exception as e:
            print(f"[ERROR] {file.name}")
            print(e)

    return pd.DataFrame(rows)

# =====================================================
# SAVE OUTPUT
# =====================================================

def save_output(df):
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    df.to_parquet(OUTPUT_FOLDER / "ikpa_monthly.parquet", index=False)
    df.to_csv(    OUTPUT_FOLDER / "ikpa_monthly.csv",     index=False, encoding="utf-8-sig")

# =====================================================
# MAIN
# =====================================================

def main():
    df = process_all_files()

    if df.empty:
        raise ValueError("Tidak ada file IKPA yang berhasil diproses")

    df = df.sort_values(["tahun", "bulan"])

    save_output(df)

    print("\nIKPA PROCESSING DONE\n")
    print(df.head())
    print(df.tail())
    print(df.describe())
    print(f"\nOutput:\n{OUTPUT_FOLDER}")


if __name__ == "__main__":
    main()