from pathlib import Path
from datetime import datetime
import pandas as pd

ROOT      = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
OUTPUT    = ROOT / "data" / "output"
OUTPUT.mkdir(parents=True, exist_ok=True)


def load_data():
    watchlist         = pd.read_parquet(PROCESSED / "watchlist_topics.parquet")
    ikpa_leading      = pd.read_csv(PROCESSED / "topic_ikpa_best_lag.csv")
    realisasi_leading = pd.read_csv(PROCESSED / "topic_realisasi_best_lag.csv")
    risk              = pd.read_parquet(PROCESSED / "risk_monitor_dataset.parquet")
    return watchlist, ikpa_leading, realisasi_leading, risk


def build_brief(watchlist, ikpa_leading, realisasi_leading, risk):
    top_watchlist  = watchlist.iloc[0]
    top5_watchlist = watchlist.head(5)["topic"].tolist()
    top_ikpa       = ikpa_leading.iloc[0]
    top_realisasi  = realisasi_leading.iloc[0]
    red_count      = risk["risk_level"].eq("RED").sum()
    yellow_count   = risk["risk_level"].eq("YELLOW").sum()
    green_count    = risk["risk_level"].eq("GREEN").sum()
    report_date    = datetime.now().strftime("%d %B %Y")

    top5_lines = "\n".join(f"{i}. {t}" for i, t in enumerate(top5_watchlist, 1))

    return f"""
============================================================
FISCAL SERVICE INTELLIGENCE
EXECUTIVE BRIEF
============================================================

Tanggal Laporan : {report_date}

------------------------------------------------------------
1. RINGKASAN KONDISI
------------------------------------------------------------

Analisis Fiscal Service Intelligence (FSI) memanfaatkan
data layanan HAI DJPb untuk mengidentifikasi pola
permasalahan pelaksanaan anggaran, mengukur tingkat
kompleksitas layanan, serta mendeteksi potensi risiko
yang dapat mempengaruhi kualitas pelaksanaan anggaran.

Berdasarkan hasil analisis, topik dengan prioritas
tertinggi saat ini adalah:

TOPIC           : {top_watchlist['topic']}
WATCHLIST SCORE : {top_watchlist['watchlist_score']:.2f}
PRIORITY        : {top_watchlist['priority']}

------------------------------------------------------------
2. TOP PRIORITY TOPICS
------------------------------------------------------------

Lima topik yang memerlukan perhatian dan pembinaan
lebih lanjut adalah:

{top5_lines}

------------------------------------------------------------
3. LEADING INDICATOR ANALYSIS
------------------------------------------------------------

TOPIK TERKUAT TERHADAP IKPA

Topic       : {top_ikpa['topic']}
Correlation : {top_ikpa['correlation']:.3f}
Lag         : {top_ikpa['lag']} bulan
Direction   : {top_ikpa['direction']}

Interpretasi:

Peningkatan permasalahan pada topik tersebut
berhubungan dengan penurunan kualitas pelaksanaan
anggaran yang tercermin dalam nilai IKPA.

TOPIK TERKUAT TERHADAP REALISASI

Topic       : {top_realisasi['topic']}
Correlation : {top_realisasi['correlation']:.3f}
Lag         : {top_realisasi['lag']} bulan
Direction   : {top_realisasi['direction']}

Interpretasi:

Peningkatan permasalahan pada topik tersebut
berpotensi mempengaruhi realisasi anggaran
dalam kurun waktu {top_realisasi['lag']} bulan
setelah permasalahan muncul.

------------------------------------------------------------
4. RISK MONITORING
------------------------------------------------------------

Distribusi tingkat risiko selama periode analisis:

GREEN  : {green_count} bulan
YELLOW : {yellow_count} bulan
RED    : {red_count} bulan

Interpretasi:

Periode dengan status RED menunjukkan adanya
indikasi risiko yang memerlukan perhatian lebih
lanjut karena kombinasi antara meningkatnya
permasalahan layanan, penurunan kualitas IKPA,
dan perlambatan realisasi anggaran.

------------------------------------------------------------
5. REKOMENDASI
------------------------------------------------------------

1. Prioritaskan pembinaan pada topik
   {top_watchlist['topic']}.

2. Tingkatkan monitoring terhadap topik
   yang memiliki hubungan kuat dengan IKPA
   dan realisasi anggaran.

3. Manfaatkan data HAI DJPb sebagai
   early warning system pelaksanaan anggaran.

4. Fokuskan intervensi pada topik yang
   memiliki kombinasi:
   - Emerging Issues tinggi
   - Complexity tinggi
   - Impact tinggi

5. Lakukan pemantauan berkala terhadap
   Early Warning Watchlist sebagai dasar
   penentuan prioritas pembinaan satker.

------------------------------------------------------------
KESIMPULAN
------------------------------------------------------------

Data layanan HAI DJPb tidak hanya berfungsi sebagai
sarana konsultasi dan penyelesaian masalah, tetapi
juga dapat dimanfaatkan sebagai sumber informasi
strategis untuk mendeteksi potensi risiko
pelaksanaan anggaran secara lebih dini.

Pendekatan Fiscal Service Intelligence memungkinkan
organisasi mengubah data layanan menjadi insight
yang mendukung pengambilan keputusan berbasis data.

============================================================
END OF REPORT
============================================================
"""


def save_brief(text):
    output_file = OUTPUT / "executive_brief.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    return output_file


def main():
    print("\nLoading datasets...")
    watchlist, ikpa_leading, realisasi_leading, risk = load_data()

    print("Building executive brief...")
    brief = build_brief(watchlist, ikpa_leading, realisasi_leading, risk)
    output_file = save_brief(brief)

    print("\n=================================")
    print("EXECUTIVE BRIEF GENERATED")
    print(output_file)
    print("=================================")


if __name__ == "__main__":
    main()