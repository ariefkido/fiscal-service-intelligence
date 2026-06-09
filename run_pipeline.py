# run_pipeline.py

from pathlib import Path
import subprocess
import sys
import time

PROJECT_ROOT = Path(__file__).parent


# --- pipeline order ----------------------------------------------------------

PIPELINE = [
    # topic engine
    ("Topic Discovery",       "src/topic_engine/discover_topics.py"),
    ("Topic Classification",  "src/topic_engine/topic_classifier.py"),
    # data processing
    ("IKPA Processing",       "src/data_processing/ikpa_processor.py"),
    ("Realisasi Processing",  "src/data_processing/realisasi_processor.py"),
    # feature engineering
    ("Service Heatmap",       "src/feature_engineering/service_heatmap.py"),
    ("Emerging Issues",       "src/feature_engineering/emerging_issues.py"),
    ("Complexity Radar",      "src/feature_engineering/complexity_radar.py"),
    # analytics
    ("Correlation Analysis",      "src/analytics/correlation_analysis.py"),
    ("Lag Correlation Analysis",  "src/analytics/lag_correlation_analysis.py"),
    ("Risk Monitoring",           "src/analytics/risk_monitor.py"),
    ("Watchlist Analysis",        "src/analytics/watchlist_analysis.py"),
    # reporting
    ("Executive Brief",       "src/reporting/executive_brief.py"),
    ("Executive Brief DOCX",  "src/reporting/executive_brief_docx.py"),
]


# --- expected outputs --------------------------------------------------------

EXPECTED_OUTPUTS = {
    "Topic Discovery":       "outputs/topic_discovery/ticket_dataset.parquet",
    "Topic Classification":  "data/processed/topic_dataset.parquet",
    "IKPA Processing":       "data/processed/ikpa_monthly.parquet",
    "Realisasi Processing":  "data/processed/realisasi_monthly.parquet",
    "Service Heatmap":       "data/processed/heatmap_dataset.parquet",
    "Emerging Issues":       "data/processed/emerging_issue_dataset.parquet",
    "Complexity Radar":      "data/processed/complexity_radar.parquet",
    "Risk Monitoring":       "data/processed/risk_monitor_dataset.parquet",
    "Watchlist Analysis":    "data/processed/watchlist_topics.parquet",
}


# --- run script --------------------------------------------------------------

def run_script(name, script_path):
    script_file = PROJECT_ROOT / script_path
    if not script_file.exists():
        raise FileNotFoundError(f"Script tidak ditemukan:\n{script_file}")

    print(f"\n{'=' * 80}")
    print(f"RUNNING : {name}")
    print('=' * 80)

    start  = time.time()
    result = subprocess.run(
        [sys.executable, str(script_file)],
        cwd=PROJECT_ROOT, capture_output=True, text=True
    )
    duration = time.time() - start

    if result.returncode != 0:
        print("\nSTDOUT:"); print(result.stdout)
        print("\nSTDERR:"); print(result.stderr)
        raise RuntimeError(f"{name} gagal dijalankan (exit code {result.returncode})")

    if result.stdout:
        print(result.stdout)

    expected = EXPECTED_OUTPUTS.get(name)
    if expected:
        output_file = PROJECT_ROOT / expected
        if not output_file.exists():
            raise RuntimeError(f"{name} selesai tetapi output tidak ditemukan:\n{output_file}")
        print(f"Output OK : {output_file}")

    print(f"✓ Selesai ({duration:.1f} detik)")


# --- main --------------------------------------------------------------------

def main():
    total_start = time.time()

    print("=" * 80)
    print("FISCAL SERVICE INTELLIGENCE PIPELINE")
    print("=" * 80)
    print(f"\nProject Root:\n{PROJECT_ROOT}")

    for name, script in PIPELINE:
        run_script(name, script)

    total_duration = time.time() - total_start

    print(f"\n{'=' * 80}")
    print("SEMUA PROSES BERHASIL")
    print(f"{'=' * 80}")
    print(f"Total waktu : {total_duration:.1f} detik")
    print("\nOutput utama:")
    for output in EXPECTED_OUTPUTS.values():
        print(f"  {output}")
    print(f"\nUntuk menjalankan dashboard:")
    print(f"  {sys.executable} -m streamlit run dashboard/app.py")
    print("=" * 80)


if __name__ == "__main__":
    main()