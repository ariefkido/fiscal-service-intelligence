from pathlib import Path
from collections import Counter
import pandas as pd
import re

# =====================================================
# CONFIG
# =====================================================

TOP_N_SUBJECTS   = 500
MIN_KEYWORD_FREQ = 20
MIN_BIGRAM_FREQ  = 10

# =====================================================
# CLEAN SUBJECT
# =====================================================

def clean_subject(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = " ".join(text.split())

    return text

# =====================================================
# BIGRAM
# =====================================================

def generate_bigrams(text):
    words = text.split()

    if len(words) < 2:
        return []

    return [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]

# =====================================================
# LOAD SUBJECT DATA
# =====================================================

def load_subject_data(file_path):
    return pd.read_csv(file_path).head(TOP_N_SUBJECTS)

# =====================================================
# EXTRACT KEYWORDS
# =====================================================

def extract_keywords(df):
    words   = [w for subject in df["subject"] for w in clean_subject(subject).split()]
    counter = Counter(words)

    result = pd.DataFrame(counter.most_common(), columns=["keyword", "frequency"])
    return result[result["frequency"] >= MIN_KEYWORD_FREQ]

# =====================================================
# EXTRACT BIGRAMS
# =====================================================

def extract_bigrams(df):
    bigrams = [b for subject in df["subject"] for b in generate_bigrams(clean_subject(subject))]
    counter = Counter(bigrams)

    result = pd.DataFrame(counter.most_common(), columns=["bigram", "frequency"])
    return result[result["frequency"] >= MIN_BIGRAM_FREQ]

# =====================================================
# BUILD CANDIDATE TOPICS
# =====================================================

def build_candidate_topics(keyword_df, bigram_df):
    candidate_patterns = {
        "SAKTI":          ["sakti"],
        "DIGIT":          ["digit"],
        "SPM":            ["spm"],
        "SP2D":           ["sp2d"],
        "SPAN":           ["span"],
        "OMSPAN":         ["omspan"],
        "SUPPLIER":       ["supplier"],
        "KONTRAK":        ["kontrak"],
        "LPJ_BENDAHARA":  ["lpj"],
        "CAPAIAN_OUTPUT": ["output"],
        "REVISI_DIPA":    ["revisi", "dipa"],
        "UP_TUP_GUP":     ["up", "tup", "gup"],
        "GPP":            ["gpp"],
        "MPN_G3":         ["mpn"],
        "SIMASPATEN":     ["simaspaten"],
        "PMRT":           ["pmrt"],
    }

    rows = []
    for topic, patterns in candidate_patterns.items():
        keyword_freq = keyword_df[keyword_df["keyword"].isin(patterns)]["frequency"].sum()
        bigram_freq  = bigram_df[
            bigram_df["bigram"].str.contains("|".join(patterns), case=False, na=False)
        ]["frequency"].sum()

        rows.append({
            "topic":             topic,
            "keyword_frequency": keyword_freq,
            "bigram_frequency":  bigram_freq,
            "candidate_score":   keyword_freq + bigram_freq,
        })

    return pd.DataFrame(rows).sort_values("candidate_score", ascending=False)

# =====================================================
# SAVE OUTPUTS
# =====================================================

def save_outputs(output_folder, candidate_subjects, candidate_keywords, candidate_bigrams, candidate_topics):
    output_folder.mkdir(parents=True, exist_ok=True)

    candidate_subjects.to_csv(output_folder / "candidate_subjects.csv", index=False, encoding="utf-8-sig")
    candidate_keywords.to_csv(output_folder / "candidate_keywords.csv", index=False, encoding="utf-8-sig")
    candidate_bigrams.to_csv(output_folder / "candidate_bigrams.csv",   index=False, encoding="utf-8-sig")
    candidate_topics.to_csv(output_folder / "candidate_topics.csv",     index=False, encoding="utf-8-sig")

    with pd.ExcelWriter(output_folder / "topic_summary.xlsx") as writer:
        candidate_subjects.to_excel(writer, sheet_name="Subjects",  index=False)
        candidate_keywords.to_excel(writer, sheet_name="Keywords",  index=False)
        candidate_bigrams.to_excel(writer,  sheet_name="Bigrams",   index=False)
        candidate_topics.to_excel(writer,   sheet_name="Topics",    index=False)

# =====================================================
# MAIN
# =====================================================

def main():
    root          = Path(__file__).resolve().parents[2]
    input_file    = root / "outputs" / "topic_discovery" / "top_subjects.csv"
    output_folder = root / "outputs" / "topic_candidates"

    print("\nLoading top_subjects...")
    subject_df = load_subject_data(input_file)

    print("Extracting keywords...")
    keyword_df = extract_keywords(subject_df)

    print("Extracting bigrams...")
    bigram_df = extract_bigrams(subject_df)

    print("Building topic candidates...")
    topic_df = build_candidate_topics(keyword_df, bigram_df)

    save_outputs(output_folder, subject_df, keyword_df, bigram_df, topic_df)

    print("\n=================================")
    print("TOPIC CANDIDATE EXTRACTION DONE")
    print(f"\nOutput:\n{output_folder}")
    print("\n=================================")


if __name__ == "__main__":
    main()