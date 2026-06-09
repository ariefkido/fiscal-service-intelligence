import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd
import re

from topic_engine.topic_taxonomy import TOPIC_TAXONOMY, TOPIC_PRIORITY


# --- normalize text ----------------------------------------------------------

def normalize_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = " ".join(text.split())

    return text


# --- classify topic ----------------------------------------------------------

def classify_topic(subject, message):
    combined = f"{normalize_text(subject)} {normalize_text(message)}"

    for topic in TOPIC_PRIORITY:
        for keyword in TOPIC_TAXONOMY[topic]["keywords"]:
            if re.search(rf"\b{re.escape(keyword.lower())}\b", combined):
                return topic

    return "LAINNYA"


# --- load data ---------------------------------------------------------------

def load_ticket_dataset(file_path):
    print("\nLoading ticket dataset...")
    return pd.read_parquet(file_path)


# --- apply classification ----------------------------------------------------

def apply_classification(df):
    print("\nClassifying topics...")

    df["topic"] = df.apply(
        lambda row: classify_topic(
            row.get("subject_clean", ""),
            row.get("pesan_clean", "")
        ),
        axis=1
    )

    return df


# --- summary & coverage ------------------------------------------------------

def build_summary(df):
    summary         = df["topic"].value_counts().reset_index()
    summary.columns = ["topic", "jumlah_tiket"]
    summary["persentase"] = (summary["jumlah_tiket"] / len(df) * 100).round(2)
    return summary

def calculate_coverage(df):
    total         = len(df)
    uncategorized = (df["topic"] == "LAINNYA").sum()
    return round((total - uncategorized) / total * 100, 2)


# --- save output -------------------------------------------------------------

def save_output(output_folder, topic_df, summary_df):
    output_folder.mkdir(parents=True, exist_ok=True)

    public_df = topic_df.drop(columns=["subject", "pesan"], errors="ignore")
    public_df.to_parquet(output_folder / "topic_dataset.parquet", index=False)
    summary_df.to_csv(  output_folder / "topic_summary.csv",      index=False, encoding="utf-8-sig")


# --- main --------------------------------------------------------------------

def main():
    root          = Path(__file__).resolve().parents[2]
    input_file    = root / "outputs" / "topic_discovery" / "ticket_dataset.parquet"
    output_folder = root / "data" / "processed"

    df = load_ticket_dataset(input_file)
    print(f"Total tiket  : {len(df):,}")

    topic_df   = apply_classification(df)
    summary_df = build_summary(topic_df)
    coverage   = calculate_coverage(topic_df)

    save_output(output_folder, topic_df, summary_df)

    print(f"\nCoverage     : {coverage}%")
    print(f"Classified   : {coverage}%")
    print(f"Unclassified : {100 - coverage}%")
    print("\nTop Topics")
    print(summary_df.head(20))
    print(f"\nOutput:\n{output_folder}")


if __name__ == "__main__":
    main()