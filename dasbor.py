# ===========================================
# 🎓 DASHBOARD VISUALISASI ANALISIS MAHASISWA
# ===========================================

import streamlit as st
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# KONFIGURASI HALAMAN
# ==============================
st.set_page_config(
    page_title="Dashboard Analisis Mahasiswa",
    layout="wide",
    page_icon="🎓",
)
st.title("🎓 Dashboard Analisis Fenomena Last Minute Mahasiswa")

# ==============================
# BACA DATA OTOMATIS (TANPA UPLOAD)
# ==============================
try:
    df = pd.read_csv("data lastminute bersih.csv")
    df.columns = df.columns.str.strip()
    st.success("✅ Data berhasil dimuat otomatis!")

except FileNotFoundError:
    st.error("❌ File 'data lastminute bersih.csv' tidak ditemukan di folder yang sama dengan dashboard.py.")
    st.stop()

# ==============================
# DETEKSI TIPE DATA
# ==============================
num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

# Tabs untuk navigasi
tab_data, tab_viz = st.tabs(["📋 Data & Statistik", "📈 Visualisasi"])

# ==============================
# TAB 1: DATA & STATISTIK
# ==============================
with tab_data:
    st.subheader("📄 Preview Data")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("📊 Statistik Deskriptif")
    if num_cols:
        st.dataframe(df[num_cols].describe(), use_container_width=True)
    else:
        st.warning("Tidak ada kolom numerik untuk ditampilkan.")

    st.markdown("**Kolom Numerik:**")
    st.write(num_cols)
    st.markdown("**Kolom Kategorikal:**")
    st.write(cat_cols)

# ==============================
# TAB 2: VISUALISASI
# ==============================
with tab_viz:
    st.header("📊 Dashboard Visualisasi Data Mahasiswa")

    # --- RINGKASAN UMUM ---
    st.markdown("### 📌 Ringkasan Umum")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jumlah Responden", len(df))
    c2.metric("Kolom Numerik", len(num_cols))
    c3.metric("Kolom Kategorikal", len(cat_cols))
    c4.metric("Data Kosong", df.isna().sum().sum())

    st.divider()

    # ==============================
    # VISUALISASI 1: PIE & BAR CHART
    # ==============================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧩 Distribusi Kategorikal (Pie Chart)")
        if cat_cols:
            pie_col = st.selectbox("Pilih kolom kategori:", cat_cols, key="pie")
            pie_data = df[pie_col].value_counts().reset_index()
            pie_data.columns = [pie_col, "Jumlah"]
            fig_pie = px.pie(
                pie_data,
                names=pie_col,
                values="Jumlah",
                hole=0.4,
                title=f"Distribusi {pie_col}",
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("Tidak ada kolom kategorikal ditemukan.")

    with col2:
        st.subheader("📊 Frekuensi Kategorikal (Bar Chart)")
        if cat_cols:
            bar_col = st.selectbox("Pilih kolom kategori:", cat_cols, key="bar")
            bar_data = df[bar_col].value_counts().reset_index()
            bar_data.columns = [bar_col, "Jumlah"]
            fig_bar = px.bar(
                bar_data,
                x="Jumlah",
                y=bar_col,
                orientation="h",
                title=f"Frekuensi {bar_col}",
                color="Jumlah",
                color_continuous_scale="teal",
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Tidak ada kolom kategorikal ditemukan.")

    st.divider()

    # ==============================
    # VISUALISASI 2: LINE & BOX PLOT
    # ==============================
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📈 Tren Data Numerik (Line Chart)")
        if num_cols:
            line_col = st.selectbox("Pilih kolom numerik:", num_cols, key="line")
            fig_line = px.line(
                df,
                y=line_col,
                title=f"Tren Nilai {line_col}",
                markers=True,
                color_discrete_sequence=["#00CC96"],
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.warning("Tidak ada kolom numerik ditemukan.")

    with col4:
        st.subheader("📦 Distribusi Nilai (Box Plot)")
        if num_cols:
            box_col = st.selectbox("Pilih kolom numerik:", num_cols, key="box")
            fig_box = px.box(
                df,
                y=box_col,
                title=f"Distribusi {box_col}",
                points="all",
                color_discrete_sequence=["#636EFA"],
            )
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.warning("Tidak ada kolom numerik ditemukan.")

    st.divider()

    # ==============================
    # VISUALISASI 3: HISTOGRAM
    # ==============================
    st.subheader("📊 Distribusi Data (Histogram)")
    if num_cols:
        hist_col = st.selectbox("Pilih kolom numerik:", num_cols, key="hist")
        fig_hist = px.histogram(
            df,
            x=hist_col,
            nbins=20,
            title=f"Distribusi {hist_col}",
            color_discrete_sequence=["#EF553B"],
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.warning("Tidak ada kolom numerik ditemukan.")

    st.divider()

    # ==============================
    # VISUALISASI 4: HEATMAP KORELASI
    # ==============================
    st.subheader("🔥 Matriks Korelasi (Heatmap)")
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()

        n = len(corr.columns)
        fig, ax = plt.subplots(figsize=(min(12, n * 0.8), min(8, n * 0.6)))
        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            center=0,
            fmt=".2f",
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            square=True,
            ax=ax,
        )
        ax.set_title("Korelasi Antar Variabel Numerik", fontsize=14, pad=12)
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Tidak cukup kolom numerik untuk menampilkan korelasi.")

    st.caption("💡 Gunakan dropdown di setiap bagian untuk mengganti kolom yang divisualisasikan.")

