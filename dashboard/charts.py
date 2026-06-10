import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# SERVICE HEATMAP
# =====================================================

def plot_service_heatmap(df):
    top_topics = (
        df.groupby("topic")["jumlah_tiket"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index
    )

    temp  = df[df["topic"].isin(top_topics)]
    pivot = temp.pivot_table(
        index="topic",
        columns="bulan",
        values="jumlah_tiket",
        aggfunc="sum",
        fill_value=0,
    )

    fig = px.imshow(
        pivot,
        aspect      = "auto",
        title       = "Service Heatmap",
        color_continuous_scale = [
            [0.0, "#00B050"],
            [0.5, "#FFD966"],
            [1.0, "#C00000"],
        ],
    )
    fig.update_layout(
        height=500,
        xaxis_title="Month",
        yaxis_title="Topic",
        coloraxis_colorbar_title="Tickets",
    )

    return fig

# =====================================================
# TOPIC TREND COMPARISON
# =====================================================

def plot_topic_comparison(df, selected_topics):
    temp = df[df["topic"].isin(selected_topics)].copy()

    fig = px.line(
        temp,
        x="periode",
        y="jumlah_tiket",
        color="topic",
        markers=True,
        title="Topic Trend Comparison",
    )
    fig.update_layout(height=500, xaxis_title="Periode", yaxis_title="Jumlah Tiket")

    return fig

# =====================================================
# EMERGING ISSUES
# =====================================================

def plot_emerging_issues(df):
    temp = df.copy()
    temp["emerging_index"] = temp["emerging_index"].fillna(0).clip(lower=0)
    temp = (
        temp.sort_values("emerging_index", ascending=False)
        .head(10)
        .sort_values("emerging_index", ascending=True)
    )

    fig = px.bar(
        temp,
        x="emerging_index",
        y="topic",
        orientation="h",
        text="emerging_index",
        title="Top Emerging Issues",
    )
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    fig.update_layout(height=500, xaxis_title="Emerging Index", yaxis_title="")

    return fig

# =====================================================
# COMPLEXITY RADAR COMPARISON
# =====================================================

def plot_complexity_radar(complexity_df, selected_topics):
    fig     = go.Figure()
    metrics = ["volume_score", "risk_score", "diversity_score", "length_score"]
    labels  = ["Volume", "Risk", "Diversity", "Length"]

    for topic in selected_topics:
        row = complexity_df[complexity_df["topic"] == topic]

        if len(row) == 0:
            continue

        row    = row.iloc[0]
        values = [row[m] for m in metrics]
        values += values[:1]
        theta   = labels + labels[:1]

        fig.add_trace(go.Scatterpolar(r=values, theta=theta, fill="toself", name=topic))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="Complexity Radar Comparison",
        height=600,
    )

    return fig

# =====================================================
# RISK MONITOR
# =====================================================

def plot_risk_monitor(df):
    fig = px.line(df, x="periode", y="risk_score", markers=True, title="Risk Monitoring Timeline")

    if "threshold_yellow" in df.columns and "threshold_red" in df.columns:
        fig.add_hline(y=df["threshold_yellow"].iloc[0], line_dash="dash", annotation_text="Yellow")
        fig.add_hline(y=df["threshold_red"].iloc[0],    line_dash="dash", annotation_text="Red")

    fig.update_layout(
        height=500,
        xaxis_title="Period",
        yaxis_title="Risk Score"
    )

    return fig

# =====================================================
# RISK DISTRIBUTION
# =====================================================

def plot_risk_distribution(df):
    summary         = df["risk_level"].value_counts().reset_index()
    summary.columns = ["risk_level", "count"]

    fig = px.pie(summary, names="risk_level", values="count", title="Risk Distribution")
    fig.update_layout(height=500)

    return fig

# =====================================================
# IKPA TREND
# =====================================================

def plot_ikpa_trend(df):
    fig = px.line(df, x="periode", y="ikpa_score", markers=True, title="IKPA Trend")

    fig.add_hline(y=95, line_dash="dash", annotation_text="Sangat Baik")
    fig.add_hline(y=89, line_dash="dot",  annotation_text="Baik")
    fig.add_hline(y=70, line_dash="dot",  annotation_text="Cukup")

    fig.update_layout(
        height=500,
        xaxis_title="Period",
        yaxis_title="IKPA Score"
    )

    return fig

# =====================================================
# REALISASI TREND
# =====================================================

def plot_realisasi_trend(df):
    fig = px.line(df, x="periode", y="realisasi_pct", markers=True, title="Realisasi Anggaran (%)")
    
    fig.update_layout(
        height=500,
        xaxis_title="Period",
        yaxis_title="Budget Realization (%)"
    )

    return fig

# =====================================================
# LEADING INDICATOR
# =====================================================

def plot_leading_indicator(df, title):
    temp = (
        df.sort_values("abs_correlation", ascending=False)
        .head(10)
        .sort_values("correlation")
    )

    fig = px.bar(
        temp,
        x="correlation",
        y="topic",
        color="direction",
        orientation="h",
        hover_data=["lag"],
        title=title,
        color_discrete_map={
            "Positive": "#00B050",  # hijau
            "Negative": "#C00000"   # merah
        }
    )
    fig.update_layout(height=500, xaxis_title="Correlation Strength", yaxis_title="")

    return fig

def build_leading_indicator_summary(ikpa_df, realisasi_df):
    ikpa_top = ikpa_df.sort_values("abs_correlation", ascending=False).iloc[0]
    real_top = realisasi_df.sort_values("abs_correlation", ascending=False).iloc[0]

    return (
        f"Topik **{ikpa_top['topic']}** memiliki hubungan terkuat terhadap IKPA "
        f"dengan korelasi **{ikpa_top['correlation']:.3f}** pada lag **{ikpa_top['lag']} bulan**. "
        f"Topik **{real_top['topic']}** memiliki hubungan terkuat terhadap realisasi anggaran "
        f"dengan korelasi **{real_top['correlation']:.3f}** pada lag **{real_top['lag']} bulan**. "
        "Temuan ini menunjukkan bahwa data layanan HAI DJPb mengandung sinyal operasional "
        "yang dapat dimanfaatkan sebagai leading indicator pelaksanaan anggaran."
    )

# =====================================================
# EXECUTIVE KPI
# =====================================================

def build_executive_kpis(emerging_df, complexity_df, risk_df, heatmap_df):
    total_tickets = heatmap_df["jumlah_tiket"].sum()
    total_topics  = heatmap_df["topic"].nunique()

    top_emerging = (
        emerging_df.sort_values("emerging_index", ascending=False).iloc[0]["topic"]
        if len(emerging_df) > 0 else "-"
    )

    most_complex = complexity_df.sort_values("complexity_score", ascending=False).iloc[0]["topic"]

    latest_risk = (
        risk_df.sort_values("periode").iloc[-1]["risk_level"]
        if len(risk_df) > 0 else "-"
    )

    return {
        "total_tickets": int(total_tickets),
        "total_topics":  int(total_topics),
        "top_emerging":  top_emerging,
        "most_complex":  most_complex,
        "latest_risk":   latest_risk,
    }

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def build_executive_summary(emerging_df, complexity_df, risk_df):
    if len(emerging_df) > 0:
        top_e          = emerging_df.sort_values("emerging_index", ascending=False).iloc[0]
        emerging_topic = top_e["topic"]
        emerging_index = top_e["emerging_index"]
    else:
        emerging_topic = "-"
        emerging_index = 0

    top_c         = complexity_df.sort_values("complexity_score", ascending=False).iloc[0]
    complex_topic = top_c["topic"]
    complex_score = top_c["complexity_score"]

    red_count    = (risk_df["risk_level"] == "RED").sum()
    yellow_count = (risk_df["risk_level"] == "YELLOW").sum()
    latest_risk  = risk_df.sort_values("periode").iloc[-1]["risk_level"]

    return (
        f"FSI mengidentifikasi {emerging_topic} sebagai isu yang mengalami "
        f"peningkatan paling signifikan sepanjang tahun dengan Emerging Index "
        f"sebesar {emerging_index:.0f} dan menjadi prioritas utama dalam Watchlist. "
        f"Di sisi lain, {complex_topic} merupakan topik dengan tingkat "
        f"kompleksitas layanan tertinggi (Complexity Score {complex_score:.0f}), "
        f"menunjukkan kebutuhan pendampingan yang lebih intensif.\n\n"
        f"Risk Monitoring mencatat {red_count} bulan RED dan "
        f"{yellow_count} bulan YELLOW, meskipun kondisi terkini berada "
        f"pada level {latest_risk}. Temuan ini menunjukkan bahwa risiko "
        f"operasional masih perlu diantisipasi melalui pembinaan dini pada "
        f"topik prioritas sebelum berdampak pada kualitas pelaksanaan anggaran."
    )

# =====================================================
# WATCHLIST
# =====================================================

def plot_watchlist(df):
    temp = df.head(10).sort_values("watchlist_score", ascending=True)

    fig = px.bar(
        temp,
        x="watchlist_score",
        y="topic",
        orientation="h",
        color="watchlist_score",
        color_continuous_scale="Reds",
        text="watchlist_score",
        title="Top Priority Topics",
    )
    fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig.update_layout(height=500, xaxis_title="Watchlist Score", yaxis_title="")

    return fig

def build_watchlist_summary(df):
    top  = df.iloc[0]
    top5 = ", ".join(df.head(5)["topic"].tolist())

    return (
        f"Topik dengan prioritas tertinggi saat ini adalah **{top['topic']}** "
        f"dengan Watchlist Score sebesar **{top['watchlist_score']:.2f}**. "
        f"Topik prioritas pembinaan saat ini meliputi: {top5}. "
        "Watchlist menggabungkan indikator Emerging Issues, Complexity Radar, "
        "dan Leading Indicator Analysis untuk membantu menentukan urutan "
        "intervensi yang perlu dilakukan terlebih dahulu."
    )

# =====================================================
# KEY FINDINGS
# =====================================================

def build_key_findings(watchlist_df, ikpa_leading_df, realisasi_leading_df, risk_df):
    top_watchlist = watchlist_df.iloc[0]
    top_ikpa      = ikpa_leading_df.sort_values("abs_correlation", ascending=False).iloc[0]
    top_realisasi = realisasi_leading_df.sort_values("abs_correlation", ascending=False).iloc[0]
    red_months    = (risk_df["risk_level"] == "RED").sum()
    yellow_months = (risk_df["risk_level"] == "YELLOW").sum()

    return [
        f"🔴 Prioritas utama saat ini adalah **{top_watchlist['topic']}** dengan Watchlist Score **{top_watchlist['watchlist_score']:.2f}**.",
        f"📉 Topik **{top_ikpa['topic']}** memiliki hubungan negatif terkuat terhadap IKPA ({top_ikpa['correlation']:.3f}).",
        f"⏳ Topik **{top_realisasi['topic']}** berkorelasi dengan perlambatan realisasi anggaran setelah {top_realisasi['lag']} bulan ({top_realisasi['correlation']:.3f}).",
        f"⚠️ Risk Monitor mencatat **{red_months} bulan RED** dan **{yellow_months} bulan YELLOW**.",
        "🎯 **Rekomendasi:** Fokuskan pembinaan pada topik prioritas Watchlist, khususnya yang berdampak terhadap IKPA dan realisasi.",
    ]