# run_pipeline.py

from pathlib import Path
import subprocess
import sys
import time

PROJECT_ROOT = Path(__file__).parent


PIPELINE = [
    ("Topic Classification", "src/topic_engine/topic_classifier.py"),

    ("IKPA Processing", "src/data_processing/ikpa_processor.py"),
    ("Realisasi Processing", "src/data_processing/realisasi_processor.py"),

    ("Service Heatmap", "src/feature_engineering/service_heatmap.py"),
    ("Emerging Issues", "src/feature_engineering/emerging_issues.py"),
    ("Complexity Radar", "src/feature_engineering/complexity_radar.py"),

    ("Correlation Analysis", "src/analytics/correlation_analysis.py"),
    ("Lag Correlation Analysis", "src/analytics/lag_correlation_analysis.py"),

    ("Risk Monitoring", "src/analytics/risk_monitor.py"),
    ("Watchlist Analysis", "src/analytics/watchlist_analysis.py"),

    ("Executive Brief", "src/reporting/executive_brief.py"),
    ("Executive Brief DOCX", "src/reporting/executive_brief_docx.py"),
]


def run_script(name, script_path):
    script_file = PROJECT_ROOT / script_path

    if not script_file.exists():
        raise FileNotFoundError(
            f"Script tidak ditemukan: {script_file}"
        )

    print("\n" + "=" * 80)
    print(f"RUNNING : {name}")
    print("=" * 80)

    start = time.time()

    result = subprocess.run(
        [sys.executable, str(script_file)],
        cwd=PROJECT_ROOT
    )

    duration = time.time() - start

    if result.returncode != 0:
        raise RuntimeError(
            f"{name} gagal dijalankan "
            f"(exit code {result.returncode})"
        )

    print(f"✓ Selesai ({duration:.1f} detik)")


def main():

    total_start = time.time()

    print("=" * 80)
    print("FISCAL SERVICE INTELLIGENCE PIPELINE")
    print("=" * 80)

    for name, script in PIPELINE:
        run_script(name, script)

    total_duration = time.time() - total_start

    print("\n" + "=" * 80)
    print("SEMUA PROSES BERHASIL")
    print(f"Total waktu: {total_duration:.1f} detik")
    print("=" * 80)

    print("\nUntuk menjalankan dashboard:")
    print("streamlit run dashboard/app.py")


if __name__ == "__main__":
    main()