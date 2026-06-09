"""
=========================================================
TOPIC TAXONOMY
Fiscal Service Intelligence (FSI)

Versi: 1.0
=========================================================

Master taxonomy untuk klasifikasi tiket HAI.

Dipakai oleh:
- topic_classifier.py
- service_heatmap.py
- emerging_issue.py
- complexity_engine.py
- risk_monitor.py
"""

# =========================================================
# TOPIC TAXONOMY
# =========================================================

TOPIC_TAXONOMY = {

    # =====================================================
    # APLIKASI INTI
    # =====================================================

    "SAKTI": {
        "category":    "Aplikasi Inti",
        "risk_weight": 5,
        "keywords": [
            "sakti", "modul komitmen", "modul pembayaran", "modul bendahara",
            "persediaan", "aset tetap", "piutang", "utang",
            "implementasi sakti", "migrasi sakti",
            "user sakti", "akses sakti",
            "sakti web", "sakti desktop",
        ],
    },

    "OMSPAN": {
        "category":    "Aplikasi Inti",
        "risk_weight": 5,
        "keywords": [
            "omspan", "monitoring", "pelaporan omspan",
            "konfirmasi omspan", "rekon omspan", "akses omspan",
        ],
    },

    "SPAN": {
        "category":    "Aplikasi Inti",
        "risk_weight": 5,
        "keywords": [
            "span", "kode pembayaran", "data span",
        ],
    },

    "DIGIT": {
        "category":    "Aplikasi Inti",
        "risk_weight": 2,
        "keywords": [
            "digit", "reset password digit", "akun digit",
            "password digit", "registrasi digit", "login digit",
        ],
    },

    "GPP": {
        "category":    "Aplikasi Inti",
        "risk_weight": 2,
        "keywords": [
            "gpp", "aplikasi gpp", "gaji pegawai",
        ],
    },

    "SIMASPATEN": {
        "category":    "Aplikasi Inti",
        "risk_weight": 2,
        "keywords": ["simaspaten"],
    },

    # =====================================================
    # PELAKSANAAN ANGGARAN
    # =====================================================

    "SPM": {
        "category":    "Pelaksanaan Anggaran",
        "risk_weight": 4,
        "keywords": [
            "spm", "penolakan spm", "koreksi spm",
            "spm gaji", "spm ls", "spm gu", "spm tup",
        ],
    },

    "SP2D": {
        "category":    "Pelaksanaan Anggaran",
        "risk_weight": 4,
        "keywords": [
            "sp2d", "retur sp2d", "identifikasi pembayaran",
        ],
    },

    "REVISI_DIPA": {
        "category":    "Pelaksanaan Anggaran",
        "risk_weight": 4,
        "keywords": [
            "revisi dipa", "revisi anggaran",
            "halaman iii", "hal iii", "halaman 3", "revisi halaman iii",
        ],
    },

    "KONTRAK": {
        "category":    "Pelaksanaan Anggaran",
        "risk_weight": 3,
        "keywords": [
            "kontrak", "data kontrak", "addendum kontrak", "kontrak supplier",
        ],
    },

    "CAPAIAN_OUTPUT": {
        "category":    "Pelaksanaan Anggaran",
        "risk_weight": 4,
        "keywords": [
            "capaian output", "output kegiatan", "realisasi output",
        ],
    },

    # =====================================================
    # BENDAHARA & PEMBAYARAN
    # =====================================================

    "SUPPLIER": {
        "category":    "Bendahara & Pembayaran",
        "risk_weight": 3,
        "keywords": [
            "supplier", "data supplier", "rekening supplier", "perubahan rekening",
        ],
    },

    "LPJ_BENDAHARA": {
        "category":    "Bendahara & Pembayaran",
        "risk_weight": 2,
        "keywords": [
            "lpj", "lpj bendahara", "laporan pertanggungjawaban",
        ],
    },

    "UP_TUP_GUP": {
        "category":    "Bendahara & Pembayaran",
        "risk_weight": 3,
        "keywords": [
            "uang persediaan", "tambahan uang persediaan", "ganti uang persediaan",
            "up/tup", "up tup", "up gup",
            "surat up", "surat tup", "surat gup",
        ],
    },

    "MPN_G3": {
        "category":    "Bendahara & Pembayaran",
        "risk_weight": 2,
        "keywords": [
            "mpn", "mpn g3", "billing", "kode billing", "penerimaan negara",
        ],
    },

    # =====================================================
    # APLIKASI LAMA / TRANSISI
    # =====================================================

    "SAS": {
        "category":    "Aplikasi Legacy",
        "risk_weight": 2,
        "keywords": ["sas", "aplikasi sas"],
    },

    "PIN_PPSPM": {
        "category":    "Aplikasi Legacy",
        "risk_weight": 2,
        "keywords": ["pin ppspm", "ppspm"],
    },

    # =====================================================
    # LAINNYA
    # =====================================================

    "PMRT": {
        "category":    "Lainnya",
        "risk_weight": 1,
        "keywords": ["pmrt", "penghapusan pmrt"],
    },

    "LAINNYA": {
        "category":    "Lainnya",
        "risk_weight": 1,
        "keywords":    [],
    },
}

# =========================================================
# PRIORITY ORDER
#
# Jika satu tiket match lebih dari satu topik,
# classifier akan memilih topik dengan prioritas
# lebih tinggi.
# =========================================================

TOPIC_PRIORITY = [
    "SAKTI", "OMSPAN", "SPAN",
    "SPM", "SP2D", "REVISI_DIPA",
    "SUPPLIER", "KONTRAK", "CAPAIAN_OUTPUT",
    "LPJ_BENDAHARA", "UP_TUP_GUP",
    "DIGIT", "MPN_G3", "GPP",
    "SIMASPATEN", "SAS", "PIN_PPSPM",
    "PMRT", "LAINNYA",
]

# =========================================================
# HELPER
# =========================================================

ALL_TOPICS = list(TOPIC_TAXONOMY.keys())

TOPIC_CATEGORIES = sorted({item["category"] for item in TOPIC_TAXONOMY.values()})