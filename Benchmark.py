import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import requests
import time
import re

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


AUTO_REFRESH_SECONDS = 10


# ============================================================
# COLUMN FORMATTING CONFIGURATION
# ============================================================

PERCENTAGE_COLUMNS = [
    "Achieved",
    "Projection",
    "Backlog %"
]


WHOLE_NUMBER_COLUMNS = [
    "Backlog Units",
    "Target need to achive",
    "Backlog Units ( Per day )",
    "Target need to achive ( per day )",
    "Daily total Target"
]


# ============================================================
# PREMIUM BMW / MINI DASHBOARD CSS
# ============================================================

st.markdown(
    """
    <style>


    /* ========================================================
       GLOBAL APPLICATION
    ======================================================== */

    .stApp {

        background:

            radial-gradient(
                circle at 90% 5%,
                rgba(28, 105, 212, 0.10),
                transparent 28%
            ),

            radial-gradient(
                circle at 5% 95%,
                rgba(150, 160, 175, 0.15),
                transparent 32%
            ),

            linear-gradient(
                135deg,
                #f7f8fa 0%,
                #eef1f4 50%,
                #fafbfc 100%
            );

        color: #17191c;

        font-family:
            "Helvetica Neue",
            Arial,
            sans-serif;
    }


    /* ========================================================
       MAIN CONTENT
    ======================================================== */

    .block-container {

        padding-top: 2.8rem;

        padding-bottom: 2rem;

        max-width: 1550px;
    }


    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {

        background:

            linear-gradient(
                180deg,
                #111720 0%,
                #19212b 55%,
                #0d1218 100%
            );

        border-right:
            1px solid rgba(255,255,255,0.08);

        box-shadow:
            10px 0px 40px rgba(0,0,0,0.15);
    }


    section[data-testid="stSidebar"] > div {

        padding-top: 2rem;
    }


    .sidebar-brand {

        font-size: 10px;

        letter-spacing: 4px;

        text-transform: uppercase;

        color: #8d98a5;

        margin-bottom: 7px;
    }


    .sidebar-title {

        font-size: 30px;

        font-weight: 600;

        letter-spacing: -1px;

        line-height: 1.05;

        color: #ffffff;

        margin-bottom: 25px;
    }


    .sidebar-divider {

        height: 1px;

        background:

            linear-gradient(
                90deg,
                transparent,
                rgba(255,255,255,0.18),
                transparent
            );

        margin: 24px 0;
    }


    .sidebar-info {

        font-size: 10px;

        letter-spacing: 1.5px;

        color: #7f8994;

        line-height: 2;
    }


    .sidebar-info span {

        color: #e5e9ed;

        font-size: 11px;
    }


    /* ========================================================
       HEADER
    ======================================================== */

    .top-label {

        display: inline-block;

        font-size: 10px;

        letter-spacing: 4px;

        text-transform: uppercase;

        color: #65717d;

        padding-bottom: 8px;

        border-bottom:
            2px solid #1c69d4;

        margin-bottom: 18px;
    }


    .main-title {

        font-size: clamp(40px, 5vw, 66px);

        font-weight: 650;

        letter-spacing: -3.5px;

        line-height: 0.95;

        color: #15181c;

        margin-bottom: 18px;
    }


    .main-title .muted {

        color: #7f8790;

        font-weight: 300;
    }


    .subtitle {

        font-size: 14px;

        color: #69727c;

        letter-spacing: 0.2px;

        max-width: 850px;

        line-height: 1.8;

        margin-bottom: 30px;
    }


    /* ========================================================
       BRAND BADGES
    ======================================================== */

    .brand-container {

        display: flex;

        gap: 12px;

        margin-bottom: 30px;
    }


    .brand-badge {

        padding: 10px 20px;

        background:
            rgba(255,255,255,0.80);

        border:
            1px solid rgba(20,25,30,0.10);

        color: #252a30;

        font-size: 10px;

        font-weight: 700;

        letter-spacing: 3px;

        box-shadow:
            0px 6px 18px rgba(0,0,0,0.06);

        transition:
            all 0.25s ease;
    }


    .brand-badge:hover {

        transform:
            translateY(-2px);

        box-shadow:
            0px 12px 25px rgba(0,0,0,0.10);
    }


    .brand-badge.bmw {

        border-left:
            4px solid #1c69d4;
    }


    .brand-badge.mini {

        border-left:
            4px solid #444444;
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
                135deg,
                rgba(255,255,255,0.95),
                rgba(248,249,250,0.90)
            );

        border:
            1px solid rgba(20,25,30,0.10);

        box-shadow:
            0px 10px 28px rgba(0,0,0,0.06);

        padding: 16px 20px;

        margin-bottom: 35px;

        border-radius: 5px;
    }


    .status-left {

        display: flex;

        align-items: center;

        font-size: 10px;

        letter-spacing: 2px;

        color: #3c4650;

        text-transform: uppercase;

        font-weight: 600;
    }


    .live-dot {

        width: 9px;

        height: 9px;

        background: #1c69d4;

        border-radius: 50%;

        margin-right: 10px;

        box-shadow:

            0 0 0 5px rgba(28,105,212,0.10),

            0 0 15px rgba(28,105,212,0.30);
    }


    .status-right {

        font-size: 10px;

        color: #7b858f;

        letter-spacing: 1px;
    }


    /* ========================================================
       SECTION HEADERS
    ======================================================== */

    .section-number {

        font-size: 9px;

        color: #1c69d4;

        font-weight: 700;

        letter-spacing: 3px;

        margin-bottom: 7px;
    }


    .section-title {

        font-size: 27px;

        font-weight: 600;

        color: #171a1e;

        letter-spacing: -0.8px;

        margin-bottom: 6px;
    }


    .section-description {

        font-size: 12px;

        color: #78818a;

        margin-bottom: 22px;
    }


    /* ========================================================
       KPI CARDS
    ======================================================== */

    .kpi-card {

        background:

            linear-gradient(
                145deg,
                rgba(255,255,255,0.98),
                rgba(244,246,248,0.95)
            );

        border:
            1px solid rgba(20,25,30,0.09);

        border-radius: 5px;

        padding: 23px;

        min-height: 130px;

        position: relative;

        overflow: hidden;

        box-shadow:
            0px 10px 30px rgba(0,0,0,0.06);

        transition:
            all 0.25s ease;
    }


    .kpi-card:hover {

        transform:
            translateY(-5px);

        box-shadow:
            0px 18px 40px rgba(0,0,0,0.10);

        border-color:
            rgba(28,105,212,0.30);
    }


    .kpi-card::before {

        content: "";

        position: absolute;

        top: 0;

        left: 0;

        width: 100%;

        height: 3px;

        background:

            linear-gradient(
                90deg,
                #1c69d4,
                #5da1ff,
                #d7dce1
            );
    }


    .kpi-label {

        font-size: 9px;

        letter-spacing: 2px;

        text-transform: uppercase;

        color: #7a838d;

        margin-bottom: 14px;

        font-weight: 600;
    }


    .kpi-value {

        font-size: 34px;

        font-weight: 650;

        color: #15191d;

        letter-spacing: -1.5px;
    }


    .kpi-sub {

        font-size: 10px;

        color: #8a929a;

        margin-top: 8px;
    }


    /* ========================================================
       BUTTON
    ======================================================== */

    .stButton > button {

        width: 100%;

        border-radius: 5px;

        border:
            1px solid rgba(255,255,255,0.15);

        background:

            linear-gradient(
                135deg,
                #24354a,
                #16212d
            );

        color: #ffffff;

        font-size: 10px;

        font-weight: 600;

        letter-spacing: 1.8px;

        text-transform: uppercase;

        padding: 11px 15px;

        transition:
            all 0.25s ease;

        box-shadow:
            0px 6px 18px rgba(0,0,0,0.20);
    }


    .stButton > button:hover {

        background:

            linear-gradient(
                135deg,
                #1c69d4,
                #1558b3
            );

        border-color:
            #1c69d4;

        transform:
            translateY(-2px);
    }


    /* ========================================================
       SELECTBOX
    ======================================================== */

    div[data-baseweb="select"] > div {

        background-color:
            rgba(255,255,255,0.08) !important;

        border-color:
            rgba(255,255,255,0.18) !important;

        border-radius:
            5px !important;

        color:
            #ffffff !important;
    }


    section[data-testid="stSidebar"] label {

        color: #cfd6dd !important;

        font-size: 11px !important;

        letter-spacing: 1px;
    }


    /* ========================================================
       FOOTER
    ======================================================== */

    .footer {

        border-top:
            1px solid rgba(20,25,30,0.10);

        margin-top: 65px;

        padding-top: 22px;

        padding-bottom: 20px;

        display: flex;

        justify-content: space-between;

        color: #7d858d;

        font-size: 9px;

        letter-spacing: 1.5px;

        text-transform: uppercase;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# NORMALIZE COLUMN NAME
# ============================================================

def normalize_column_name(column_name):

    column_name = str(column_name)

    column_name = column_name.strip()

    column_name = re.sub(
        r"\s+",
        " ",
        column_name
    )

    return column_name.lower()


# ============================================================
# FIND COLUMN SAFELY
# ============================================================

def find_matching_column(
    dataframe,
    target_column
):

    normalized_target = normalize_column_name(
        target_column
    )


    for column in dataframe.columns:

        if (
            normalize_column_name(column)
            == normalized_target
        ):

            return column


    return None


# ============================================================
# DATA LOADING FUNCTION
# ============================================================

def load_data():

    try:

        # ----------------------------------------------------
        # CACHE BUSTER
        # ----------------------------------------------------

        cache_buster = int(
            time.time()
        )


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
            StringIO(
                response.text
            )
        )


        # ----------------------------------------------------
        # REMOVE EMPTY ROWS
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


        return (
            df,
            response.headers
        )


    except Exception as e:

        return (
            pd.DataFrame(),
            str(e)
        )


# ============================================================
# FORMAT PERCENTAGE
# ============================================================

def format_percentage(value):

    if pd.isna(value):

        return ""


    if isinstance(
        value,
        str
    ):

        value = value.strip()


        if value == "":

            return ""


        value = value.replace(
            "%",
            ""
        )


        value = value.replace(
            ",",
            ""
        )


    try:

        numeric_value = float(
            value
        )


    except (
        ValueError,
        TypeError
    ):

        return str(
            value
        )


    # --------------------------------------------------------
    # 0.85 -> 85.00%
    # 85 -> 85.00%
    # --------------------------------------------------------

    if abs(
        numeric_value
    ) <= 1:

        numeric_value = (
            numeric_value * 100
        )


    return (
        f"{numeric_value:,.2f}%"
    )


# ============================================================
# FORMAT WHOLE NUMBER
# ============================================================

def format_whole_number(value):

    if pd.isna(value):

        return ""


    if isinstance(
        value,
        str
    ):

        value = value.strip()


        if value == "":

            return ""


        value = value.replace(
            ",",
            ""
        )


    try:

        numeric_value = float(
            value
        )


    except (
        ValueError,
        TypeError
    ):

        return str(
            value
        )


    return (
        f"{numeric_value:,.0f}"
    )


# ============================================================
# APPLY TABLE FORMATTING
# ============================================================

def format_table_data(dataframe):

    formatted_df = dataframe.copy()


    # --------------------------------------------------------
    # PERCENTAGE FORMATTING
    # --------------------------------------------------------

    for target_column in PERCENTAGE_COLUMNS:

        actual_column = find_matching_column(
            formatted_df,
            target_column
        )


        if actual_column is not None:

            formatted_df[
                actual_column
            ] = (
                formatted_df[
                    actual_column
                ]
                .apply(
                    format_percentage
                )
            )


    # --------------------------------------------------------
    # WHOLE NUMBER FORMATTING
    # --------------------------------------------------------

    for target_column in WHOLE_NUMBER_COLUMNS:

        actual_column = find_matching_column(
            formatted_df,
            target_column
        )


        if actual_column is not None:

            formatted_df[
                actual_column
            ] = (
                formatted_df[
                    actual_column
                ]
                .apply(
                    format_whole_number
                )
            )


    return formatted_df


# ============================================================
# CREATE PREMIUM HTML TABLE
# ============================================================

def create_luxury_table(dataframe):


    table_html = dataframe.to_html(
        index=False,
        escape=True,
        classes="luxury-table",
        border=0
    )


    html = f"""

    <!DOCTYPE html>

    <html>

    <head>

    <meta charset="UTF-8">


    <style>


    * {{

        box-sizing:
            border-box;
    }}


    html,
    body {{

        margin: 0;

        padding: 0;

        width: 100%;

        background:
            #ffffff;

        font-family:
            "Helvetica Neue",
            Arial,
            sans-serif;
    }}


    /* ========================================================
       TABLE WRAPPER
    ======================================================== */

    .table-wrapper {{

        width: 100%;

        max-height: 610px;

        overflow-x: auto;

        overflow-y: auto;

        background:
            #ffffff;

        border:
            1px solid #c8ced5;

        border-radius:
            6px;

    }}


    /* ========================================================
       TABLE
    ======================================================== */

    .luxury-table {{

        width: 100%;

        min-width:
            max-content;

        border-collapse:
            collapse;

        border-spacing:
            0;

        margin:
            0;

        font-size:
            12px;

        color:
            #2a2f35;

        white-space:
            nowrap;
    }}


    /* ========================================================
       TABLE HEADER
    ======================================================== */

    .luxury-table thead th {{

        background:

            linear-gradient(
                135deg,
                #202a36,
                #111820
            );

        color:
            #ffffff;

        font-size:
            10px;

        font-weight:
            600;

        letter-spacing:
            0.3px;

        padding:
            16px 14px;

        text-align:
            center;

        border-right:
            1px solid #53606d;

        border-bottom:
            2px solid #1c69d4;

        white-space:
            nowrap;

        position:
            sticky;

        top:
            0;

        z-index:
            10;
    }}


    .luxury-table thead th:first-child {{

        text-align:
            left;

        padding-left:
            18px;
    }}


    .luxury-table thead th:last-child {{

        border-right:
            none;
    }}


    /* ========================================================
       TABLE ROWS
    ======================================================== */

    .luxury-table tbody tr {{

        background:
            #ffffff;

        transition:
            background 0.18s ease;
    }}


    .luxury-table tbody tr:nth-child(even) {{

        background:
            #f5f7f9;
    }}


    .luxury-table tbody tr:hover {{

        background:
            #eaf2fc;
    }}


    /* ========================================================
       TABLE CELLS
    ======================================================== */

    .luxury-table tbody td {{

        padding:
            13px 14px;

        border-right:
            1px solid #d5dbe1;

        border-bottom:
            1px solid #d5dbe1;

        text-align:
            center;

        vertical-align:
            middle;

        color:
            #30363d;

        font-size:
            11px;
    }}


    /* ========================================================
       FIRST COLUMN
    ======================================================== */

    .luxury-table tbody td:first-child {{

        text-align:
            left;

        padding-left:
            18px;

        font-weight:
            500;

        color:
            #1d252d;
    }}


    /* ========================================================
       LAST COLUMN
    ======================================================== */

    .luxury-table tbody td:last-child {{

        border-right:
            none;
    }}


    /* ========================================================
       LAST ROW
    ======================================================== */

    .luxury-table tbody tr:last-child td {{

        border-bottom:
            none;
    }}


    /* ========================================================
       SCROLLBAR
    ======================================================== */

    .table-wrapper::-webkit-scrollbar {{

        height:
            10px;

        width:
            10px;
    }}


    .table-wrapper::-webkit-scrollbar-track {{

        background:
            #edf0f3;
    }}


    .table-wrapper::-webkit-scrollbar-thumb {{

        background:
            #9da7b1;

        border-radius:
            10px;
    }}


    .table-wrapper::-webkit-scrollbar-thumb:hover {{

        background:
            #727d88;
    }}


    </style>

    </head>


    <body>


        <div class="table-wrapper">

            {table_html}

        </div>


    </body>

    </html>

    """


    return html


# ============================================================
# SIDEBAR HEADER
# ============================================================

with st.sidebar:

    st.markdown(
        """
 <div class="sidebar-brand">

    BMW GROUP

 </div>


 <div class="sidebar-title">

    Benchmark<br>
    Intelligence

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

  PERFORMANCE FILTER

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

business_area_column = find_matching_column(
    df,
    "Business Area"
)


# ============================================================
# SIDEBAR FILTER
# ============================================================

with st.sidebar:


    if business_area_column is not None:


        business_areas = (

            df[
                business_area_column
            ]

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
    # SIDEBAR INFORMATION
    # ========================================================

    st.markdown(

        f"""

 <div class="sidebar-info">


    DATA SOURCE<br>

 <span>

    GitHub / benchmark_data.csv

 </span>


 <br><br>


    REFRESH RATE<br>

 <span>

    {AUTO_REFRESH_SECONDS} seconds

 </span>


 <br><br>


    TOTAL RECORDS<br>

 <span>

    {len(df):,}

 </span>


 <br><br>


    TOTAL COLUMNS<br>

 <span>

    {len(df.columns):,}

 </span>


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


    BMW

 <span class="muted">

    &

 </span>

    MINI


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


    A centralized executive benchmarking environment for
        performance comparison, operational visibility,
        and data-driven management decision-making.


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

    "%d %b %Y | %H:%M:%S"

)


st.markdown(

    f"""

 <div class="status-card">


 <div class="status-left">


 <div class="live-dot">

 </div>


 LIVE DATA CONNECTION


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

  Current business intelligence overview based on the selected Business Area.

 </div>

    """,

    unsafe_allow_html=True

)


# ============================================================
# KPI CALCULATIONS
# ============================================================

row_count = len(
    filtered_df
)


column_count = len(
    filtered_df.columns
)


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

k1, k2, k3, k4 = st.columns(
    4
)


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

  Available data columns

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

    Analytical performance fields

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
# SECTION 02
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

    Detailed benchmark data based on the currently selected Business Area.

 </div>

    """,

    unsafe_allow_html=True

)


# ============================================================
# REMOVE FIRST TWO COLUMNS
# ============================================================

if len(
    filtered_df.columns
) > 2:


    display_df = (

        filtered_df

        .iloc[:, 2:]

        .copy()

    )


else:


    display_df = (
        filtered_df.copy()
    )


# ============================================================
# REMOVE EMPTY COLUMNS
# ============================================================

display_df = display_df.dropna(

    axis=1,

    how="all"

)


# ============================================================
# REMOVE EMPTY ROWS
# ============================================================

display_df = display_df.dropna(

    axis=0,

    how="all"

)


# ============================================================
# RESET INDEX
# ============================================================

display_df = display_df.reset_index(
    drop=True
)


# ============================================================
# APPLY REQUIRED COLUMN FORMATTING
# ============================================================

display_df = format_table_data(
    display_df
)


# ============================================================
# PREMIUM HTML TABLE
# ============================================================

table_html = create_luxury_table(
    display_df
)


components.html(

    table_html,

    height=630,

    scrolling=False

)


# ============================================================
# FOOTER
# ============================================================

st.markdown(

    """

 <div class="footer">


 <div>

    BMW GROUP · BENCHMARKING INTELLIGENCE

 </div>


<div>

    · CONFIDENTIAL ·

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
