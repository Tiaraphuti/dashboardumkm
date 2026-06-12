import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Dashboard Profil UMKM",
    page_icon="📊",
    layout="wide"
)

# =====================================
# LOAD DATA
# =====================================
@st.cache_data
def load_data():
    df = pd.read_excel("data_umkm_clean.xlsx")

    # Convert datetime
    df["Waktu Profiling"] = pd.to_datetime(
        df["Waktu Profiling"],
        dayfirst=True,
        errors="coerce"
    )

    return df


df = load_data()

# =====================================
# SIDEBAR
# =====================================
st.sidebar.title("⚙️ Settings")

# tanggal min & max
min_date = df["Waktu Profiling"].min().date()
max_date = df["Waktu Profiling"].max().date()

# start date
start_date = st.sidebar.date_input(
    "Start date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

# end date
end_date = st.sidebar.date_input(
    "End date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

# timeframe
time_frame = st.sidebar.selectbox(
    "Select time frame",
    ["Daily", "Weekly", "Monthly"]
)

# chart sektor usaha
chart_type = st.sidebar.selectbox(
    "Select a chart type",
    ["Bar", "Pie"]
)

# =====================================
# FILTER DATA
# =====================================
filtered_df = df[
    (df["Waktu Profiling"].dt.date >= start_date) &
    (df["Waktu Profiling"].dt.date <= end_date)
]

# =====================================
# TITLE
# =====================================
st.title("📊 Dashboard Profil UMKM")
st.markdown("Visualisasi Profil Pelaku UMKM")

st.divider()

# =====================================
# KPI
# =====================================
total_umkm = len(filtered_df)

total_sektor = filtered_df[
    "Sektor Usaha"
].nunique()

total_produk = (
    filtered_df["Produk Jasa"] == "Produk"
).sum()

total_jasa = (
    filtered_df["Produk Jasa"] == "Jasa"
).sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total UMKM",
        f"{total_umkm:,}"
    )

with col2:
    st.metric(
        "Jumlah Sektor",
        total_sektor
    )

with col3:
    st.metric(
        "Produk",
        total_produk
    )

with col4:
    st.metric(
        "Jasa",
        total_jasa
    )

st.divider()

# =====================================
# PREPARE DATA
# =====================================

# gender
gender = (
    filtered_df["Jenis Kelamin"]
    .value_counts()
    .reset_index()
)
gender.columns = [
    "Jenis Kelamin",
    "Jumlah"
]

# produk jasa
produk = (
    filtered_df["Produk Jasa"]
    .value_counts()
    .reset_index()
)
produk.columns = [
    "Produk Jasa",
    "Jumlah"
]

# sektor usaha
sektor = (
    filtered_df["Sektor Usaha"]
    .value_counts()
    .reset_index()
)
sektor.columns = [
    "Sektor Usaha",
    "Jumlah"
]

# =====================================
# PIE CHARTS
# =====================================
col1, col2 = st.columns(2)

# gender
with col1:

    fig_gender = px.pie(
        gender,
        names="Jenis Kelamin",
        values="Jumlah",
        title="Distribusi Jenis Kelamin",
        hole=0.35
    )

    fig_gender.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_gender,
        use_container_width=True
    )

# produk jasa
with col2:

    fig_produk = px.pie(
        produk,
        names="Produk Jasa",
        values="Jumlah",
        title="Distribusi Produk / Jasa",
        hole=0.55
    )

    fig_produk.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_produk,
        use_container_width=True
    )

# =====================================
# TREND PROFILING
# =====================================
st.markdown("---")
st.markdown(
    """
    <div style="
        background-color:#E5E5E5;
        padding:10px;
        border:1px solid #CFCFCF;
        text-align:center;
        font-size:28px;
        font-weight:bold;
        border-radius:6px;
    ">
        TREND PROFILING
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

trend_df = filtered_df.copy()

# grouping berdasarkan timeframe
if time_frame == "Daily":

    trend_df["Periode"] = (
        trend_df["Waktu Profiling"]
        .dt.floor("D")
    )

elif time_frame == "Weekly":

    trend_df["Periode"] = (
        trend_df["Waktu Profiling"]
        .dt.to_period("W")
        .dt.start_time
    )

elif time_frame == "Monthly":

    trend_df["Periode"] = (
        trend_df["Waktu Profiling"]
        .dt.to_period("M")
        .dt.start_time
    )

# group data
trend = (
    trend_df
    .groupby("Periode")
    .size()
    .reset_index(name="Jumlah")
    .sort_values("Periode")
)

# chart
fig_trend = px.area(
    trend,
    x="Periode",
    y="Jumlah",
    markers=True,
    title=f"Trend Profiling ({time_frame})"
)

# format tampilan tanggal
if time_frame == "Daily":
    fig_trend.update_xaxes(
        tickformat="%d %b %Y"
    )

elif time_frame == "Weekly":
    fig_trend.update_xaxes(
        tickformat="%d %b %Y"
    )

elif time_frame == "Monthly":
    fig_trend.update_xaxes(
        tickformat="%b %Y"
    )

fig_trend.update_layout(
    xaxis_title="Periode",
    yaxis_title="Jumlah Profiling"
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

# =====================================
# VISUALISASI HASIL KELAS UMKM
# =====================================
st.markdown("---")
st.markdown(
    """
    <div style="
        background-color:#E5E5E5;
        padding:10px;
        border:1px solid #CFCFCF;
        text-align:center;
        font-size:28px;
        font-weight:bold;
        border-radius:6px;
    ">
        DISTRIBUSI HASIL KELAS UMKM
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)
# hitung jumlah tiap kelas
hasil = (
    filtered_df["Hasil"]
    .value_counts()
    .reset_index()
)

hasil.columns = [
    "Hasil",
    "Jumlah"
]

# urutan kelas biar tidak random
kelas_order = [
    "Kelas 1 - FOUNDATION BUILDERS",
    "Kelas 2 - BRANDING ENTHUSIASTS",
    "Kelas 3 - COMMERCE OPTIMIZERS",
    "Kelas 4 - SUSTAINABLE ADVOCATES"
]

hasil["Hasil"] = pd.Categorical(
    hasil["Hasil"],
    categories=kelas_order,
    ordered=True
)

hasil = hasil.sort_values("Hasil")

# chart
fig_hasil = px.bar(
    hasil,
    x="Jumlah",
    y="Hasil",
    orientation="h",
    text="Jumlah",
    title="Distribusi Hasil Profiling UMKM"
)

fig_hasil.update_layout(
    xaxis_title="Jumlah UMKM",
    yaxis_title="Kategori Hasil"
)

fig_hasil.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_hasil,
    use_container_width=True
)

# =====================================
# DISTRIBUSI SEKTOR USAHA
# =====================================
st.markdown("---")
st.markdown(
    """
    <div style="
        background-color:#E5E5E5;
        padding:10px;
        border:1px solid #CFCFCF;
        text-align:center;
        font-size:28px;
        font-weight:bold;
        border-radius:6px;
    ">
        DISTRIBUSI SEKTOR USAHA
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

if chart_type == "Bar":

    fig_sektor = px.bar(
        sektor,
        x="Jumlah",
        y="Sektor Usaha",
        orientation="h",
        text="Jumlah"
    )

    fig_sektor.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        ),
        xaxis_title="Jumlah UMKM",
        yaxis_title="Sektor Usaha"
    )

    fig_sektor.update_traces(
        textposition="outside"
    )

else:

    fig_sektor = px.pie(
        sektor,
        names="Sektor Usaha",
        values="Jumlah",
        hole=0.4
    )

    fig_sektor.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

st.plotly_chart(
    fig_sektor,
    use_container_width=True
)


# =====================================
# HELPER FUNCTION DONUT CHART
# =====================================
def create_donut_chart(
    dataframe,
    column_name,
    title,
    category_order=None
):

    data = (
        dataframe[column_name]
        .value_counts()
        .reset_index()
    )

    data.columns = [
        column_name,
        "Jumlah"
    ]

    # custom order
    if category_order:
        data[column_name] = pd.Categorical(
            data[column_name],
            categories=category_order,
            ordered=True
        )

        data = data.sort_values(
            column_name
        )

    fig = px.pie(
        data,
        names=column_name,
        values="Jumlah",
        hole=0.55,
        title=title
    )

    fig.update_traces(
        textinfo="percent",
        textposition="inside"
    )

    fig.update_layout(
        legend_title="",
        height=320,
        margin=dict(
            t=50,
            b=20,
            l=20,
            r=20
        )
    )

    return fig


# =====================================
# PSIKOGRAFI
# =====================================
st.markdown("---")
st.markdown(
    """
    <div style="
        background-color:#E5E5E5;
        padding:10px;
        border:1px solid #CFCFCF;
        text-align:center;
        font-size:28px;
        font-weight:bold;
        border-radius:6px;
    ">
        PSIKOGRAFI
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# 1. Motif Wirausaha
motif_order = [
    "Memanfaatkan peluang yang ada",
    "Menjadi sumber pendapatan utama untuk menopang kebutuhan hidup",
    "Melakukan perluasan usaha ke pasar regional, global, dan lainnya",
    "Menjadi sumber pendapatan tambahan",
    "Lainnya"
]

with col1:
    fig = create_donut_chart(
        filtered_df,
        "Motif Wirausaha",
        "Motif Wirausaha",
        motif_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 2. Alasan Memilih Bidang Usaha
alasan_order = [
    "Kejelasan pasar dan kebutuhan konsumen",
    "Kondisi persaingan dan peluang",
    "Kemampuan dan keinginan pribadi"
]

with col2:
    fig = create_donut_chart(
        filtered_df,
        "Alasan Memilih Bidang Usaha",
        "Alasan Memilih Usaha",
        alasan_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 3. Sikap Terhadap Resiko
col3, _ = st.columns([1, 1])

resiko_order = [
    "Mengambil risiko dengan penuh pertimbangan",
    "Selalu mengambil risiko untuk memanfaatkan peluang",
    "Cenderung menghindari risiko"
]

with col3:
    fig = create_donut_chart(
        filtered_df,
        "Sikap Terhadap Resiko",
        "Sikap Terhadap Resiko",
        resiko_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================
# SEKTOR INTERNAL
# =====================================
st.markdown("---")

st.markdown(
    """
    <div style="
        background-color:#E5E5E5;
        padding:10px;
        border:1px solid #CFCFCF;
        text-align:center;
        font-size:28px;
        font-weight:bold;
        border-radius:6px;
    ">
        SEKTOR INTERNAL
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# 1. Jumlah SDM Bergaji Tetap
sdm_order = [
    "<2 orang",
    "2-10 orang",
    "11-50 orang",
    ">50 orang"
]

with col1:
    fig = create_donut_chart(
        filtered_df,
        "Jumlah SDM Bergaji Tetap",
        "Jumlah SDM Bergaji Tetap",
        sdm_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 2. Sumber Bahan Baku
bahan_order = [
    "Pasar",
    "Langganan",
    "Langganan tetap (berkontrak)",
    "Lainnya"
]

with col2:
    fig = create_donut_chart(
        filtered_df,
        "Sumber Bahan Baku",
        "Sumber Bahan Baku",
        bahan_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# row kedua
col3, col4 = st.columns(2)

# 3. Metode Produksi
metode_order = [
    "Proses produksi masih menggunakan cara manual",
    "Proses produksi sudah menggunakan bantuan mesin",
    "Proses produksi sudah mengikuti Standard Operating Procedure (SOP)"
]

with col3:
    fig = create_donut_chart(
        filtered_df,
        "Metode Produksi",
        "Metode Produksi",
        metode_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 4. Pengalaman Pelatihan
pelatihan_order = [
    "1 Kali",
    "2 Kali",
    "3 Kali",
    ">3 Kali",
    "Lainnya"
]

with col4:
    fig = create_donut_chart(
        filtered_df,
        "Pengalaman Pelatihan",
        "Pengalaman Pelatihan",
        pelatihan_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================
# PASAR
# =====================================
st.markdown("---")

st.markdown(
    """
    <div style="
        background-color:#E5E5E5;
        padding:10px;
        border:1px solid #CFCFCF;
        text-align:center;
        font-size:28px;
        font-weight:bold;
        border-radius:6px;
    ">
        PASAR
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# ROW 1
# =====================================
col1, col2 = st.columns(2)

# 1. Outlet
outlet_order = [
    "Memiliki/menggunakan keduanya",
    "Hanya toko offline (fisik) saja",
    "Hanya toko online saja"
]

with col1:
    fig = create_donut_chart(
        filtered_df,
        "Outlet",
        "Outlet",
        outlet_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 2. Pemahaman Atas Pesaing
pesaing_order = [
    "Mengetahui lebih dari 1 (satu) pesaing terdekat dan harga produk/jasanya",
    "Mengetahui pesaing terdekat dan harga produk/jasanya",
    "Mengetahui pesaing terdekat, namun tidak mengetahui harga produk/jasanya",
    "Tidak mengetahui pesaing terdekat dan harga produk/jasanya sama sekali"
]

with col2:
    fig = create_donut_chart(
        filtered_df,
        "Pemahaman Atas Pesaing",
        "Pemahaman Atas Pesaing",
        pesaing_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================
# ROW 2
# =====================================
col3, col4 = st.columns(2)

# 3. Order Subkontrak Masuk
masuk_order = [
    "Tidak menerima",
    "Menerima"
]

with col3:
    fig = create_donut_chart(
        filtered_df,
        "Order Subkontrak Masuk",
        "Order Sub-kontrak Masuk",
        masuk_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 4. Order Subkontrak Keluar
keluar_order = [
    "Tidak memberikan",
    "Memberikan"
]

with col4:
    fig = create_donut_chart(
        filtered_df,
        "Order Subkontrak Keluar",
        "Order Sub-kontrak Keluar",
        keluar_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================
# ROW 3
# =====================================
col5, col6 = st.columns(2)

# 5. Cakupan Pasar
cakupan_order = [
    "Lokal",
    "Regional",
    "Nasional",
    "Global"
]

with col5:
    fig = create_donut_chart(
        filtered_df,
        "Cakupan Pasar",
        "Cakupan Pasar",
        cakupan_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 6. Pengalaman Pameran
pameran_order = [
    "Belum Pernah",
    "Lokal",
    "Regional",
    "Nasional"
]

with col6:
    fig = create_donut_chart(
        filtered_df,
        "Pengalaman Pameran",
        "Pengalaman Pameran",
        pameran_order
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================
# BRANDING
# =====================================
st.markdown("---")

st.markdown(
    """
    <div style="
        background-color:#E5E5E5;
        padding:10px;
        border:1px solid #CFCFCF;
        text-align:center;
        font-size:28px;
        font-weight:bold;
        border-radius:6px;
    ">
        BRANDING
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# HITUNG MULTI SELECT BRANDING
# =====================================

branding_col = (
    filtered_df["Branding"]
    .fillna("-")
    .astype(str)
)

jumlah_merek = branding_col.str.contains(
    "Nama Merek",
    case=False,
    na=False
).sum()

jumlah_logo = branding_col.str.contains(
    "Logo",
    case=False,
    na=False
).sum()

jumlah_kemasan = branding_col.str.contains(
    "Kemasan",
    case=False,
    na=False
).sum()

jumlah_hki = branding_col.str.contains(
    "HKI",
    case=False,
    na=False
).sum()

# dataframe branding
branding_df = pd.DataFrame({
    "Kategori": [
        "Nama Merek",
        "Logo",
        "Kemasan",
        "HKI"
    ],
    "Jumlah": [
        jumlah_merek,
        jumlah_logo,
        jumlah_kemasan,
        jumlah_hki
    ]
})

# =====================================
# KPI CARDS
# =====================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Nama Merek",
        f"{jumlah_merek:,}"
    )

with col2:
    st.metric(
        "Logo",
        f"{jumlah_logo:,}"
    )

with col3:
    st.metric(
        "Kemasan",
        f"{jumlah_kemasan:,}"
        )

with col4:
    st.metric(
        "HKI",
        f"{jumlah_hki:,}"
    )

# =====================================
# BAR CHART BRANDING
# =====================================
fig_branding = px.bar(
    
    branding_df,
    x="Jumlah",
    y="Kategori",
    orientation="h",
    text="Jumlah",
    title="Kepemilikan Branding UMKM"
)

fig_branding.update_layout(
    yaxis=dict(
        categoryorder="total ascending"
    ),
    xaxis_title="Jumlah UMKM",
    yaxis_title=""
)

fig_branding.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_branding,
    use_container_width=True
)

# =====================================
# DIGITALISASI
# =====================================
st.markdown("---")

st.markdown(
    """
    <div style="
        background-color:#E5E5E5;
        padding:10px;
        border:1px solid #CFCFCF;
        text-align:center;
        font-size:28px;
        font-weight:bold;
        border-radius:6px;
    ">
        DIGITALISASI
    </div>
    """,
    unsafe_allow_html=True
)


# =====================================
# HELPER FUNCTION MULTI CHECKLIST
# =====================================
def count_multiselect(
    dataframe,
    column_name,
    categories
):
    col = (
        dataframe[column_name]
        .fillna("-")
        .astype(str)
    )

    result = {}

    for item in categories:
        result[item] = col.str.contains(
            item,
            case=False,
            na=False
        ).sum()

    return pd.DataFrame({
        "Kategori": result.keys(),
        "Jumlah": result.values()
    })


# =====================================
# MEDIA SOSIAL
# =====================================
media_social = [
    "Whatsapp messenger",
    "Whatsapp business",
    "Facebook",
    "Instagram",
    "Youtube",
    "TikTok",
    "Google My Business"
]

media_df = count_multiselect(
    filtered_df,
    "Media Sosial",
    media_social
)

media_df = media_df.sort_values(
    "Jumlah",
    ascending=True
)

# =====================================
# MARKETPLACE
# =====================================
marketplace = [
    "Padi UMKM",
    "Tokopedia",
    "Shopee",
    "Bukalapak",
    "Lazada",
    "Tiktok Shop"
]

marketplace_df = count_multiselect(
    filtered_df,
    "Marketplace",
    marketplace
)

marketplace_df = marketplace_df.sort_values(
    "Jumlah",
    ascending=True
)

# =====================================
# POS
# =====================================
pos = [
    "Kasir Aja",
    "Qasir",
    "MokaPOS",
    "Majoo",
    "Odoo"
]

pos_df = count_multiselect(
    filtered_df,
    "POS (Aplikasi Point Of Sale)",
    pos
)

# gabungkan semua selain kasir aja
pos_total = pd.DataFrame({
    "Kategori": [
        "Kasir Aja",
        "Qasir/MokaPOS/Majoo/Odoo"
    ],
    "Jumlah": [
        pos_df[
            pos_df["Kategori"] ==
            "Kasir Aja"
        ]["Jumlah"].sum(),

        pos_df[
            pos_df["Kategori"] !=
            "Kasir Aja"
        ]["Jumlah"].sum()
    ]
})

# =====================================
# VISUALISASI
# =====================================
col1, col2 = st.columns(2)

# MEDIA SOSIAL
with col1:

    st.subheader(
        "Media Sosial"
    )

    fig_media = px.bar(
        media_df,
        x="Jumlah",
        y="Kategori",
        orientation="h",
        text="Jumlah"
    )

    fig_media.update_traces(
        textposition="outside"
    )

    fig_media.update_layout(
        height=420,
        yaxis_title="",
        xaxis_title="Jumlah UMKM"
    )

    st.plotly_chart(
        fig_media,
        use_container_width=True
    )

# MARKETPLACE
with col2:

    st.subheader(
        "Marketplace"
    )

    fig_market = px.bar(
        marketplace_df,
        x="Jumlah",
        y="Kategori",
        orientation="h",
        text="Jumlah"
    )

    fig_market.update_traces(
        textposition="outside"
    )

    fig_market.update_layout(
        height=420,
        yaxis_title="",
        xaxis_title="Jumlah UMKM"
    )

    st.plotly_chart(
        fig_market,
        use_container_width=True
    )

# POS
st.subheader(
    "Point Of Sale (POS)"
)

col3, col4 = st.columns(2)

with col3:
    st.metric(
        "Kasir Aja",
        int(pos_total.iloc[0]["Jumlah"])
    )

with col4:
    st.metric(
        "Qasir / MokaPOS / Majoo / Odoo",
        int(pos_total.iloc[1]["Jumlah"])
    )

fig_pos = px.bar(
    pos_total,
    x="Jumlah",
    y="Kategori",
    orientation="h",
    text="Jumlah"
)

fig_pos.update_traces(
    textposition="outside"
)

fig_pos.update_layout(
    yaxis_title="",
    xaxis_title="Jumlah UMKM",
    height=300
)

st.plotly_chart(
    fig_pos,
    use_container_width=True
)


# =====================================
# LEGALTAS & SERTIFIKASI
# =====================================
st.markdown("---")

st.markdown(
    """
    <div style="
        background-color:#E5E5E5;
        padding:10px;
        border:1px solid #CFCFCF;
        text-align:center;
        font-size:28px;
        font-weight:bold;
        border-radius:6px;
    ">
        LEGALITAS & SERTIFIKASI
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# LEGALTAS USAHA
# =====================================
legalitas_items = [
    "SKU",
    "IUMK",
    "NIB",
    "BPOM",
    "SIUP",
    "TDP",
    "Belum ada legalitas usaha"
]

legalitas_df = count_multiselect(
    filtered_df,
    "Legalitas Usaha",
    legalitas_items
)

legalitas_df = legalitas_df.sort_values(
    "Jumlah",
    ascending=True
)

# =====================================
# SERTIFIKASI USAHA
# =====================================
sertifikasi_items = [
    "SPP-PIRT",
    "Haki",
    "Halal",
    "Ekspor",
    "Belum ada sertifikasi usaha"
]

sertifikasi_df = count_multiselect(
    filtered_df,
    "Sertifikasi Usaha",
    sertifikasi_items
)

sertifikasi_df = sertifikasi_df.sort_values(
    "Jumlah",
    ascending=True
)

# =====================================
# KPI SUMMARY
# =====================================
col1, col2 = st.columns(2)

with col1:
    total_legalitas = (
        legalitas_df["Jumlah"]
        .sum()
    )

    st.metric(
        "Total Legalitas",
        f"{int(total_legalitas):,}"
    )

with col2:
    total_sertifikasi = (
        sertifikasi_df["Jumlah"]
        .sum()
    )

    st.metric(
        "Total Sertifikasi",
        f"{int(total_sertifikasi):,}"
    )

# =====================================
# CHARTS
# =====================================
col1, col2 = st.columns(2)

# LEGALTAS
with col1:

    st.subheader(
        "Legalitas Usaha"
    )

    fig_legalitas = px.bar(
        legalitas_df,
        x="Jumlah",
        y="Kategori",
        orientation="h",
        text="Jumlah"
    )

    fig_legalitas.update_traces(
        textposition="outside"
    )

    fig_legalitas.update_layout(
        yaxis_title="",
        xaxis_title="Jumlah UMKM",
        height=450
    )

    st.plotly_chart(
        fig_legalitas,
        use_container_width=True
    )

# SERTIFIKASI
with col2:

    st.subheader(
        "Sertifikasi Usaha"
    )

    fig_sertifikasi = px.bar(
        sertifikasi_df,
        x="Jumlah",
        y="Kategori",
        orientation="h",
        text="Jumlah"
    )

    fig_sertifikasi.update_traces(
        textposition="outside"
    )

    fig_sertifikasi.update_layout(
        yaxis_title="",
        xaxis_title="Jumlah UMKM",
        height=450
    )

    st.plotly_chart(
        fig_sertifikasi,
        use_container_width=True
    )

# =====================================
# FAKTOR PENTING PENGEMBANGAN UMKM
# =====================================
st.markdown("---")

st.markdown(
    """
    <div style="
        background-color:#E5E5E5;
        padding:10px;
        border:1px solid #CFCFCF;
        text-align:center;
        font-size:28px;
        font-weight:bold;
        border-radius:6px;
    ">
        FAKTOR PENTING PENGEMBANGAN UMKM
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# LOAD FEATURE IMPORTANCE
# =====================================
importance_df = pd.read_excel(
    "feature_importance.xlsx"
)

# pastikan numerik
importance_df["Important Score"] = pd.to_numeric(
    importance_df["Important Score"],
    errors="coerce"
)

importance_df = importance_df.dropna()

# =====================================
# INSIGHT TOP 3
# =====================================
top3 = (
    importance_df
    .sort_values(
        "Important Score",
        ascending=False
    )
    .head(3)["Feature"]
    .tolist()
)

st.info(
    f"""
    Berdasarkan hasil analisis feature importance,
    faktor yang paling berpengaruh terhadap
    pengembangan kelas UMKM adalah:

    **1. {top3[0]}**  
    **2. {top3[1]}**  
    **3. {top3[2]}**
    """
)

# =====================================
# PLOT
# =====================================
importance_plot = (
    importance_df
    .sort_values(
        "Important Score",
        ascending=True
    )
)

fig_importance = px.bar(
    importance_plot,
    x="Important Score",
    y="Feature",
    orientation="h",
    text="Important Score",
    title="Ranking Faktor Penting Pengembangan UMKM"
)

fig_importance.update_traces(
    textposition="outside"
)

fig_importance.update_layout(
    height=650,
    xaxis_title="Important Score",
    yaxis_title=""
)

st.plotly_chart(
    fig_importance,
    use_container_width=True
)
    
# =====================================
# DATAFRAME
# =====================================
with st.expander(
    "📄 Lihat Data UMKM"
):

    st.dataframe(
        filtered_df[
            [
                "Nama Usaha",
                "Nama Pemilik Usaha",
                "Jenis Kelamin",
                "Sektor Usaha",
                "Produk Jasa",
                "Provinsi",
                "Kota",
                "Waktu Profiling"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
