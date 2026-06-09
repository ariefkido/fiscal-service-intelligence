from pathlib import Path
from collections import Counter
import pandas as pd
import re

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# =====================================================
# STOPWORDS
# =====================================================

def build_stopwords():
    factory    = StopWordRemoverFactory()
    stop_words = set(factory.get_stop_words())

    custom_stopwords = {
        # singkatan umum
        "yg", "dgn", "tdk", "sih", "ya", "jd", "nya", "krn", "klo", "utk", "dri",
        # sapaan
        "pak", "bu", "bapak", "ibu", "yth", "yth.",
        # institusi
        "hai", "djpb", "djpbn", "kemenkeu",
        # layanan
        "mohon", "tolong", "bantu", "permohonan", "informasi", "layanan",
        # tiket
        "tiket", "ticket", "nomor", "tanggal",
        # akun
        "user", "password",
        # noise
        "error", "kendala", "masalah",
        # email
        "email", "mail", "surat", "nbsp", "pengirim", "penerima",
        "jawaban", "disclaimer", "pendapat", "hukum", "elektronik",
        "feedback", "lampiran", "lampirannya",
        "semoga", "membantu", "terima", "kasih",
        "sampaikan", "menyampaikan",
        "helpdesk", "satker", "kppn",
    }

    stop_words.update(custom_stopwords)
    return stop_words

# =====================================================
# REMOVE EMAIL FOOTER
# =====================================================

def remove_email_footer(text):
    if pd.isna(text):
        return ""

    text = str(text)

    footer_patterns = [
        "pesan ini dan setiap lampirannya",
        "email ini mungkin berisi informasi",
        "informasi yang terkandung",
        "disclaimer",
        "pendapat yang disampaikan",
        "pesan elektronik ini",
        "mohon tidak membalas email ini",
        "this email",
        "the information contained",
        "intended recipient",
        "please do not reply",
        "confidential information",
    ]

    lower_text = text.lower()
    for pattern in footer_patterns:
        pos = lower_text.find(pattern)
        if pos != -1:
            text = text[:pos]
            break

    return text

# =====================================================
# SUBJECT CLEANER
# =====================================================

def clean_subject(text):
    if pd.isna(text):
        return ""

    text = str(text)
    text = re.sub(r"^(RE|FW|FWD)\s*:", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[.*?\]", "", text)
    text = " ".join(text.split())

    return text.strip()

# =====================================================
# TEXT CLEANER
# =====================================================

def clean_text(text, stop_words):
    if pd.isna(text):
        return ""

    text  = remove_email_footer(text)
    text  = str(text).lower()
    text  = re.sub(r"[^a-zA-Z\s]", " ", text)
    words = [w for w in text.split() if w not in stop_words and len(w) > 2]

    return " ".join(words)

# =====================================================
# BIGRAM
# =====================================================

def generate_bigrams(text):
    words = text.split()

    if len(words) < 2:
        return []

    return [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]

# =====================================================
# LOAD FILES
# =====================================================

def load_hai_files(raw_folder):
    files = sorted(Path(raw_folder).glob("sintetik_data_hai_*.xlsx"))

    if not files:
        raise FileNotFoundError(f"Tidak ditemukan file HAI:\n{raw_folder}")

    print(f"\nDitemukan {len(files)} file")

    dfs = []
    for file in files:
        print(f"Membaca {file.name}")
        df = pd.read_excel(file)
        df["source_file"] = file.stem
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

# =====================================================
# BUILD TICKET DATASET
# =====================================================

def build_ticket_dataset(df):
    print("\nMembentuk dataset tiket...")

    required_cols = ["ref_tiket", "tgl_tiket", "subject", "bidang", "pesan"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Kolom tidak ditemukan: {missing}")

    df["tgl_tiket"] = pd.to_datetime(df["tgl_tiket"], errors="coerce")

    tickets = (
        df.groupby("ref_tiket")
        .agg({
            "tgl_tiket": "min",
            "subject":   "first",
            "bidang":    lambda x: ", ".join(sorted(set(x.dropna().astype(str)))),
            "pesan":     lambda x: " ".join(x.dropna().astype(str)),
        })
        .reset_index()
    )

    tickets["tahun"]   = tickets["tgl_tiket"].dt.year
    tickets["bulan"]   = tickets["tgl_tiket"].dt.month
    tickets["periode"] = tickets["tgl_tiket"].dt.strftime("%Y-%m")

    return tickets

# =====================================================
# DISCOVERY
# =====================================================

def discover_topics(tickets, stop_words):
    print("\nCleaning subject...")
    tickets["subject_clean"] = tickets["subject"].apply(clean_subject)

    print("Cleaning message...")
    tickets["pesan_clean"] = tickets["pesan"].apply(lambda x: clean_text(x, stop_words))

    top_subjects         = tickets["subject_clean"].value_counts().reset_index()
    top_subjects.columns = ["subject", "jumlah_tiket"]

    all_words   = [w for text in tickets["pesan_clean"] for w in text.split()]
    top_keywords = pd.DataFrame(Counter(all_words).most_common(1000), columns=["keyword", "frequency"])
    top_keywords = top_keywords[top_keywords["frequency"] >= 20]

    all_bigrams = [b for text in tickets["pesan_clean"] for b in generate_bigrams(text)]
    top_bigrams = pd.DataFrame(Counter(all_bigrams).most_common(500), columns=["bigram", "frequency"])
    top_bigrams = top_bigrams[top_bigrams["frequency"] >= 10]

    top_bidang         = tickets["bidang"].value_counts().reset_index()
    top_bidang.columns = ["bidang", "jumlah_tiket"]

    return tickets, top_subjects, top_keywords, top_bigrams, top_bidang

# =====================================================
# SAVE OUTPUT
# =====================================================

def save_outputs(output_folder, tickets, top_subjects, top_keywords, top_bigrams, top_bidang):
    output_folder.mkdir(parents=True, exist_ok=True)

    top_subjects.to_csv(output_folder / "top_subjects.csv", index=False, encoding="utf-8-sig")
    top_keywords.to_csv(output_folder / "top_keywords.csv", index=False, encoding="utf-8-sig")
    top_bigrams.to_csv(output_folder / "top_bigrams.csv",   index=False, encoding="utf-8-sig")
    top_bidang.to_csv(output_folder / "top_bidang.csv",     index=False, encoding="utf-8-sig")
    tickets.to_parquet(output_folder / "ticket_dataset.parquet", index=False)

# =====================================================
# MAIN
# =====================================================

def main():
    root          = Path(__file__).resolve().parents[2]
    raw_folder    = root / "data" / "raw" / "Dataset HAI DJPb 2020-2022"
    output_folder = root / "outputs" / "topic_discovery"

    df = load_hai_files(raw_folder)
    print(f"\nTotal record : {len(df):,}")

    tickets = build_ticket_dataset(df)
    print(f"Total tiket : {len(tickets):,}")

    stop_words = build_stopwords()
    tickets, top_subjects, top_keywords, top_bigrams, top_bidang = discover_topics(tickets, stop_words)

    save_outputs(output_folder, tickets, top_subjects, top_keywords, top_bigrams, top_bidang)

    print("\nTOPIC DISCOVERY SELESAI")
    print(f"\nOutput:\n{output_folder}")


if __name__ == "__main__":
    main()