import streamlit as st
import pandas as pd
from datetime import datetime
import time


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

AUTO_REFRESH_SECONDS = 300


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
                rgba(40, 40, 40, 0.35),
                transparent 30%
            ),
            radial-gradient(
                circle at 10% 90%,
                rgba(30, 30, 30, 0.25),
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

        border-right: 1px solid #242424;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    .sidebar-brand {

        font-size: 11px;
        letter-spacing: 4px;
        text-transform: uppercase;

        color: #8f8f8f;

        margin-bottom: 5px;
    }

    .sidebar-title {

        font-size: 25px;
        font-weight: 700;

        letter-spacing: -0.5px;

        color: #ffffff;

        margin-bottom: 25px;
    }

    .sidebar-divider {

        height: 1px;
        background: #2a2a2a;

        margin: 20px 0;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .top-label {

        font-size: 11px;

        letter-spacing: 4px;

        text-transform: uppercase;

        color: #858585;

        margin-bottom: 8px;
    }


    .main-title {

        font-size: clamp(32px, 5vw, 58px);

        font-weight: 700;

        letter-spacing: -2.5px;

        line-height: 1;

        color: #ffffff;

        margin-bottom: 12px;
    }


    .main-title span {

        color: #8f8f8f;
        font-weight: 300;
    }


    .subtitle {

        font-size: 14px;

        color: #858585;

        letter-spacing: 0.5px;

        max-width: 850px;

        line-height: 1.7;

        margin-bottom: 30px;
    }


    /* ========================================================
       BRAND BADGES
       ======================================================== */

    .brand-container {

        display: flex;

        gap: 10px;

        margin-bottom: 28px;
    }


    .brand-badge {

        border: 1px solid #333333;

        background: #111111;

        padding: 8px 16px;

        font-size: 11px;

        letter-spacing: 3px;

        font-weight: 600;

        color: #d7d7d7;

    }


    .brand-badge.bmw {

        border-left: 3px solid #ffffff;

    }


    .brand-badge.mini {

        border-left: 3px solid #777777;

    }


    /* ========================================================
       KPI CARDS
       ======================================================== */

    .kpi-card {

        background:
            linear-gradient(
                145deg,
                #151515,
                #0d0d0d
            );

        border: 1px solid #292929;

        padding: 22px;

        min-height: 125px;

        position: relative;

        overflow: hidden;

        transition: all 0.2s ease;
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

        background: #eeeeee;

    }


    .kpi-label {

        font-size: 10px;

        letter-spacing: 2px;

        text-transform: uppercase;

        color: #777777;

        margin-bottom: 13px;

    }


    .kpi-value {

        font-size: 31px;

        font-weight: 600;

        color: #ffffff;

        letter-spacing: -1px;

    }


    .kpi-sub {

        font-size: 11px;

        color: #777777;

        margin-top: 7px;

    }


    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    .section-number {

        font-size: 10px;

        color: #666666;

        letter-spacing: 3px;

        margin-bottom: 5px;

    }


    .section-title {

        font-size: 23px;

        font-weight: 600;

        color: #ffffff;

        margin-bottom: 5px;

    }


    .section-description {

        font-size: 12px;

        color: #707070;

        margin-bottom: 20px;

    }


    /* ========================================================
       DATA STATUS
       ======================================================== */

    .status-card {

        display: flex;

        justify-content: space-between;

        align-items: center;

        background: #101010;

        border: 1px solid #262626;

        padding: 12px 16px;

        margin-bottom: 20px;

    }


    .status-left {

        font-size: 11px;

        color: #888888;

        letter-spacing: 1px;

    }


    .status-right {

        font-size: 11px;

        color: #cfcfcf;

    }


    .status-dot {

        display: inline-block;

        width: 7px;

        height: 7px;

        border-radius: 50%;

        background: #bdbdbd;

        margin-right: 7px;

    }


    /* ========================================================
       TABLE
       ======================================================== */

    div[data-testid="stDataFrame"] {

        border: 1px solid #292929;

    }


    /* ========================================================
       STREAMLIT BUTTONS
       ======================================================== */

    .stButton > button {

        width: 100%;

        border-radius: 0px;

        border: 1px solid #383838;

        background: #151515;

        color: #eeeeee;

        font-size: 11px;

        letter-spacing: 1.5px;

        text-transform: uppercase;

        padding: 10px 14px;

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

        color: white !important;

    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {

        border-top: 1px solid #252525;

        margin-top: 60px;

        padding-top: 20px;

        padding-bottom: 30px;

        display: flex;

        justify-content: space-between;

        color: #5f5f5f;

        font-size: 10px;

        letter-spacing: 1.5px;

        text-transform: uppercase;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADER
# ============================================================

@st.cache_data(ttl=AUTO_REFRESH_SECONDS)
def load_data():

    try:

        df = pd.read_csv(DATA_URL)

        # ----------------------------------------------------
        # Remove completely empty rows
        # ----------------------------------------------------

        df = df.dropna(how="all")

        # ----------------------------------------------------
        # Remove rows where every value is blank
        # ----------------------------------------------------

        df = df[
            ~df.apply(
                lambda row:
                row.astype(str)
                .str.strip()
                .replace("nan", "")
                .eq("")
                .all(),
                axis=1
            )
        ]

        # ----------------------------------------------------
        # Clean column names
        # ----------------------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # ----------------------------------------------------
        # Remove Excel-generated Unnamed columns
        # ----------------------------------------------------

        df = df.loc[
            :,
            ~df.columns.str.startswith("Unnamed")
        ]

        # ----------------------------------------------------
        # Remove duplicate columns
        # ----------------------------------------------------

        df = df.loc[
            :,
            ~df.columns.duplicated()
        ]

        # ----------------------------------------------------
        # Reset index
        # ----------------------------------------------------

        df = df.reset_index(drop=True)

        return df

    except Exception as e:

        st.error(
            f"Unable to load dashboard data: {e}"
        )

        return pd.DataFrame()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">BMW GROUP</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-title">Benchmark</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-brand">DATA FILTER</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    df = load_data()

    business_area_column = None

    for col in df.columns:

        if str(col).strip().lower() == "business area":

            business_area_column = col

            break


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
            ].unique()
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


    # --------------------------------------------------------
    # Refresh button
    # --------------------------------------------------------

    if st.button(
        "↻  Refresh Data",
        use_container_width=True
    ):

        st.cache_data.clear()

        st.rerun()


    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Data information
    # --------------------------------------------------------

    if not df.empty:

        st.markdown(
            f"""
            <div style="
                font-size:10px;
                letter-spacing:1.5px;
                color:#666;
                line-height:2;
            ">

            ROWS<br>
            <span style="color:#aaa;">
            {len(df):,}
            </span>

            <br><br>

            COLUMNS<br>
            <span style="color:#aaa;">
            {len(df.columns):,}
            </span>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="top-label">BMW GROUP / MIS & BUSINESS INTELLIGENCE</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-title">
        BMW <span>&</span> MINI
        <span>Benchmark</span>
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
# ERROR HANDLING
# ============================================================

if df.empty:

    st.error(
        "No data could be loaded from the GitHub CSV."
    )

    st.info(
        "Please check that benchmark_data.csv exists "
        "in the Benchamrk repository."
    )

    st.stop()


# ============================================================
# APPLY BUSINESS AREA FILTER
# ============================================================

filtered_df = df.copy()


if (
    business_area_column is not None
    and selected_business_area != "All"
):

    filtered_df = filtered_df[
        filtered_df[business_area_column]
        .astype(str)
        .str.strip()
        == selected_business_area
    ]


# ============================================================
# KPI SECTION
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

business_area_count = 0

if business_area_column is not None:

    business_area_count = (
        filtered_df[business_area_column]
        .nunique()
    )


numeric_columns = (
    filtered_df
    .select_dtypes(include="number")
    .columns
)

numeric_count = len(numeric_columns)


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
                Filtered records
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


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# DATA STATUS
# ============================================================

current_time = datetime.now().strftime(
    "%d %b %Y  |  %H:%M"
)

st.markdown(
    f"""
    <div class="status-card">

        <div class="status-left">
            <span class="status-dot"></span>
            LIVE DATA CONNECTION
        </div>

        <div class="status-right">
            Last dashboard refresh:
            {current_time}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA TABLE
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

    display_df = filtered_df.iloc[:, 2:].copy()

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
# REMOVE COMPLETELY EMPTY ROWS AGAIN
# ============================================================

display_df = display_df.dropna(
    axis=0,
    how="all"
)


# ============================================================
# REPLACE NaN FOR DISPLAY
# ============================================================

display_df = display_df.fillna("")


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
# AUTO REFRESH
# ============================================================

st.markdown(
    f"""
    <script>
        setTimeout(function() {{
            window.location.reload();
        }}, {AUTO_REFRESH_SECONDS * 1000});
    </script>
    """,
    unsafe_allow_html=True
)
