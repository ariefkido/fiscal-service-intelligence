from pathlib import Path
import pandas as pd

# =====================================================
# PROJECT ROOT
# =====================================================

ROOT        = Path(__file__).resolve().parents[1]
DATA_FOLDER = ROOT / "data" / "processed"

# =====================================================
# GENERIC LOADER
# =====================================================

def load_parquet(filename):
    file_path = DATA_FOLDER / filename

    if not file_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan:\n{file_path}")

    return pd.read_parquet(file_path)

def load_csv(filename):
    file_path = DATA_FOLDER / filename

    if not file_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan:\n{file_path}")

    return pd.read_csv(file_path)

# =====================================================
# SERVICE HEATMAP
# =====================================================

def load_heatmap():
    return load_parquet("heatmap_dataset.parquet")

# =====================================================
# EMERGING ISSUES
# =====================================================

def load_emerging():
    return load_parquet("emerging_issue_dataset.parquet")

# =====================================================
# COMPLEXITY RADAR
# =====================================================

def load_complexity():
    return load_parquet("complexity_radar.parquet")

# =====================================================
# RISK MONITOR
# =====================================================

def load_risk_monitor():
    return load_parquet("risk_monitor_dataset.parquet")

# =====================================================
# IKPA
# =====================================================

def load_ikpa():
    return load_parquet("ikpa_monthly.parquet")

def load_ikpa_leading():
    return load_csv("topic_ikpa_best_lag.csv")

# =====================================================
# REALISASI
# =====================================================

def load_realisasi():
    return load_parquet("realisasi_monthly.parquet")

def load_realisasi_leading():
    return load_csv("topic_realisasi_best_lag.csv")

# =====================================================
# WATCHLIST
# =====================================================

def load_watchlist():
    return load_parquet("watchlist_topics.parquet")

# =====================================================
# LOAD ALL
# =====================================================

def load_all_data():
    return {
        "heatmap":            load_heatmap(),
        "emerging":           load_emerging(),
        "complexity":         load_complexity(),
        "risk":               load_risk_monitor(),
        "ikpa":               load_ikpa(),
        "ikpa_leading":       load_ikpa_leading(),
        "realisasi":          load_realisasi(),
        "realisasi_leading":  load_realisasi_leading(),
        "watchlist":          load_watchlist(),
    }

# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":
    data = load_all_data()

    print("\nDATASETS LOADED\n")

    for name, df in data.items():
        print(f"{name:<20}{df.shape}")