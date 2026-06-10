from pathlib import Path
import pandas as pd

PROJECT_ROOT  = Path(__file__).resolve().parents[2]
PROCESSED     = PROJECT_ROOT / "data" / "processed"

# =====================================================
# CONFIG
# =====================================================

EXCLUDE_TOPICS = ["LAINNYA"]

# =====================================================
# LOAD DATA
# =====================================================

def load_data():
    topic_df    = pd.read_parquet(PROCESSED / "topic_dataset.parquet")
    emerging_df = pd.read_parquet(PROCESSED / "emerging_issue_dataset.parquet")
    return topic_df, emerging_df

# =====================================================
# NORMALIZE
# =====================================================

def normalize(series):
    min_val = series.min()
    max_val = series.max()

    if max_val == min_val:
        return pd.Series([100] * len(series), index=series.index)

    return (series - min_val) / (max_val - min_val) * 100

# =====================================================
# SUBJECT DIVERSITY
# =====================================================

def build_subject_diversity(df):
    result         = df.groupby("topic")["subject_clean"].nunique().reset_index()
    result.columns = ["topic", "subject_diversity"]
    return result

# =====================================================
# MESSAGE LENGTH
# =====================================================

def build_message_length(df):
    temp = df.copy()
    temp["message_length"] = temp["pesan_clean"].fillna("").astype(str).str.split().str.len()

    result = temp.groupby("topic")["message_length"].mean().reset_index()
    return result

# =====================================================
# TOPIC VOLUME
# =====================================================

def build_topic_volume(df):
    result         = df["topic"].value_counts().reset_index()
    result.columns = ["topic", "ticket_volume"]
    return result

# =====================================================
# EMERGING RISK
# =====================================================

def build_emerging_risk(df):
    temp = df.copy()
    temp["emerging_score"] = temp["emerging_score"].clip(lower=0)

    result         = temp.groupby("topic")["emerging_score"].max().reset_index()
    result.columns = ["topic", "emerging_risk"]
    return result

# =====================================================
# BUILD COMPLEXITY SCORE
# =====================================================

def build_complexity_score(diversity_df, length_df, volume_df, risk_df):
    df = (
        diversity_df
        .merge(length_df, on="topic", how="outer")
        .merge(volume_df, on="topic", how="outer")
        .merge(risk_df,   on="topic", how="outer")
        .fillna(0)
    )

    df = df[~df["topic"].isin(EXCLUDE_TOPICS)]

    df["diversity_score"] = normalize(df["subject_diversity"])
    df["length_score"]    = normalize(df["message_length"])
    df["volume_score"]    = normalize(df["ticket_volume"])
    df["risk_score"]      = normalize(df["emerging_risk"])

    df["complexity_score"] = (
        0.40 * df["volume_score"]
        + 0.30 * df["risk_score"]
        + 0.20 * df["diversity_score"]
        + 0.10 * df["length_score"]
    ).round(2)

    return df.sort_values("complexity_score", ascending=False).reset_index(drop=True)

# =====================================================
# SAVE OUTPUT
# =====================================================

def save_outputs(df):
    PROCESSED.mkdir(parents=True, exist_ok=True)

    df.to_parquet(PROCESSED / "complexity_radar.parquet", index=False)
    df.to_csv(    PROCESSED / "complexity_radar.csv",     index=False, encoding="utf-8-sig")

# =====================================================
# MAIN
# =====================================================

def main():
    topic_df, emerging_df = load_data()

    diversity_df  = build_subject_diversity(topic_df)
    length_df     = build_message_length(topic_df)
    volume_df     = build_topic_volume(topic_df)
    risk_df       = build_emerging_risk(emerging_df)
    complexity_df = build_complexity_score(diversity_df, length_df, volume_df, risk_df)

    save_outputs(complexity_df)

    cols = ["topic", "complexity_score", "volume_score", "risk_score", "diversity_score", "length_score"]

    print("\nCOMPLEXITY RADAR DONE")
    print("\nTOP 15 COMPLEX TOPICS\n")
    print(complexity_df[cols].head(15))
    print(f"\nOutput:\n{PROCESSED}")


if __name__ == "__main__":
    main()