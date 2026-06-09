# Fiscal Service Intelligence (FSI)

## Overview

Fiscal Service Intelligence (FSI) merupakan solusi analitik berbasis data layanan HAI DJPb yang dirancang untuk mendeteksi potensi risiko pelaksanaan anggaran secara lebih dini. Proyek ini memanfaatkan pola interaksi layanan Help, Answer, Improve (HAI) DJPb sebagai sumber informasi strategis untuk mengidentifikasi permasalahan yang berkembang, mengukur tingkat kompleksitas layanan, serta memantau dampaknya terhadap kualitas pelaksanaan anggaran.

FSI mengubah data layanan yang sebelumnya bersifat operasional menjadi sistem pendukung keputusan berbasis data (data-driven decision support system) untuk membantu proses pembinaan satuan kerja secara lebih tepat sasaran.

---

## Background

HAI DJPb merupakan layanan helpdesk dan contact center resmi Direktorat Jenderal Perbendaharaan yang menerima pertanyaan, konsultasi, dan penyampaian informasi terkait pelaksanaan APBN.

Setiap interaksi layanan sebenarnya menyimpan sinyal operasional mengenai permasalahan yang sedang dihadapi satuan kerja. Namun, data tersebut umumnya dimanfaatkan untuk penyelesaian tiket secara individual dan belum digunakan secara optimal sebagai sumber intelijen organisasi.

Di sisi lain, kualitas pelaksanaan anggaran diukur melalui Indikator Kinerja Pelaksanaan Anggaran (IKPA) dan realisasi anggaran. Selama ini proses pembinaan sering dilakukan setelah permasalahan tercermin pada indikator kinerja, sehingga bersifat reaktif.

FSI dikembangkan untuk menjawab kebutuhan tersebut dengan memanfaatkan data layanan HAI sebagai leading indicator yang dapat memberikan sinyal dini sebelum permasalahan berdampak pada IKPA maupun realisasi anggaran.

---

## Problem Statement

Bagaimana memanfaatkan data layanan HAI DJPb untuk:

* Mengidentifikasi permasalahan yang paling sering dihadapi satuan kerja;
* Mengetahui topik layanan yang mengalami peningkatan signifikan;
* Mengukur tingkat kompleksitas permasalahan layanan;
* Mendeteksi hubungan antara permasalahan layanan dengan kualitas pelaksanaan anggaran;
* Menentukan prioritas pembinaan secara lebih objektif dan berbasis data.

---

## Objectives

1. Mengidentifikasi pola permasalahan layanan berdasarkan data HAI DJPb.
2. Mengukur tingkat kompleksitas masing-masing topik layanan.
3. Mendeteksi isu yang sedang berkembang (emerging issues).
4. Menghubungkan data layanan dengan IKPA dan realisasi anggaran.
5. Membangun sistem peringatan dini (early warning system) pelaksanaan anggaran.
6. Menyediakan rekomendasi prioritas pembinaan berbasis data.

---

## Data Sources

### 1. HAI DJPb

Periode: 2020–2022

Digunakan untuk:

* Topic Discovery
* Topic Classification
* Service Heatmap
* Emerging Issues Detection
* Complexity Analysis

### 2. IKPA

Periode: 2020–2022

Digunakan untuk:

* Analisis hubungan layanan dengan kualitas pelaksanaan anggaran
* Risk Monitoring
* Leading Indicator Analysis

### 3. Realisasi Anggaran

Periode: 2020–2022

Digunakan untuk:

* Monitoring outcome pelaksanaan anggaran
* Analisis dampak layanan terhadap realisasi anggaran

---

## Methodology

### Topic Discovery

Mengidentifikasi topik layanan utama berdasarkan analisis teks pada data tiket HAI.

Output:

* Topic Taxonomy
* Topic Classification Dictionary

---

### Service Heatmap

Menganalisis distribusi jumlah tiket berdasarkan topik dan periode.

Output:

* Topik dominan
* Pola musiman layanan
* Tren permasalahan

---

### Emerging Issues Detection

Mengidentifikasi topik yang mengalami peningkatan signifikan dibandingkan pola historis.

Output:

* Emerging Score
* Top Emerging Issues

---

### Complexity Radar

Mengukur kompleksitas setiap topik layanan berdasarkan:

* Volume tiket
* Keragaman subjek
* Panjang pesan
* Risiko operasional

Output:

* Complexity Score
* Complexity Radar

---

### Correlation Analysis

Mengukur hubungan antara volume permasalahan layanan dengan:

* Nilai IKPA
* Realisasi anggaran

Output:

* Correlation Score
* Impact Analysis

---

### Lag Correlation Analysis

Mengidentifikasi jeda waktu (lag) antara peningkatan permasalahan layanan dan dampaknya terhadap indikator pelaksanaan anggaran.

Output:

* Leading Indicator Analysis

---

### Risk Monitoring

Menggabungkan:

* Risiko layanan HAI
* Risiko IKPA
* Risiko realisasi anggaran

Output:

* Risk Score
* Risk Level
* Risk Timeline

---

### Early Warning Watchlist

Menentukan prioritas pembinaan berdasarkan kombinasi:

Watchlist Score =

30% Emerging Issues

40% Complexity

30% Impact Analysis

Output:

* Priority Ranking
* Critical Topics
* Early Warning Watchlist

---

## Solution Architecture

```text
HAI DJPb
     │
     ▼
Topic Discovery
     │
     ├── Service Heatmap
     ├── Emerging Issues
     ├── Complexity Radar
     │
     ▼
Correlation Analysis
     │
     ▼
Lag Correlation Analysis
     │
     ▼
Leading Indicator Analysis
     │
     ▼
Risk Monitoring
     │
     ▼
Early Warning Watchlist
     │
     ▼
Executive Dashboard
Executive Brief
```

---

## Key Findings

Berdasarkan hasil analisis:

* UP_TUP_GUP merupakan topik dengan prioritas tertinggi pada Early Warning Watchlist.
* SAKTI merupakan topik dengan tingkat kompleksitas tertinggi.
* Permasalahan UP_TUP_GUP memiliki hubungan negatif terkuat terhadap IKPA.
* Permasalahan SPM menunjukkan hubungan terkuat terhadap perlambatan realisasi anggaran dengan lag dua bulan.
* Data layanan HAI mengandung sinyal operasional yang dapat dimanfaatkan sebagai leading indicator pelaksanaan anggaran.

---

## Dashboard Features

### Executive Summary

Ringkasan kondisi pelaksanaan anggaran dan layanan.

### Early Warning Watchlist

Prioritas pembinaan berdasarkan kombinasi risiko, kompleksitas, dan dampak.

### Service Heatmap

Visualisasi distribusi layanan per topik dan periode.

### Topic Trend Comparison

Perbandingan tren beberapa topik layanan.

### Emerging Issues

Deteksi topik yang mengalami peningkatan signifikan.

### Complexity Radar

Visualisasi komponen pembentuk kompleksitas layanan.

### Leading Indicator Analysis

Hubungan antara layanan HAI dengan IKPA dan realisasi anggaran.

### Risk Monitoring

Monitoring risiko pelaksanaan anggaran secara berkala.

### Outcome Indicators

Pemantauan IKPA dan realisasi anggaran.

---

## Executive Reporting

FSI menyediakan:

* Executive Dashboard (Streamlit)
* Executive Brief (.txt)
* Executive Brief (.docx)

untuk mendukung pengambilan keputusan berbasis data.

---

## Technology Stack

* Python
* Pandas
* NumPy
* Plotly
* Streamlit
* PyArrow
* OpenPyXL
* Sastrawi
* Python-Docx

---

## Project Structure

```text
src
├── analytics
├── data_processing
├── feature_engineering
├── reporting
└── topic_engine

dashboard
data
```

---

## Expected Impact

### Organizational Impact

* Pembinaan satuan kerja lebih tepat sasaran.
* Deteksi dini risiko pelaksanaan anggaran.
* Pengambilan keputusan berbasis data.

### Operational Impact

* Identifikasi isu prioritas secara lebih cepat.
* Monitoring risiko yang lebih proaktif.
* Pemanfaatan data layanan sebagai sumber intelijen organisasi.

---

## Conclusion

Fiscal Service Intelligence membuktikan bahwa data layanan HAI DJPb tidak hanya berfungsi sebagai sarana konsultasi dan penyelesaian masalah, tetapi juga dapat dimanfaatkan sebagai sumber informasi strategis untuk mendeteksi potensi risiko pelaksanaan anggaran secara lebih dini.

Dengan mengintegrasikan analisis layanan, IKPA, dan realisasi anggaran, FSI menghasilkan sistem peringatan dini yang membantu organisasi menentukan prioritas pembinaan secara lebih efektif, objektif, dan berbasis data.

## Data

Dataset yang digunakan dalam pengembangan berasal dari data operasional internal DJPb dan tidak dapat dipublikasikan. Repository ini hanya menyediakan struktur data contoh untuk keperluan demonstrasi.