import streamlit as st
import pandas as pd
import os
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="BMW & MINI | Benchmark Dashboard",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# EXCEL CONFIGURATION
# ============================================================

EXCEL_FILE = r"https://infinitycr1.sharepoint.com/sites/MIS-InfinityCars/Benchmarking KPI Master.xlsx"

SHEET_NAME = "Dash"


# ============================================================
# BRAND LOGOS
# ============================================================

BMW_LOGO = (
    "https://commons.wikimedia.org/wiki/"
    "Special:Redirect/file/BMW_logo_(gray).svg"
)

MINI_LOGO = (
    "https://commons.wikimedia.org/wiki/"
    "Special:Redirect/file/Mini-logo.svg"
)


# ============================================================
# PREMIUM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f5f6f8;
    }

    .main {
        padding-top: 0rem;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e3e6eb;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.4rem 1.25rem;
    }


    /* ========================================================
       BRAND AREA
       ======================================================== */

    .brand-container {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 5px 0 8px 0;
    }

    .sidebar-title {
        font-size: 17px;
        font-weight: 700;
        color: #17233c;
        letter-spacing: -0.3px;
        margin-top: 12px;
    }

    .sidebar-subtitle {
        font-size: 10px;
        font-weight: 600;
        color: #667085;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 5px;
    }


    /* ========================================================
       SIDEBAR DIVIDER
       ======================================================== */

    .sidebar-line {
        height: 1px;
        background: #e4e7eb;
        margin: 23px 0;
    }


    /* ========================================================
       FILTER LABEL
       ======================================================== */

    .filter-label {
        font-size: 10px;
        font-weight: 700;
        color: #667085;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 10px;
    }


    /* ========================================================
       DATA STATUS
       ======================================================== */

    .status-box {
        background: #f8fafc;
        border: 1px solid #e5e9ef;
        border-radius: 10px;
        padding: 14px;
        margin-top: 8px;
    }

    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #35b86b;
        margin-right: 8px;
    }

    .status-text {
        color: #17233c;
        font-size: 12px;
        font-weight: 600;
    }

    .status-subtext {
        color: #7b8493;
        font-size: 10px;
        margin-top: 5px;
        padding-left: 16px;
    }


    /* ========================================================
       SIDEBAR FOOTER
       ======================================================== */

    .sidebar-footer {
        margin-top: 35px;
        padding: 15px;
        background: #f7f8fa;
        border: 1px solid #e8eaee;
        border-radius: 10px;
        color: #667085;
        font-size: 10px;
        line-height: 1.6;
    }


    /* ========================================================
       MAIN HEADER
       ======================================================== */

    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 28px;
    }

    .header-left {
        border-left: 4px solid #1c69d4;
        padding-left: 17px;
    }

    .page-title {
        font-size: 31px;
        line-height: 1.15;
        font-weight: 700;
        color: #17233c;
        letter-spacing: -1px;
        margin: 0;
    }

    .page-subtitle {
        color: #737d8e;
        font-size: 13px;
        margin-top: 7px;
    }


    /* ========================================================
       REFRESH CARD
       ======================================================== */

    .refresh-card {
        background: #ffffff;
        border: 1px solid #e4e7ec;
        border-radius: 11px;
        padding: 13px 17px;
        min-width: 210px;
        box-shadow: 0 4px 18px rgba(20, 30, 50, 0.04);
    }

    .refresh-label {
        font-size: 9px;
        text-transform: uppercase;
        color: #7c8491;
        letter-spacing: 1px;
        font-weight: 700;
    }

    .refresh-value {
        color: #17233c;
        font-size: 12px;
        font-weight: 600;
        margin-top: 5px;
    }


    /* ========================================================
       KPI CARDS
       ======================================================== */

    .kpi-card {
        background: #ffffff;
        border: 1px solid #e4e7ec;
        border-radius: 12px;
        min-height: 122px;
        padding: 21px;
        box-shadow: 0 4px 18px rgba(20, 30, 50, 0.045);
        transition: all 0.2s ease;
    }

    .kpi-card:hover {
        box-shadow: 0 8px 25px rgba(20, 30, 50, 0.08);
        transform: translateY(-1px);
    }

    .kpi-icon {
        width: 37px;
        height: 37px;
        border-radius: 50%;
        background: #edf4ff;
        color: #1769d8;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        margin-bottom: 13px;
    }

    .kpi-label {
        font-size: 9px;
        color: #687386;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }

    .kpi-value {
        font-size: 25px;
        color: #17233c;
        font-weight: 700;
        margin-top: 4px;
    }


    /* ========================================================
       SECTION
       ======================================================== */

    .section-card {
        background: #ffffff;
        border: 1px solid #e4e7ec;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 18px rgba(20, 30, 50, 0.04);
    }

    .section-title {
        color: #17233c;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.1px;
    }

    .section-description {
        color: #7b8493;
        font-size: 11px;
        margin-top: 4px;
    }


    /* ========================================================
       DATA TABLE
       ======================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 9px;
        overflow: hidden;
        border: 1px solid #e2e6eb;
    }


    /* ========================================================
       BUTTON
       ======================================================== */

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #17233c;
        background: #17233c;
        color: white;
        font-weight: 600;
        font-size: 12px;
        min-height: 42px;
    }

    .stButton > button:hover {
        background: #243554;
        border-color: #243554;
        color: white;
    }


    /* ========================================================
       SELECT BOX
       ======================================================== */

    div[data-baseweb="select"] > div {
        border-radius: 8px;
        border-color: #dfe4eb;
        background: #ffffff;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 9px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .luxury-footer {
        border-top: 1px solid #e1e5ea;
        margin-top: 35px;
        padding-top: 20px;
        text-align: center;
        color: #7a8391;
        font-size: 11px;
    }

    .footer-brand {
        color: #17233c;
        font-weight: 600;
        font-size: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD EXCEL DATA
# ============================================================

@st.cache_data(ttl=300)
def load_data():

    df = pd.read_excel(
        EXCEL_FILE,
        sheet_name=SHEET_NAME,
        engine="openpyxl"
    )

    # --------------------------------------------------------
    # REMOVE COMPLETELY EMPTY ROWS
    # --------------------------------------------------------

    df = df.dropna(how="all")

    # --------------------------------------------------------
    # REMOVE ROWS CONTAINING ONLY BLANK VALUES
    # --------------------------------------------------------

    df = df[
        ~df.apply(
            lambda row:
            row.astype(str).str.strip().eq("").all(),
            axis=1
        )
    ]

    # --------------------------------------------------------
    # CLEAN COLUMN NAMES
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # RESET INDEX
    # --------------------------------------------------------

    df = df.reset_index(drop=True)

    return df


# ============================================================
# CHECK EXCEL FILE
# ============================================================

if not os.path.exists(EXCEL_FILE):

    st.error("Excel file not found.")

    st.code(EXCEL_FILE)

    st.info(
        "Please update the EXCEL_FILE variable "
        "with the correct Excel path."
    )

    st.stop()


# ============================================================
# READ DATA
# ============================================================

try:

    df = load_data()

except Exception as e:

    st.error("Unable to read the Excel file.")

    st.exception(e)

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BMW + MINI LOGOS
    # --------------------------------------------------------

    logo_col1, logo_col2 = st.columns([1, 1.35])

    with logo_col1:

        st.image(
            BMW_LOGO,
            width=58
        )

    with logo_col2:

        st.image(
            MINI_LOGO,
            width=82
        )


    # --------------------------------------------------------
    # SIDEBAR TITLE
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-title">BMW & MINI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Benchmark Dashboard'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sidebar-line"></div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    st.markdown(
        '<div class="filter-label">Filters</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # BUSINESS AREA FILTER
    # --------------------------------------------------------

    if "Business Area" in df.columns:

        business_areas = (
            df["Business Area"]
            .dropna()
            .astype(str)
            .str.strip()
        )

        business_areas = sorted(
            business_areas[
                business_areas != ""
            ].unique()
        )

        selected_business_area = st.multiselect(
            "Business Area",
            options=business_areas,
            default=business_areas
        )

    else:

        st.error(
            "'Business Area' column was not found."
        )

        selected_business_area = []


    # --------------------------------------------------------
    # RESET FILTER
    # --------------------------------------------------------

    if st.button(
        "↻  Reset Filters",
        use_container_width=True
    ):

        st.rerun()


    st.markdown(
        '<div class="sidebar-line"></div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # DATA STATUS
    # --------------------------------------------------------

    st.markdown(
        '<div class="filter-label">Data Status</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
 <div class="status-box">

 <div>
 <span class="status-dot"></span>
 <span class="status-text">
    Connected
 </span>
 </div>

 <div class="status-subtext">
    Dash sheet
 </div>

</div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # LAST REFRESH
    # --------------------------------------------------------

    st.markdown(
        '<div class="filter-label" '
        'style="margin-top:22px;">'
        'Last Refresh'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            color:#17233c;
            font-size:12px;
            font-weight:600;
            margin-top:8px;
        ">
            ◷ &nbsp;
            {datetime.now().strftime("%d %b %Y %H:%M:%S")}
        </div>

        <div style="
            color:#7a8391;
            font-size:10px;
            margin-top:5px;
        ">
            Auto refresh every 5 min
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # SIDEBAR FOOTER
    # --------------------------------------------------------

    st.markdown(
        """
 <div class="sidebar-footer">

 <strong>◆</strong>
    &nbsp; Driving Performance.<br>

 <span style="padding-left:20px;">
    Delivering Excellence.
 </span>

 </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# APPLY BUSINESS AREA FILTER
# ============================================================

filtered_df = df.copy()


if "Business Area" in filtered_df.columns:

    if selected_business_area:

        filtered_df = filtered_df[
            filtered_df["Business Area"]
            .astype(str)
            .str.strip()
            .isin(selected_business_area)
        ]

    else:

        filtered_df = filtered_df.iloc[0:0]


# ============================================================
# RESET FILTERED DATAFRAME INDEX
# ============================================================

filtered_df = filtered_df.reset_index(drop=True)


# ============================================================
# REMOVE FIRST TWO COLUMNS FROM DISPLAY
# ============================================================

if len(filtered_df.columns) > 2:

    display_df = filtered_df.iloc[:, 2:].copy()

else:

    display_df = pd.DataFrame()


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
 <div class="page-header">

 <div class="header-left">

 <div class="page-title">
    BMW & MINI Benchmark Dashboard
 </div>

 <div class="page-subtitle">
    Real-time insights. Smarter performance.
 </div>

 </div>

 <div class="refresh-card">

 <div class="refresh-label">
    Last Refresh
 </div>

 <div class="refresh-value">
    ◷ &nbsp;
    """
    + datetime.now().strftime("%d %b %Y %H:%M:%S")
    + """
 </div>

 </div>

 </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONNECTION STATUS
# ============================================================

st.success(
    f"Connected • Excel / {SHEET_NAME} sheet"
)


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.markdown(
        f"""
 <div class="kpi-card">

 <div class="kpi-icon">
    ▱
 </div>

 <div class="kpi-label">
    Total Records
 </div>

 <div class="kpi-value">
    {len(filtered_df):,}
 </div>

</div>
        """,
        unsafe_allow_html=True
    )


with k2:

    st.markdown(
        f"""
 <div class="kpi-card">

 <div class="kpi-icon">
    ▦
 </div>

 <div class="kpi-label">
    Display Columns
 </div>

 <div class="kpi-value">
    {len(display_df.columns):,}
 </div>

</div>
        """,
        unsafe_allow_html=True
    )


with k3:

    st.markdown(
        f"""
 <div class="kpi-card">

 <div class="kpi-icon">
    ◫
 </div>

 <div class="kpi-label">
    Business Areas
 </div>

 <div class="kpi-value">
    {len(selected_business_area):,}
 </div>

 </div>
        """,
        unsafe_allow_html=True
    )


with k4:

    st.markdown(
        f"""
 <div class="kpi-card">

 <div class="kpi-icon">
    ◷
 </div>

 <div class="kpi-label">
    Records Displayed
 </div>

 <div class="kpi-value">
    {len(display_df):,}
 </div>

</div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TABLE SECTION
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

st.markdown(
    """
 <div class="section-card">

 <div class="section-title">
    ▦ &nbsp; DASH SHEET DATA
 </div>

 <div class="section-description">
    Benchmark data based on the selected Business Area
 </div>

</div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA TABLE
# ============================================================

if display_df.empty:

    st.warning(
        "No data available to display."
    )

else:

    st.dataframe(
        display_df,
        use_container_width=True,
        height=600,
        hide_index=True
    )


# ============================================================
# COLUMN INFORMATION
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

with st.expander("⌄   COLUMN INFORMATION"):

    column_info = pd.DataFrame(
        {
            "Column Name": display_df.columns,
            "Data Type": display_df.dtypes.astype(str).values,
            "Non-Empty Values": display_df.notna().sum().values
        }
    )

    st.dataframe(
        column_info,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# REFRESH
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

refresh_col1, refresh_col2 = st.columns([1, 5])


with refresh_col1:

    if st.button(
        "↻  Refresh Data",
        use_container_width=True
    ):

        st.cache_data.clear()

        st.rerun()


with refresh_col2:

    st.markdown(
        """
        <div style="
            padding-top:11px;
            color:#7a8391;
            font-size:11px;
        ">
            Data cache expires automatically every 5 minutes.
            Use Refresh Data to load the latest Excel changes immediately.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
 <div class="luxury-footer">

 <span class="footer-brand">
    BMW & MINI Benchmark Dashboard
 </span>

    &nbsp;&nbsp;•&nbsp;&nbsp;

    Driving Performance. Delivering Excellence.

 </div>
    """,
    unsafe_allow_html=True
)
