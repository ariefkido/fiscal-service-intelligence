import streamlit as st
import pandas as pd

DISPLAY_COLUMNS = {
    "topic": "Topic",
    "jumlah_tiket": "Tickets",
    "growth_rate": "Growth Rate",
    "emerging_index": "Emerging Index",
    "complexity_score": "Complexity",
    "volume_score": "Volume",
    "risk_score": "Risk",
    "diversity_score": "Diversity",
    "length_score": "Length",
    "watchlist_score": "Watchlist Score",
    "priority": "Rank",
}

from data_loader import (
    load_heatmap,
    load_emerging,
    load_complexity,
    load_risk_monitor,
    load_ikpa,
    load_realisasi,
    load_ikpa_leading,
    load_realisasi_leading,
    load_watchlist,
)
from charts import (
    plot_service_heatmap,
    plot_topic_comparison,
    plot_emerging_issues,
    plot_complexity_radar,
    plot_risk_monitor,
    plot_risk_distribution,
    plot_ikpa_trend,
    plot_realisasi_trend,
    build_executive_kpis,
    build_executive_summary,
    plot_leading_indicator,
    build_leading_indicator_summary,
    plot_watchlist,
    build_watchlist_summary,
    build_key_findings,
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Fiscal Service Intelligence",
    page_icon="📊",
    layout="wide",
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_all():
    heatmap_df           = load_heatmap()
    emerging_df          = load_emerging()
    complexity_df        = load_complexity()
    risk_df              = load_risk_monitor()
    ikpa_df              = load_ikpa()
    realisasi_df         = load_realisasi()
    ikpa_leading_df      = load_ikpa_leading()
    realisasi_leading_df = load_realisasi_leading()
    watchlist_df         = load_watchlist()

    return (
        heatmap_df,
        emerging_df,
        complexity_df,
        risk_df,
        ikpa_df,
        realisasi_df,
        ikpa_leading_df,
        realisasi_leading_df,
        watchlist_df,
    )


(
    heatmap_df,
    emerging_df,
    complexity_df,
    risk_df,
    ikpa_df,
    realisasi_df,
    ikpa_leading_df,
    realisasi_leading_df,
    watchlist_df,
) = load_all()

# =====================================================
# HEADER
# =====================================================

st.title("Fiscal Service Intelligence")
st.markdown(
    """
    Early Warning System berbasis pola interaksi layanan HAI DJPb
    untuk mendeteksi potensi risiko pelaksanaan anggaran sebelum
    tercermin pada indikator IKPA dan realisasi anggaran.
    """
)
st.divider()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Filter")

available_years = sorted(heatmap_df["tahun"].unique())
selected_year   = st.sidebar.selectbox("Tahun", available_years, index=len(available_years) - 1)

# =====================================================
# FILTER DATA
# =====================================================

heatmap_filtered   = heatmap_df[heatmap_df["tahun"]       == selected_year]
emerging_filtered  = emerging_df[emerging_df["tahun"]     == selected_year]
risk_filtered      = risk_df[risk_df["tahun"]             == selected_year]
ikpa_filtered      = ikpa_df[ikpa_df["tahun"]             == selected_year]
realisasi_filtered = realisasi_df[realisasi_df["tahun"]   == selected_year]

# =====================================================
# KPI
# =====================================================

kpis = build_executive_kpis(emerging_filtered, complexity_df, risk_filtered, heatmap_filtered)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tickets",      f"{kpis['total_tickets']:,}")
col2.metric("Top Emerging Issue", kpis["top_emerging"])
col3.metric("Most Complex Topic", kpis["most_complex"])
col4.metric("Current Risk",       kpis["latest_risk"])

st.divider()

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.subheader("📋 Executive Summary")
st.success(build_executive_summary(emerging_filtered, complexity_df, risk_filtered))
st.divider()

# =====================================================
# EXECUTIVE INSIGHT
# =====================================================

if kpis["latest_risk"] == "RED":
    recommendation = (
        "Risiko pelaksanaan anggaran berada pada level tinggi. "
        "Prioritaskan intervensi segera terhadap topik yang mengalami "
        "peningkatan tercepat dan memiliki kompleksitas tinggi."
    )
elif kpis["latest_risk"] == "YELLOW":
    recommendation = (
        "Risiko pelaksanaan anggaran menunjukkan peningkatan. "
        "Perkuat monitoring dan lakukan langkah mitigasi "
        "pada topik yang sedang berkembang."
    )
else:
    recommendation = (
        "Kondisi pelaksanaan anggaran relatif stabil. "
        "Pertahankan monitoring rutin dan fokus pada "
        "topik dengan kompleksitas tertinggi."
    )

st.info(
    f"""
### Executive Insight

**Top Emerging Issue:** {kpis["top_emerging"]}

**Most Complex Topic:** {kpis["most_complex"]}

**Current Risk Status:** {kpis["latest_risk"]}

### Recommendation

{recommendation}

FSI memanfaatkan pola interaksi layanan HAI DJPb
sebagai leading indicator untuk mendeteksi potensi
risiko pelaksanaan anggaran sebelum tercermin pada
indikator IKPA dan realisasi anggaran.
"""
)

# =====================================================
# EARLY WARNING WATCHLIST
# =====================================================

st.subheader("🛎 Early Warning Watchlist")
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(plot_watchlist(watchlist_df), use_container_width=True)
with col2:
    display_df = (
        watchlist_df[["priority", "topic", "watchlist_score"]]
        .head(10)
        .rename(columns=DISPLAY_COLUMNS)
    )
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
    )

st.warning(build_watchlist_summary(watchlist_df))
st.divider()

# =====================================================
# KEY FINDINGS
# =====================================================

st.subheader("📖 Key Findings & Recommendations")
for finding in build_key_findings(watchlist_df, ikpa_leading_df, realisasi_leading_df, risk_df):
    st.info(finding)
st.divider()

# =====================================================
# SERVICE HEATMAP
# =====================================================

st.subheader("🔥 Service Heatmap")
st.plotly_chart(plot_service_heatmap(heatmap_filtered), use_container_width=True)
st.divider()

# =====================================================
# TOPIC TREND COMPARISON
# =====================================================

st.subheader("📊 Topic Trend Comparison")

available_topics = sorted(heatmap_filtered["topic"].unique())
default_topics   = [t for t in ["SPAN", "SPM", "GPP"] if t in available_topics]

selected_trend_topics = st.multiselect(
    "Pilih Topik untuk Dibandingkan",
    available_topics,
    default=default_topics,
)

if selected_trend_topics:
    st.plotly_chart(
        plot_topic_comparison(heatmap_filtered, selected_trend_topics),
        use_container_width=True,
    )

st.divider()

# =====================================================
# TOP EMERGING ISSUES
# =====================================================

st.subheader("Top Emerging Issues")

latest_period = emerging_filtered["periode"].max()

top_emerging_df = (
    emerging_filtered[
        emerging_filtered["periode"] == latest_period
    ]
    .sort_values("emerging_index", ascending=False)
    .head(10)
)
emerging_cols   = ["topic", "jumlah_tiket", "growth_rate", "emerging_index"]

col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(plot_emerging_issues(top_emerging_df), use_container_width=True)
with col2:
    display_df = (
        top_emerging_df[emerging_cols]
        .copy()
        .rename(columns=DISPLAY_COLUMNS)
    )
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
    )

st.divider()

# =====================================================
# COMPLEXITY RADAR
# =====================================================

st.subheader("🎯 Complexity Radar Comparison")

selected_complexity_topics = st.multiselect(
    "Pilih Topik",
    sorted(complexity_df["topic"].unique()),
    default=["SPAN", "SPM", "GPP"],
)

complexity_cols = ["topic", "complexity_score", "volume_score", "risk_score", "diversity_score", "length_score"]

col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(
        plot_complexity_radar(complexity_df, selected_complexity_topics),
        use_container_width=True,
    )
with col2:
    comparison_df = (
        complexity_df[complexity_df["topic"].isin(selected_complexity_topics)][complexity_cols]
        .sort_values("complexity_score", ascending=False)
    )
    display_df = (
        comparison_df
        .copy()
        .rename(columns=DISPLAY_COLUMNS)
        .round(2)
    )
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
    )

st.divider()

# =====================================================
# LEADING INDICATOR ANALYSIS
# =====================================================

st.subheader("📎 Leading Indicator Analysis")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(
        plot_leading_indicator(ikpa_leading_df, "Top Topics vs IKPA"),
        use_container_width=True,
    )
with col2:
    st.plotly_chart(
        plot_leading_indicator(realisasi_leading_df, "Top Topics vs Realisasi"),
        use_container_width=True,
    )

st.info(build_leading_indicator_summary(ikpa_leading_df, realisasi_leading_df))
st.divider()

# =====================================================
# RISK MONITORING
# =====================================================

st.subheader("🚨 Risk Monitoring")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_risk_monitor(risk_filtered), use_container_width=True)
with col2:
    st.plotly_chart(plot_risk_distribution(risk_filtered), use_container_width=True)
    if "threshold_yellow" in risk_filtered.columns:
        st.caption(
            f"Yellow Threshold : {risk_filtered['threshold_yellow'].iloc[0]:.2f}\n\n"
            f"Red Threshold    : {risk_filtered['threshold_red'].iloc[0]:.2f}"
        )

st.divider()

# =====================================================
# OUTCOME INDICATORS
# =====================================================

st.subheader("📉 Outcome Indicators")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_ikpa_trend(ikpa_filtered), use_container_width=True)
with col2:
    st.plotly_chart(plot_realisasi_trend(realisasi_filtered), use_container_width=True)

st.divider()

# =====================================================
# RAW DATA
# =====================================================

with st.expander("Lihat Dataset Risiko"):
    st.dataframe(
        risk_filtered,
        hide_index=True,
        use_container_width=True,
    )

# =====================================================
# FOOTER
# =====================================================

st.caption(
    """
    Fiscal Service Intelligence (FSI)

    Dataset:
    - HAI DJPb 2020-2022
    - IKPA Kanwil DJPb Provinsi Jambi 2020-2022
    - Realisasi APBN Provinsi Jambi 2020-2022

    DJPb Data Analytics Competition (DDAC)
    """
)