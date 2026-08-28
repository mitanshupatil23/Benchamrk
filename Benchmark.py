import streamlit as st
import pandas as pd
import requests
import time

from io import StringIO
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="BMW | MINI Benchmark Dashboard",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONFIGURATION
# ============================================================

DATA_URL = (
    "https://raw.githubusercontent.com/"
    "mitanshupatil23/Benchamrk/"
    "main/benchmark_data.csv"
)

# Refresh dashboard every 10 seconds
AUTO_REFRESH_SECONDS = 10


# ============================================================
# PREMIUM BMW / MINI CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
    ======================================================== */

    .stApp {

        background:
            radial-gradient(
                circle at 85% 10%,
                rgba(55, 55, 55, 0.25),
                transparent 30%
            ),
            radial-gradient(
                circle at 10% 90%,
                rgba(40, 40, 40, 0.20),
                transparent 35%
            ),
            #080808;

        color: #f4f4f4;

        font-family:
            "Arial",
            "Helvetica Neue",
            sans-serif;
    }


    /* ========================================================
       MAIN CONTENT
    ======================================================== */

    .block-container {

        padding-top: 2.5rem;
        padding-bottom: 1rem;

        max-width: 1500px;
    }


    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #0b0b0b 0%,
                #101010 55%,
                #080808 100%
            );

        border-right: 1px solid #252525;
    }


    section[data-testid="stSidebar"] > div {

        padding-top: 2rem;
    }


    .sidebar-brand {

        font-size: 10px;

        letter-spacing: 4px;

        text-transform: uppercase;

        color: #777777;

        margin-bottom: 5px;
    }


    .sidebar-title {

        font-size: 26px;

        font-weight: 700;

        letter-spacing: -0.8px;

        color: #ffffff;

        margin-bottom: 25px;
    }


    .sidebar-divider {

        height: 1px;

        background: #252525;

        margin: 22px 0;
    }


    .sidebar-info {

        font-size: 10px;

        letter-spacing: 1.5px;

        color: #626262;

        line-height: 2;
    }


    .sidebar-info span {

        color: #bcbcbc;
    }


    /* ========================================================
       HEADER
    ======================================================== */

    .top-label {

        font-size: 10px;

        letter-spacing: 4px;

        text-transform: uppercase;

        color: #777777;

        margin-bottom: 10px;
    }


    .main-title {

        font-size: clamp(36px, 5vw, 60px);

        font-weight: 700;

        letter-spacing: -3px;

        line-height: 0.95;

        color: #ffffff;

        margin-bottom: 15px;
    }


    .main-title .muted {

        color: #858585;

        font-weight: 300;
    }


    .subtitle {

        font-size: 13px;

        color: #777777;

        letter-spacing: 0.3px;

        max-width: 900px;

        line-height: 1.8;

        margin-bottom: 25px;
    }


    /* ========================================================
       BRAND BADGES
    ======================================================== */

    .brand-container {

        display: flex;

        gap: 10px;

        margin-bottom: 30px;
    }


    .brand-badge {

        padding: 9px 17px;

        background: #111111;

        border: 1px solid #303030;

        color: #d9d9d9;

        font-size: 10px;

        font-weight: 600;

        letter-spacing: 3px;

    }


    .brand-badge.bmw {

        border-left: 3px solid #eeeeee;
    }


    .brand-badge.mini {

        border-left: 3px solid #777777;
    }


    /* ========================================================
       LIVE STATUS
    ======================================================== */

    .status-card {

        display: flex;

        justify-content: space-between;

        align-items: center;

        background:
            linear-gradient(
                90deg,
                #111111,
                #0c0c0c
            );

        border: 1px solid #272727;

        padding: 13px 17px;

        margin-bottom: 28px;
    }


    .status-left {

        display: flex;

        align-items: center;

        font-size: 10px;

        letter-spacing: 2px;

        color: #a7a7a7;

        text-transform: uppercase;
    }


    .live-dot {

        width: 8px;

        height: 8px;

        background: #cfcfcf;

        border-radius: 50%;

        margin-right: 9px;

        box-shadow:
            0 0 0 4px rgba(200, 200, 200, 0.05),
            0 0 10px rgba(220, 220, 220, 0.20);
    }


    .status-right {

        font-size: 10px;

        color: #696969;

        letter-spacing: 1px;
    }


    /* ========================================================
       SECTION HEADERS
    ======================================================== */

    .section-number {

        font-size: 9px;

        color: #5e5e5e;

        letter-spacing: 3px;

        margin-bottom: 5px;
    }


    .section-title {

        font-size: 23px;

        font-weight: 600;

        color: #ffffff;

        letter-spacing: -0.5px;

        margin-bottom: 5px;
    }


    .section-description {

        font-size: 11px;

        color: #696969;

        margin-bottom: 20px;
    }


    /* ========================================================
       KPI CARDS
    ======================================================== */

    .kpi-card {

        background:
            linear-gradient(
                145deg,
                #151515,
                #0c0c0c
            );

        border: 1px solid #282828;

        padding: 21px;

        min-height: 120px;

        position: relative;

        overflow: hidden;

        transition: 0.2s ease;
    }


    .kpi-card:hover {

        border-color: #4a4a4a;

        transform: translateY(-2px);
    }


    .kpi-card::before {

        content: "";

        position: absolute;

        top: 0;

        left: 0;

        width: 100%;

        height: 2px;

        background: #dddddd;
    }


    .kpi-label {

        font-size: 9px;

        letter-spacing: 2px;

        text-transform: uppercase;

        color: #6c6c6c;

        margin-bottom: 12px;
    }


    .kpi-value {

        font-size: 30px;

        font-weight: 600;

        color: #ffffff;

        letter-spacing: -1px;
    }


    .kpi-sub {

        font-size: 10px;

        color: #626262;

        margin-top: 7px;
    }


    /* ========================================================
       TABLE
    ======================================================== */

    div[data-testid="stDataFrame"] {

        border: 1px solid #292929;

        border-radius: 0px;
    }


    /* ========================================================
       BUTTON
    ======================================================== */

    .stButton > button {

        width: 100%;

        border-radius: 0px;

        border: 1px solid #383838;

        background: #151515;

        color: #eeeeee;

        font-size: 10px;

        letter-spacing: 1.5px;

        text-transform: uppercase;

        padding: 10px 14px;

        transition: 0.2s ease;
    }


    .stButton > button:hover {

        border-color: #777777;

        background: #202020;

        color: #ffffff;
    }


    /* ========================================================
       SELECTBOX
    ======================================================== */

    div[data-baseweb="select"] > div {

        background-color: #151515 !important;

        border-color: #353535 !important;

        border-radius: 0px !important;

        color: #ffffff !important;
    }


    /* ========================================================
       FOOTER
    ======================================================== */

    .footer {

        border-top: 1px solid #252525;

        margin-top: 55px;

        padding-top: 20px;

        padding-bottom: 25px;

        display: flex;

        justify-content: space-between;

        color: #555555;

        font-size: 9px;

        letter-spacing: 1.5px;

        text-transform: uppercase;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING FUNCTION
# ============================================================

def load_data():

    try:

        # ----------------------------------------------------
        # CACHE BUSTER
        # ----------------------------------------------------

        cache_buster = int(time.time())

        fresh_url = (
            f"{DATA_URL}?t={cache_buster}"
        )


        # ----------------------------------------------------
        # REQUEST LATEST CSV
        # ----------------------------------------------------

        response = requests.get(
            fresh_url,
            timeout=15,
            headers={
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
        )


        response.raise_for_status()


        # ----------------------------------------------------
        # READ CSV
        # ----------------------------------------------------

        df = pd.read_csv(
            StringIO(response.text)
        )


        # ----------------------------------------------------
        # REMOVE COMPLETELY EMPTY ROWS
        # ----------------------------------------------------

        df = df.dropna(
            axis=0,
            how="all"
        )


        # ----------------------------------------------------
        # CLEAN COLUMN NAMES
        # ----------------------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )


        # ----------------------------------------------------
        # REMOVE UNNAMED COLUMNS
        # ----------------------------------------------------

        df = df.loc[
            :,
            ~df.columns.str.startswith(
                "Unnamed"
            )
        ]


        # ----------------------------------------------------
        # REMOVE DUPLICATE COLUMNS
        # ----------------------------------------------------

        df = df.loc[
            :,
            ~df.columns.duplicated()
        ]


        # ----------------------------------------------------
        # RESET INDEX
        # ----------------------------------------------------

        df = df.reset_index(
            drop=True
        )


        return df, response.headers


    except Exception as e:

        return (
            pd.DataFrame(),
            str(e)
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            BMW GROUP
        </div>

        <div class="sidebar-title">
            Benchmark
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="sidebar-brand">
            DATA FILTER
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LOAD DATA
# ============================================================

df, response_info = load_data()


# ============================================================
# DATA ERROR HANDLING
# ============================================================

if df.empty:

    st.error(
        "Unable to load the latest benchmark data."
    )

    st.caption(
        f"Connection details: {response_info}"
    )

    st.stop()


# ============================================================
# FIND BUSINESS AREA COLUMN
# ============================================================

business_area_column = None


for column in df.columns:

    if (
        str(column)
        .strip()
        .lower()
        == "business area"
    ):

        business_area_column = column

        break


# ============================================================
# BUSINESS AREA FILTER
# ============================================================

with st.sidebar:

    if business_area_column is not None:

        business_areas = (
            df[business_area_column]
            .dropna()
            .astype(str)
            .str.strip()
        )


        business_areas = sorted(
            business_areas[
                business_areas != ""
            ]
            .unique()
            .tolist()
        )


        selected_business_area = st.selectbox(
            "Business Area",
            ["All"] + business_areas
        )


    else:

        selected_business_area = "All"

        st.warning(
            "Business Area column not found."
        )


    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # MANUAL REFRESH
    # ========================================================

    if st.button(
        "↻  Refresh Data"
    ):

        st.rerun()


    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SIDEBAR DATA INFORMATION
    # ========================================================

    st.markdown(
        f"""
 <div class="sidebar-info">

    DATA SOURCE<br>
    <span>GitHub / benchmark_data.csv</span>

    <br><br>

    REFRESH RATE<br>
    <span>{AUTO_REFRESH_SECONDS} seconds</span>

    <br><br>

    TOTAL RECORDS<br>
    <span>{len(df):,}</span>

    <br><br>

    TOTAL COLUMNS<br>
    <span>{len(df.columns):,}</span>

 </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# APPLY BUSINESS AREA FILTER
# ============================================================

filtered_df = df.copy()


if (
    business_area_column is not None
    and selected_business_area != "All"
):

    filtered_df = filtered_df[
        filtered_df[
            business_area_column
        ]
        .astype(str)
        .str.strip()
        == selected_business_area
    ]


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
 <div class="top-label">
    BMW GROUP / MIS & BUSINESS INTELLIGENCE
 </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
 <div class="main-title">

 BMW <span class="muted">&</span> MINI

 <span class="muted">
    Benchmark
 </span>

</div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
 <div class="subtitle">

    A centralized benchmarking view of business performance,
    designed for clean comparison, operational visibility,
    and management decision-making.

 </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BRAND BADGES
# ============================================================

st.markdown(
    """
 <div class="brand-container">

 <div class="brand-badge bmw">
    BMW
 </div>

 <div class="brand-badge mini">
    MINI
 </div>

 </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LIVE STATUS
# ============================================================

data_fetch_time = datetime.now().strftime(
    "%d %b %Y  |  %H:%M:%S"
)


st.markdown(
    f"""
 <div class="status-card">

 <div class="status-left">

 <div class="live-dot"></div>

    LIVE DATA

 </div>

 <div class="status-right">

 Last data fetch:
 {data_fetch_time}

 &nbsp;&nbsp;|&nbsp;&nbsp;

 Auto refresh:
 {AUTO_REFRESH_SECONDS}s

 </div>

</div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SECTION 01
# ============================================================

st.markdown(
    """
 <div class="section-number">
    01 / PERFORMANCE OVERVIEW
 </div>

 <div class="section-title">
    Benchmark Snapshot
 </div>

 <div class="section-description">
    Current view based on the selected Business Area.
 </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

row_count = len(filtered_df)

column_count = len(filtered_df.columns)


if business_area_column is not None:

    business_area_count = (
        filtered_df[
            business_area_column
        ]
        .nunique()
    )

else:

    business_area_count = 0


numeric_columns = (
    filtered_df
    .select_dtypes(
        include="number"
    )
    .columns
)


numeric_count = len(
    numeric_columns
)


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.markdown(
        f"""
 <div class="kpi-card">

 <div class="kpi-label">
    Records
 </div>

 <div class="kpi-value">
    {row_count:,}
 </div>

 <div class="kpi-sub">
    Current filtered records
 </div>

</div>
        """,
        unsafe_allow_html=True
    )


with k2:

    st.markdown(
        f"""
 <div class="kpi-card">

 <div class="kpi-label">
    Business Areas
 </div>

 <div class="kpi-value">
    {business_area_count:,}
 </div>

 <div class="kpi-sub">
    Active categories
 </div>

 </div>
        """,
        unsafe_allow_html=True
    )


with k3:

    st.markdown(
        f"""
 <div class="kpi-card">

 <div class="kpi-label">
    Data Fields
 </div>

 <div class="kpi-value">
    {column_count:,}
 </div>

 <div class="kpi-sub">
    Available columns
 </div>

 </div>
        """,
        unsafe_allow_html=True
    )


with k4:

    st.markdown(
        f"""
 <div class="kpi-card">

 <div class="kpi-label">
    Numeric KPIs
 </div>

 <div class="kpi-value">
    {numeric_count:,}
 </div>

 <div class="kpi-sub">
    Analytical fields
 </div>

 </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# ============================================================
# SECTION 02 — TABLE
# ============================================================

st.markdown(
    """
 <div class="section-number">
    02 / BENCHMARK DATA
 </div>

 <div class="section-title">
    Business Performance
 </div>

 <div class="section-description">
    Detailed benchmark data from the Dash dataset.
 </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# REMOVE FIRST TWO COLUMNS
# ============================================================

if len(filtered_df.columns) > 2:

    display_df = filtered_df.iloc[
        :,
        2:
    ].copy()

else:

    display_df = filtered_df.copy()


# ============================================================
# REMOVE COMPLETELY EMPTY COLUMNS
# ============================================================

display_df = display_df.dropna(
    axis=1,
    how="all"
)


# ============================================================
# REMOVE COMPLETELY EMPTY ROWS
# ============================================================

display_df = display_df.dropna(
    axis=0,
    how="all"
)


# ============================================================
# CLEAN DISPLAY DATA
# ============================================================

display_df = display_df.fillna("")


display_df = display_df.reset_index(
    drop=True
)


# ============================================================
# DISPLAY TABLE
# ============================================================

st.dataframe(
    display_df,

    use_container_width=True,

    hide_index=True,

    height=560
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
 <div class="footer">

 <div>
    BMW GROUP · BENCHMARKING
 </div>

 <div>
    MIS / BUSINESS INTELLIGENCE
 </div>

 </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# AUTO REFRESH — EVERY 10 SECONDS
# ============================================================

st.markdown(
    f"""
    <script>

        setTimeout(
            function() {{

                window.location.reload();

            }},

            {AUTO_REFRESH_SECONDS * 1000}

        );

    </script>
    """,
    unsafe_allow_html=True
)