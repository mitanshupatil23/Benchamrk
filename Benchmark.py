import streamlit as st
import pandas as pd
import requests
import time
import re
import calendar
import numpy as np
import plotly.graph_objects as go

from io import StringIO
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="BMW | MINI Benchmark Intelligence",
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

AUTO_REFRESH_SECONDS = 60


# ============================================================
# COLUMN CONFIGURATION
# ============================================================

COLUMN_CONFIG = {

    "business_area": "Business Area",

    "month": "Month",

    "input_1": "Input 1",

    "input_2": "Input 2",

    "achieved": "Achieved",

    "projection": "Projection",

    "backlog_percent": "Backlog %",

    "backlog_units": "Backlog Units",

    "target_remaining": "Target need to achive",

    "backlog_per_day": "Backlog Units ( Per day )",

    "target_per_day": "Target need to achive ( per day )",

    "daily_target": "Daily total Target"
}


# ============================================================
# LUXURY COLOR PALETTE
# ============================================================

COLORS = {

    "background": "#080B0F",

    "background_2": "#0D1117",

    "card": "#111820",

    "card_2": "#151D26",

    "border": "#26313D",

    "text": "#F5F7FA",

    "muted": "#85919E",

    "blue": "#2F80ED",

    "blue_light": "#6AA9FF",

    "gold": "#C9A45C",

    "gold_light": "#E4C77F",

    "silver": "#B5BEC8",

    "red": "#D65F5F",

    "red_light": "#F07A7A",

    "green": "#46A37C",

    "green_light": "#70C9A1",

    "purple": "#9676E8",

    "forecast": "#AAB4C2"
}


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
<style>


/* ============================================================
   HIDE STREAMLIT TOP TOOLBAR
============================================================ */

[data-testid="stHeader"] {{
    background: transparent !important;
}}


[data-testid="stToolbar"] {{
    display: none !important;
}}


[data-testid="stDecoration"] {{
    display: none !important;
}}


#MainMenu {{
    visibility: hidden;
}}


footer {{
    visibility: hidden;
}}


/* ============================================================
   GLOBAL
============================================================ */

.stApp {{

    background:

        radial-gradient(
            circle at 90% 0%,
            rgba(47,128,237,0.12),
            transparent 30%
        ),

        radial-gradient(
            circle at 5% 95%,
            rgba(201,164,92,0.08),
            transparent 32%
        ),

        linear-gradient(
            135deg,
            #080B0F,
            #0B1016,
            #111820
        );

    color: {COLORS["text"]};

}}


.block-container {{

    padding-top: 2.5rem;

    padding-bottom: 3rem;

    max-width: 1700px;

}}


/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {{

    background:

        linear-gradient(
            180deg,
            #090E14,
            #101720,
            #080B0F
        );

    border-right:
        1px solid rgba(255,255,255,0.08);

}}


section[data-testid="stSidebar"] > div {{

    padding-top: 2rem;

}}


/* Sidebar navigation button */

[data-testid="collapsedControl"] {{

    background:
        linear-gradient(
            135deg,
            #1C69D4,
            #123B70
        ) !important;

    border:
        1px solid rgba(255,255,255,0.25) !important;

    border-radius:
        7px !important;

    color:
        white !important;

    opacity:
        1 !important;

    box-shadow:
        0 6px 20px rgba(28,105,212,0.35);

}}


[data-testid="collapsedControl"] svg {{

    fill:
        white !important;

}}


.sidebar-brand {{

    font-size:
        9px;

    letter-spacing:
        4px;

    color:
        #6F7C89;

    text-transform:
        uppercase;

    margin-bottom:
        8px;

}}


.sidebar-title {{

    font-size:
        30px;

    font-weight:
        650;

    letter-spacing:
        -1.2px;

    line-height:
        1.05;

    color:
        #FFFFFF;

    margin-bottom:
        28px;

}}


.sidebar-divider {{

    height:
        1px;

    background:

        linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.16),
            transparent
        );

    margin:
        24px 0;

}}


section[data-testid="stSidebar"] label {{

    color:
        #D4DAE1 !important;

    font-size:
        11px !important;

    letter-spacing:
        0.8px;

}}


/* ============================================================
   HEADER
============================================================ */

.top-label {{

    display:
        inline-block;

    font-size:
        9px;

    letter-spacing:
        4px;

    color:
        {COLORS["blue_light"]};

    text-transform:
        uppercase;

    border-bottom:
        2px solid {COLORS["blue"]};

    padding-bottom:
        8px;

    margin-bottom:
        18px;

}}


.main-title {{

    font-size:
        clamp(40px, 5vw, 68px);

    font-weight:
        650;

    letter-spacing:
        -3px;

    color:
        #F8FAFC;

    line-height:
        1;

}}


.main-title span {{

    color:
        #6F7B87;

    font-weight:
        300;

}}


.subtitle {{

    font-size:
        14px;

    color:
        #87929D;

    max-width:
        850px;

    line-height:
        1.8;

    margin-top:
        16px;

    margin-bottom:
        28px;

}}


/* ============================================================
   STATUS
============================================================ */

.status-card {{

    display:
        flex;

    justify-content:
        space-between;

    align-items:
        center;

    padding:
        16px 20px;

    margin-bottom:
        38px;

    background:

        linear-gradient(
            135deg,
            #141C25,
            #0E141B
        );

    border:
        1px solid {COLORS["border"]};

    border-radius:
        7px;

}}


.status-left {{

    display:
        flex;

    align-items:
        center;

    font-size:
        10px;

    letter-spacing:
        2px;

    color:
        #DCE3EA;

}}


.live-dot {{

    width:
        9px;

    height:
        9px;

    border-radius:
        50%;

    background:
        {COLORS["green"]};

    margin-right:
        10px;

    box-shadow:
        0 0 15px rgba(70,163,124,0.9);

}}


.status-right {{

    font-size:
        10px;

    color:
        #7D8995;

    letter-spacing:
        1px;

}}


/* ============================================================
   SECTION
============================================================ */

.section-number {{

    font-size:
        9px;

    color:
        {COLORS["blue_light"]};

    letter-spacing:
        3px;

    font-weight:
        700;

    margin-bottom:
        8px;

}}


.section-title {{

    font-size:
        30px;

    font-weight:
        650;

    color:
        #F5F7F9;

    letter-spacing:
        -1px;

    margin-bottom:
        6px;

}}


.section-description {{

    font-size:
        12px;

    color:
        #87939F;

    margin-bottom:
        25px;

}}


/* ============================================================
   KPI CARDS
============================================================ */

.kpi-card {{

    background:

        linear-gradient(
            145deg,
            #161F29,
            #0F151C
        );

    border:
        1px solid {COLORS["border"]};

    border-radius:
        8px;

    padding:
        22px;

    min-height:
        140px;

    position:
        relative;

    overflow:
        hidden;

    transition:
        0.25s;

}}


.kpi-card:hover {{

    transform:
        translateY(-4px);

    border-color:
        rgba(47,128,237,0.65);

}}


.kpi-card::before {{

    content:
        "";

    position:
        absolute;

    top:
        0;

    left:
        0;

    width:
        100%;

    height:
        3px;

    background:

        linear-gradient(
            90deg,
            {COLORS["blue"]},
            {COLORS["blue_light"]},
            {COLORS["gold"]}
        );

}}


.kpi-label {{

    font-size:
        9px;

    letter-spacing:
        2px;

    text-transform:
        uppercase;

    color:
        #87929D;

    margin-bottom:
        15px;

}}


.kpi-value {{

    font-size:
        30px;

    font-weight:
        650;

    color:
        #F6F8FA;

    letter-spacing:
        -1px;

}}


.kpi-sub {{

    font-size:
        10px;

    color:
        #7C8792;

    margin-top:
        8px;

}}


/* ============================================================
   INSIGHT CARDS
============================================================ */

.insight-card {{

    background:

        linear-gradient(
            145deg,
            #141C25,
            #0E141B
        );

    border:
        1px solid #25303B;

    border-radius:
        8px;

    padding:
        20px;

    min-height:
        130px;

}}


.insight-title {{

    font-size:
        10px;

    letter-spacing:
        1.5px;

    color:
        {COLORS["gold_light"]};

    margin-bottom:
        12px;

    text-transform:
        uppercase;

}}


.insight-text {{

    font-size:
        12px;

    line-height:
        1.7;

    color:
        #B8C1CA;

}}


/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {{

    width:
        100%;

    background:

        linear-gradient(
            135deg,
            #182331,
            #101820
        );

    color:
        #FFFFFF;

    border:
        1px solid #2A3745;

    border-radius:
        6px;

    font-size:
        10px;

    letter-spacing:
        1.5px;

    text-transform:
        uppercase;

}}


.stButton > button:hover {{

    border-color:
        {COLORS["blue"]};

    background:

        linear-gradient(
            135deg,
            #1C69D4,
            #164F9F
        );

}}


/* ============================================================
   FOOTER
============================================================ */

.footer {{

    margin-top:
        70px;

    padding-top:
        25px;

    border-top:
        1px solid #222B35;

    display:
        flex;

    justify-content:
        space-between;

    color:
        #65707B;

    font-size:
        9px;

    letter-spacing:
        1.5px;

}}


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
# FIND MATCHING COLUMN
# ============================================================

def find_matching_column(dataframe, target_column):

    target = normalize_column_name(
        target_column
    )

    for column in dataframe.columns:

        if normalize_column_name(column) == target:

            return column

    return None


# ============================================================
# SAFE NUMERIC
# ============================================================

def safe_numeric(series):

    cleaned = (

        series

        .astype(str)

        .str.replace("%", "", regex=False)

        .str.replace(",", "", regex=False)

        .str.strip()

    )

    return pd.to_numeric(
        cleaned,
        errors="coerce"
    )


# ============================================================
# CONVERT PERCENTAGE
# ============================================================

def convert_percentage(series):

    numeric = safe_numeric(series)

    return numeric.apply(

        lambda x:

        x * 100

        if pd.notna(x) and abs(x) <= 1

        else x

    )


# ============================================================
# MONTH SORT
# ============================================================

def get_month_sort_value(month_value):

    if pd.isna(month_value):

        return 999999


    month_text = str(
        month_value
    ).strip()


    month_text = month_text.replace(
        "’",
        "'"
    )


    formats = [

        "%b'%y",
        "%b %Y",
        "%B %Y",
        "%b-%Y",
        "%B-%Y",
        "%Y-%m",
        "%m/%Y",
        "%Y/%m"

    ]


    for fmt in formats:

        try:

            dt = datetime.strptime(
                month_text,
                fmt
            )

            return (

                dt.year * 100
                +
                dt.month

            )

        except Exception:

            pass


    month_match = re.search(
        r"([A-Za-z]{3,9})",
        month_text
    )


    year_match = re.search(
        r"(\d{2,4})",
        month_text
    )


    if month_match:

        month_name = (
            month_match
            .group(1)
            .lower()
        )


        month_number = None


        for i in range(1, 13):

            if (
                calendar.month_name[i]
                .lower()
                .startswith(month_name[:3])
            ):

                month_number = i

                break


        if month_number:

            if year_match:

                year_value = int(
                    year_match.group(1)
                )

                if year_value < 100:

                    year_value += 2000

            else:

                year_value = 2026


            return (
                year_value * 100
                +
                month_number
            )


    return 999999


# ============================================================
# GET NEXT MONTH
# ============================================================

def get_future_month_labels(last_sort, periods=3):

    labels = []

    if last_sort == 999999:

        return [
            f"Forecast {i}"
            for i in range(1, periods + 1)
        ]


    year = int(last_sort // 100)

    month = int(last_sort % 100)


    for _ in range(periods):

        month += 1

        if month > 12:

            month = 1
            year += 1


        labels.append(
            f"{calendar.month_abbr[month]}'{str(year)[-2:]}"
        )


    return labels


# ============================================================
# DATA LOADING
# ============================================================

def load_data():

    try:

        cache_buster = int(
            time.time()
        )


        fresh_url = (
            f"{DATA_URL}?t={cache_buster}"
        )


        response = requests.get(

            fresh_url,

            timeout=20,

            headers={

                "Cache-Control":
                    "no-cache",

                "Pragma":
                    "no-cache"

            }

        )


        response.raise_for_status()


        dataframe = pd.read_csv(

            StringIO(
                response.text
            )

        )


        dataframe = dataframe.dropna(
            axis=0,
            how="all"
        )


        dataframe.columns = (

            dataframe.columns
            .astype(str)
            .str.strip()

        )


        dataframe = dataframe.loc[
            :,
            ~dataframe.columns.str.startswith(
                "Unnamed"
            )
        ]


        dataframe = dataframe.loc[
            :,
            ~dataframe.columns.duplicated()
        ]


        dataframe = dataframe.reset_index(
            drop=True
        )


        return dataframe, None


    except Exception as error:

        return (
            pd.DataFrame(),
            str(error)
        )


# ============================================================
# LOAD DATA
# ============================================================

df, error_message = load_data()


if df.empty:

    st.error(
        "Unable to load benchmark data."
    )

    st.caption(
        error_message
    )

    st.stop()


# ============================================================
# DETECT COLUMNS
# ============================================================

detected_columns = {}


for key, column_name in COLUMN_CONFIG.items():

    detected_columns[key] = (

        find_matching_column(
            df,
            column_name
        )

    )


business_area_column = detected_columns[
    "business_area"
]

month_column = detected_columns[
    "month"
]


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
NAVIGATION
</div>
        """,

        unsafe_allow_html=True
    )


    page = st.radio(

        "Dashboard Page",

        [

            "01  Executive Overview",

            "02  Competitive Gap",

            "03  Target Recovery",

            "04  Business Area Comparison"

        ],

        label_visibility="collapsed"

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


    # ========================================================
    # BUSINESS AREA FILTER
    # ========================================================

    if business_area_column:


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


    # ========================================================
    # MONTH FILTER
    # ========================================================

    month_filter_df = df.copy()


    if (
        business_area_column
        and
        selected_business_area != "All"
    ):

        month_filter_df = (

            month_filter_df[

                month_filter_df[
                    business_area_column
                ]

                .astype(str)

                .str.strip()

                == selected_business_area

            ]

        )


    if month_column:


        months = (

            month_filter_df[
                month_column
            ]

            .dropna()

            .astype(str)

            .str.strip()

        )


        months = (

            months[
                months != ""
            ]

            .unique()

            .tolist()

        )


        months = sorted(
            months,
            key=get_month_sort_value
        )


        selected_months = st.multiselect(

            "Month",

            options=months,

            default=[]

        )


    else:

        selected_months = []


    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True
    )


    if st.button(
        "↻ Refresh Data"
    ):

        st.rerun()


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if (
    business_area_column
    and
    selected_business_area != "All"
):

    filtered_df = (

        filtered_df[

            filtered_df[
                business_area_column
            ]

            .astype(str)

            .str.strip()

            == selected_business_area

        ]

    )


if (
    month_column
    and
    selected_months
):

    filtered_df = (

        filtered_df[

            filtered_df[
                month_column
            ]

            .astype(str)

            .str.strip()

            .isin(
                selected_months
            )

        ]

    )


# ============================================================
# ANALYTICAL DATAFRAME
# ============================================================

analysis_df = filtered_df.copy()


for key in [

    "input_1",
    "input_2",
    "backlog_units",
    "target_remaining",
    "backlog_per_day",
    "target_per_day",
    "daily_target"

]:

    column = detected_columns[key]


    if column:

        analysis_df[
            f"{key}_numeric"
        ] = safe_numeric(
            analysis_df[column]
        )


for key in [

    "achieved",
    "projection",
    "backlog_percent"

]:

    column = detected_columns[key]


    if column:

        analysis_df[
            f"{key}_numeric"
        ] = convert_percentage(
            analysis_df[column]
        )


# ============================================================
# MONTH SORT
# ============================================================

if month_column:

    analysis_df[
        "Month Sort"
    ] = (

        analysis_df[
            month_column
        ]

        .apply(
            get_month_sort_value
        )

    )


# ============================================================
# HEADER
# ============================================================

st.markdown(

    """
<div class="top-label">
BMW / MINI BENCHMARK INTELLIGENCE
</div>
    """,

    unsafe_allow_html=True
)


st.markdown(

    """
<div class="main-title">

BMW <span>&</span> MINI

<span>Benchmark Intelligence</span>

</div>
    """,

    unsafe_allow_html=True
)


st.markdown(

    """
<div class="subtitle">

Executive benchmarking environment designed for
performance visibility, competitive positioning,
target recovery and operational decision-making.

</div>
    """,

    unsafe_allow_html=True
)


# ============================================================
# STATUS
# ============================================================

data_fetch_time = datetime.now().strftime(
    "%d %b %Y | %H:%M:%S"
)


st.markdown(

    f"""
<div class="status-card">

<div class="status-left">

<div class="live-dot"></div>
LIVE BENCHMARK DATA
</div>

<div class="status-right">

LAST FETCH: {data_fetch_time}

&nbsp;&nbsp; | &nbsp;&nbsp;

RECORDS: {len(filtered_df):,}

</div>

</div>
    """,

    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_average(column_name):

    if column_name in analysis_df.columns:

        return analysis_df[
            column_name
        ].mean()


    return np.nan


def calculate_sum(column_name):

    if column_name in analysis_df.columns:

        return analysis_df[
            column_name
        ].sum()


    return 0


def format_percent(value):

    if pd.isna(value):

        return "-"


    return f"{value:.1f}%"


def format_number(value):

    if pd.isna(value):

        return "-"


    return f"{value:,.0f}"


def create_forecast(values, periods=3):

    values = pd.Series(values).dropna()


    if len(values) == 0:

        return []


    if len(values) == 1:

        growth = 0


    else:

        growth = (
            values.iloc[-1]
            -
            values.iloc[-2]
        )


    forecasts = []

    current_value = values.iloc[-1]


    for _ in range(periods):

        current_value = (
            current_value
            +
            growth
        )

        forecasts.append(
            current_value
        )


    return forecasts


# ============================================================
# KPI VALUES
# ============================================================

achieved_avg = calculate_average(
    "achieved_numeric"
)


projection_avg = calculate_average(
    "projection_numeric"
)


backlog_percent_avg = calculate_average(
    "backlog_percent_numeric"
)


backlog_units_sum = calculate_sum(
    "backlog_units_numeric"
)


input_1_sum = calculate_sum(
    "input_1_numeric"
)


input_2_sum = calculate_sum(
    "input_2_numeric"
)


target_remaining_sum = calculate_sum(
    "target_remaining_numeric"
)


backlog_per_day_avg = calculate_average(
    "backlog_per_day_numeric"
)


target_per_day_avg = calculate_average(
    "target_per_day_numeric"
)


daily_target_avg = calculate_average(
    "daily_target_numeric"
)


# ============================================================
# PERFORMANCE GAP
# ============================================================

if (
    pd.notna(projection_avg)
    and
    pd.notna(achieved_avg)
):

    performance_gap = (
        projection_avg
        -
        achieved_avg
    )

else:

    performance_gap = np.nan


# ============================================================
# PAGE 01
# EXECUTIVE OVERVIEW
# ============================================================

if page == "01  Executive Overview":


    st.markdown(

        """
<div class="section-number">
01 / EXECUTIVE OVERVIEW
</div>

<div class="section-title">
Performance Snapshot
</div>

<div class="section-description">
High-level business performance, competitor positioning
and forward performance visibility.
</div>
        """,

        unsafe_allow_html=True
    )


    # ========================================================
    # KPI SCORECARDS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.markdown(

            f"""
<div class="kpi-card">

<div class="kpi-label">
ACHIEVED
</div>

<div class="kpi-value">
{format_percent(achieved_avg)}
</div>

<div class="kpi-sub">
Current target achievement
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    with c2:

        st.markdown(

            f"""
<div class="kpi-card">

<div class="kpi-label">
COMPETITOR PROJECTION
</div>

<div class="kpi-value">
{format_percent(projection_avg)}
</div>

<div class="kpi-sub">
Competitor performance level
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    with c3:

        st.markdown(

            f"""
<div class="kpi-card">

<div class="kpi-label">
PERFORMANCE GAP
</div>

<div class="kpi-value">
{format_percent(performance_gap)}
</div>

<div class="kpi-sub">
Gap against competitor
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    with c4:

        st.markdown(

            f"""
<div class="kpi-card">

<div class="kpi-label">
BACKLOG UNITS
</div>

<div class="kpi-value">
{format_number(backlog_units_sum)}
</div>

<div class="kpi-sub">
Units behind competitor
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # ========================================================
    # ACHIEVED VS PROJECTION TREND
    # ========================================================

    if (
        month_column
        and
        "achieved_numeric" in analysis_df.columns
        and
        "projection_numeric" in analysis_df.columns
    ):


        trend_df = (

            analysis_df

            .groupby(

                [
                    month_column,
                    "Month Sort"
                ],

                as_index=False

            )

            .agg(

                Achieved=(
                    "achieved_numeric",
                    "mean"
                ),

                Projection=(
                    "projection_numeric",
                    "mean"
                )

            )

            .sort_values(
                "Month Sort"
            )

        )


        if not trend_df.empty:


            fig = go.Figure()


            # ------------------------------------------------
            # ACHIEVED
            # ------------------------------------------------

            fig.add_trace(

                go.Scatter(

                    x=trend_df[
                        month_column
                    ],

                    y=trend_df[
                        "Achieved"
                    ],

                    mode="lines+markers",

                    name="Achieved",

                    line=dict(

                        color=COLORS[
                            "blue"
                        ],

                        width=4

                    ),

                    marker=dict(

                        size=9,

                        color=COLORS[
                            "blue"
                        ]

                    )

                )

            )


            # ------------------------------------------------
            # PROJECTION
            # ------------------------------------------------

            fig.add_trace(

                go.Scatter(

                    x=trend_df[
                        month_column
                    ],

                    y=trend_df[
                        "Projection"
                    ],

                    mode="lines+markers",

                    name="Projection",

                    line=dict(

                        color=COLORS[
                            "gold"
                        ],

                        width=4

                    ),

                    marker=dict(

                        size=9,

                        color=COLORS[
                            "gold"
                        ]

                    )

                )

            )


            # =================================================
            # FUTURE FORECAST
            # =================================================

            if len(trend_df) >= 1:


                future_months = get_future_month_labels(

                    trend_df[
                        "Month Sort"
                    ].iloc[-1],

                    periods=3

                )


                achieved_forecast = create_forecast(

                    trend_df[
                        "Achieved"
                    ],

                    periods=3

                )


                projection_forecast = create_forecast(

                    trend_df[
                        "Projection"
                    ],

                    periods=3

                )


                achieved_x = [

                    trend_df[
                        month_column
                    ].iloc[-1]

                ] + future_months


                achieved_y = [

                    trend_df[
                        "Achieved"
                    ].iloc[-1]

                ] + achieved_forecast


                projection_x = [

                    trend_df[
                        month_column
                    ].iloc[-1]

                ] + future_months


                projection_y = [

                    trend_df[
                        "Projection"
                    ].iloc[-1]

                ] + projection_forecast


                fig.add_trace(

                    go.Scatter(

                        x=achieved_x,

                        y=achieved_y,

                        mode="lines+markers",

                        name="Achieved Forecast",

                        line=dict(

                            color=COLORS[
                                "blue_light"
                            ],

                            width=3,

                            dash="dash"

                        ),

                        marker=dict(
                            size=8
                        )

                    )

                )


                fig.add_trace(

                    go.Scatter(

                        x=projection_x,

                        y=projection_y,

                        mode="lines+markers",

                        name="Projection Forecast",

                        line=dict(

                            color=COLORS[
                                "gold_light"
                            ],

                            width=3,

                            dash="dash"

                        ),

                        marker=dict(
                            size=8
                        )

                    )

                )


            # =================================================
            # LAYOUT
            # =================================================

            fig.update_layout(

                height=520,

                paper_bgcolor=COLORS[
                    "background"
                ],

                plot_bgcolor=COLORS[
                    "background"
                ],

                hovermode="x unified",

                margin=dict(

                    l=30,

                    r=30,

                    t=90,

                    b=70

                ),

                legend=dict(

                    orientation="h",

                    yanchor="bottom",

                    y=1.08,

                    xanchor="center",

                    x=0.5,

                    font=dict(

                        color=COLORS[
                            "text"
                        ],

                        size=13

                    )

                )

            )


            fig.update_xaxes(

                title="Month",

                tickfont=dict(

                    color=COLORS[
                        "text"
                    ]

                ),

                showgrid=False

            )


            fig.update_yaxes(

                title="Performance %",

                ticksuffix="%",

                tickfont=dict(

                    color=COLORS[
                        "text"
                    ]

                ),

                gridcolor=
                    "rgba(255,255,255,0.08)",

                zeroline=False

            )


            st.plotly_chart(

                fig,

                use_container_width=True,

                config={
                    "displayModeBar": False
                }

            )


    # ========================================================
    # EXECUTIVE INSIGHTS
    # ========================================================

    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown(

        """
<div class="section-number">
KEY INSIGHTS
</div>

<div class="section-title">
Executive Intelligence
</div>

<div class="section-description">
Automated interpretation of the current benchmark position.
</div>
        """,

        unsafe_allow_html=True
    )


    i1, i2, i3 = st.columns(3)


    # --------------------------------------------------------
    # PERFORMANCE INSIGHT
    # --------------------------------------------------------

    if pd.notna(performance_gap):

        if performance_gap > 0:

            performance_message = (

                f"Current performance is "
                f"<b>{performance_gap:.1f}% below</b> "
                f"competitor projection."
            )

        elif performance_gap < 0:

            performance_message = (

                f"Current performance is "
                f"<b>{abs(performance_gap):.1f}% ahead</b> "
                f"of competitor projection."
            )

        else:

            performance_message = (

                "Current performance is aligned "
                "with competitor projection."
            )

    else:

        performance_message = (
            "Performance gap information "
            "is currently unavailable."
        )


    with i1:

        st.markdown(

            f"""
<div class="insight-card">

<div class="insight-title">
COMPETITIVE POSITION
</div>

<div class="insight-text">
{performance_message}
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # BACKLOG INSIGHT
    # --------------------------------------------------------

    if backlog_units_sum > 0:

        backlog_message = (

            f"The business currently carries "
            f"<b>{format_number(backlog_units_sum)}</b> "
            f"backlog units against the competitive benchmark."
        )

    else:

        backlog_message = (

            "No significant backlog unit pressure "
            "is currently identified."
        )


    with i2:

        st.markdown(

            f"""
<div class="insight-card">

<div class="insight-title">
OPERATIONAL PRESSURE
</div>

<div class="insight-text">
{backlog_message}
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # RECOVERY INSIGHT
    # --------------------------------------------------------

    if target_remaining_sum > 0:

        recovery_message = (

            f"<b>{format_number(target_remaining_sum)}</b> "
            f"units remain to achieve the current target. "
            f"Daily recovery requirement is "
            f"<b>{format_number(target_per_day_avg)}</b> units."
        )

    else:

        recovery_message = (

            "Current target requirement appears "
            "to be substantially completed."
        )


    with i3:

        st.markdown(

            f"""
<div class="insight-card">

<div class="insight-title">
RECOVERY REQUIREMENT
</div>

<div class="insight-text">
{recovery_message}
</div>

</div>
            """,

            unsafe_allow_html=True
        )


# ============================================================
# PAGE 02
# COMPETITIVE GAP
# ============================================================

elif page == "02  Competitive Gap":


    st.markdown(

        """
<div class="section-number">
02 / COMPETITIVE GAP
</div>

<div class="section-title">
Competitive Position
</div>

<div class="section-description">
Performance gap, backlog pressure and competitive positioning analysis.
</div>
        """,

        unsafe_allow_html=True
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.markdown(

            f"""
<div class="kpi-card">

<div class="kpi-label">
AVERAGE BACKLOG
</div>

<div class="kpi-value">
{format_percent(backlog_percent_avg)}
</div>

<div class="kpi-sub">
Average competitive gap
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    with c2:

        st.markdown(

            f"""
<div class="kpi-card">

<div class="kpi-label">
BACKLOG UNITS
</div>

<div class="kpi-value">
{format_number(backlog_units_sum)}
</div>

<div class="kpi-sub">
Total units behind benchmark
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    with c3:

        st.markdown(

            f"""
<div class="kpi-card">

<div class="kpi-label">
COMPETITOR GAP
</div>

<div class="kpi-value">
{format_percent(performance_gap)}
</div>

<div class="kpi-sub">
Projection versus achieved
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # ========================================================
    # COMPETITIVE GAP CHARTS
    # ========================================================

    if month_column:


        aggregation = {}


        if "backlog_percent_numeric" in analysis_df.columns:

            aggregation[
                "Backlog Percent"
            ] = (
                "backlog_percent_numeric",
                "mean"
            )


        if "backlog_units_numeric" in analysis_df.columns:

            aggregation[
                "Backlog Units"
            ] = (
                "backlog_units_numeric",
                "sum"
            )


        if aggregation:


            gap_df = (

                analysis_df

                .groupby(

                    [
                        month_column,
                        "Month Sort"
                    ],

                    as_index=False

                )

                .agg(
                    **aggregation
                )

                .sort_values(
                    "Month Sort"
                )

            )


            if not gap_df.empty:


                col_gap_1, col_gap_2 = st.columns(2)


                # ------------------------------------------------
                # BACKLOG %
                # ------------------------------------------------

                with col_gap_1:


                    if "Backlog Percent" in gap_df.columns:


                        fig_gap = go.Figure()


                        fig_gap.add_trace(

                            go.Scatter(

                                x=gap_df[
                                    month_column
                                ],

                                y=gap_df[
                                    "Backlog Percent"
                                ],

                                mode="lines+markers",

                                name="Backlog %",

                                line=dict(

                                    color=COLORS[
                                        "red_light"
                                    ],

                                    width=4

                                ),

                                marker=dict(
                                    size=8
                                )

                            )

                        )


                        fig_gap.update_layout(

                            title="Backlog % Trend",

                            height=420,

                            paper_bgcolor=COLORS[
                                "background"
                            ],

                            plot_bgcolor=COLORS[
                                "background"
                            ],

                            legend=dict(

                                font=dict(

                                    color=COLORS[
                                        "text"
                                    ]

                                )

                            )

                        )


                        fig_gap.update_xaxes(

                            tickfont=dict(
                                color=COLORS["text"]
                            ),

                            showgrid=False

                        )


                        fig_gap.update_yaxes(

                            ticksuffix="%",

                            tickfont=dict(
                                color=COLORS["text"]
                            ),

                            gridcolor=
                                "rgba(255,255,255,0.08)"

                        )


                        st.plotly_chart(

                            fig_gap,

                            use_container_width=True,

                            config={
                                "displayModeBar": False
                            }

                        )


                # ------------------------------------------------
                # BACKLOG UNITS
                # ------------------------------------------------

                with col_gap_2:


                    if "Backlog Units" in gap_df.columns:


                        fig_units = go.Figure()


                        fig_units.add_trace(

                            go.Bar(

                                x=gap_df[
                                    month_column
                                ],

                                y=gap_df[
                                    "Backlog Units"
                                ],

                                name="Backlog Units",

                                marker_color=COLORS[
                                    "purple"
                                ]

                            )

                        )


                        fig_units.update_layout(

                            title="Backlog Units Trend",

                            height=420,

                            paper_bgcolor=COLORS[
                                "background"
                            ],

                            plot_bgcolor=COLORS[
                                "background"
                            ],

                            legend=dict(

                                font=dict(

                                    color=COLORS[
                                        "text"
                                    ]

                                )

                            )

                        )


                        fig_units.update_xaxes(

                            tickfont=dict(
                                color=COLORS["text"]
                            ),

                            showgrid=False

                        )


                        fig_units.update_yaxes(

                            tickfont=dict(
                                color=COLORS["text"]
                            ),

                            gridcolor=
                                "rgba(255,255,255,0.08)"

                        )


                        st.plotly_chart(

                            fig_units,

                            use_container_width=True,

                            config={
                                "displayModeBar": False
                            }

                        )


# ============================================================
# PAGE 03
# TARGET RECOVERY
# ============================================================

elif page == "03  Target Recovery":


    st.markdown(

        """
<div class="section-number">
03 / TARGET RECOVERY
</div>

<div class="section-title">
Recovery Strategy
</div>

<div class="section-description">
Actual performance, target position and required recovery effort.
</div>
        """,

        unsafe_allow_html=True
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.markdown(

            f"""
<div class="kpi-card">

<div class="kpi-label">
ACTUAL
</div>

<div class="kpi-value">
{format_number(input_1_sum)}
</div>

<div class="kpi-sub">
Current achieved units
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    with c2:

        st.markdown(

            f"""
<div class="kpi-card">

<div class="kpi-label">
TARGET
</div>

<div class="kpi-value">
{format_number(input_2_sum)}
</div>

<div class="kpi-sub">
Current target units
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    with c3:

        st.markdown(

            f"""
<div class="kpi-card">

<div class="kpi-label">
REMAINING
</div>

<div class="kpi-value">
{format_number(target_remaining_sum)}
</div>

<div class="kpi-sub">
Target still required
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    with c4:

        st.markdown(

            f"""
<div class="kpi-card">

<div class="kpi-label">
DAILY RECOVERY
</div>

<div class="kpi-value">
{format_number(target_per_day_avg)}
</div>

<div class="kpi-sub">
Required units per day
</div>

</div>
            """,

            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # ========================================================
    # ACTUAL VS TARGET
    # ========================================================

    if (
        month_column
        and
        "input_1_numeric" in analysis_df.columns
        and
        "input_2_numeric" in analysis_df.columns
    ):


        actual_target_df = (

            analysis_df

            .groupby(

                [
                    month_column,
                    "Month Sort"
                ],

                as_index=False

            )

            .agg(

                Actual=(

                    "input_1_numeric",

                    "sum"

                ),

                Target=(

                    "input_2_numeric",

                    "sum"

                )

            )

            .sort_values(
                "Month Sort"
            )

        )


        if not actual_target_df.empty:


            fig_actual_target = go.Figure()


            fig_actual_target.add_trace(

                go.Scatter(

                    x=actual_target_df[
                        month_column
                    ],

                    y=actual_target_df[
                        "Actual"
                    ],

                    mode="lines+markers",

                    name="Actual",

                    line=dict(

                        color=COLORS[
                            "blue"
                        ],

                        width=4

                    ),

                    marker=dict(
                        size=9
                    )

                )

            )


            fig_actual_target.add_trace(

                go.Scatter(

                    x=actual_target_df[
                        month_column
                    ],

                    y=actual_target_df[
                        "Target"
                    ],

                    mode="lines+markers",

                    name="Target",

                    line=dict(

                        color=COLORS[
                            "gold"
                        ],

                        width=4

                    ),

                    marker=dict(
                        size=9
                    )

                )

            )


            # =================================================
            # FORECAST
            # =================================================

            future_months = get_future_month_labels(

                actual_target_df[
                    "Month Sort"
                ].iloc[-1],

                periods=3

            )


            actual_forecast = create_forecast(

                actual_target_df[
                    "Actual"
                ],

                periods=3

            )


            target_forecast = create_forecast(

                actual_target_df[
                    "Target"
                ],

                periods=3

            )


            fig_actual_target.add_trace(

                go.Scatter(

                    x=[

                        actual_target_df[
                            month_column
                        ].iloc[-1]

                    ] + future_months,

                    y=[

                        actual_target_df[
                            "Actual"
                        ].iloc[-1]

                    ] + actual_forecast,

                    mode="lines+markers",

                    name="Actual Forecast",

                    line=dict(

                        color=COLORS[
                            "blue_light"
                        ],

                        width=3,

                        dash="dash"

                    )

                )

            )


            fig_actual_target.add_trace(

                go.Scatter(

                    x=[

                        actual_target_df[
                            month_column
                        ].iloc[-1]

                    ] + future_months,

                    y=[

                        actual_target_df[
                            "Target"
                        ].iloc[-1]

                    ] + target_forecast,

                    mode="lines+markers",

                    name="Target Forecast",

                    line=dict(

                        color=COLORS[
                            "gold_light"
                        ],

                        width=3,

                        dash="dash"

                    )

                )

            )


            fig_actual_target.update_layout(

                height=520,

                paper_bgcolor=COLORS[
                    "background"
                ],

                plot_bgcolor=COLORS[
                    "background"
                ],

                hovermode="x unified",

                margin=dict(

                    l=30,

                    r=30,

                    t=90,

                    b=70

                ),

                legend=dict(

                    orientation="h",

                    yanchor="bottom",

                    y=1.08,

                    xanchor="center",

                    x=0.5,

                    font=dict(

                        color=COLORS[
                            "text"
                        ],

                        size=13

                    )

                )

            )


            fig_actual_target.update_xaxes(

                title="Reporting Period",

                tickfont=dict(
                    color=COLORS["text"]
                ),

                showgrid=False

            )


            fig_actual_target.update_yaxes(

                title="Units",

                tickfont=dict(
                    color=COLORS["text"]
                ),

                gridcolor=
                    "rgba(255,255,255,0.08)",

                zeroline=False

            )


            st.plotly_chart(

                fig_actual_target,

                use_container_width=True,

                config={
                    "displayModeBar": False
                }

            )


    # ========================================================
    # DAILY REQUIREMENT
    # ========================================================

    recovery_1, recovery_2 = st.columns(2)


    with recovery_1:


        st.markdown(

            """
<div class="section-number">
RECOVERY PRESSURE
</div>

<div class="section-title">
Daily Requirement
</div>
            """,

            unsafe_allow_html=True
        )


        fig_daily = go.Figure()


        fig_daily.add_trace(

            go.Bar(

                x=[

                    "Backlog / Day",

                    "Target Recovery / Day",

                    "Daily Target"

                ],

                y=[

                    backlog_per_day_avg,

                    target_per_day_avg,

                    daily_target_avg

                ],

                marker_color=[

                    COLORS["red"],

                    COLORS["gold"],

                    COLORS["blue"]

                ]

            )

        )


        fig_daily.update_layout(

            height=400,

            paper_bgcolor=COLORS[
                "background"
            ],

            plot_bgcolor=COLORS[
                "background"
            ],

            showlegend=False

        )


        fig_daily.update_xaxes(

            tickfont=dict(
                color=COLORS["text"]
            )

        )


        fig_daily.update_yaxes(

            gridcolor=
                "rgba(255,255,255,0.08)",

            tickfont=dict(
                color=COLORS["text"]
            )

        )


        st.plotly_chart(

            fig_daily,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

        )


    with recovery_2:


        st.markdown(

            """
<div class="section-number">
RECOVERY INTELLIGENCE
</div>

<div class="section-title">
Operational Requirement
</div>
            """,

            unsafe_allow_html=True
        )


        if input_2_sum > 0:

            completion = (
                input_1_sum
                /
                input_2_sum
                *
                100
            )

        else:

            completion = 0


        fig_indicator = go.Figure(


            go.Indicator(

                mode="gauge+number",

                value=completion,

                number={

                    "suffix": "%",

                    "font": {

                        "color":
                            COLORS["text"],

                        "size": 50

                    }

                },

                gauge={

                    "axis": {

                        "range": [0, 130],

                        "tickcolor":
                            COLORS["silver"]

                    },

                    "bar": {

                        "color":
                            COLORS["blue"]

                    },

                    "bgcolor":
                        COLORS["card"],

                    "bordercolor":
                        COLORS["border"]

                }

            )

        )


        fig_indicator.update_layout(

            height=400,

            paper_bgcolor=COLORS[
                "background"
            ],

            font={

                "color":
                    COLORS["text"]

            }

        )


        st.plotly_chart(

            fig_indicator,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

        )


# ============================================================
# PAGE 04
# BUSINESS AREA COMPARISON
# ============================================================

elif page == "04  Business Area Comparison":


    st.markdown(

        """
<div class="section-number">
04 / BUSINESS AREA COMPARISON
</div>

<div class="section-title">
Business Performance Ranking
</div>

<div class="section-description">
Comparison across performance, competitor positioning
and operational pressure.
</div>
        """,

        unsafe_allow_html=True
    )


    if not business_area_column:

        st.warning(
            "Business Area column is not available."
        )


    else:


        comparison_df = df.copy()


        if (
            month_column
            and
            selected_months
        ):

            comparison_df = (

                comparison_df[

                    comparison_df[
                        month_column
                    ]

                    .astype(str)

                    .str.strip()

                    .isin(
                        selected_months
                    )

                ]

            )


        # ====================================================
        # NUMERIC COLUMNS
        # ====================================================

        if detected_columns["achieved"]:

            comparison_df[
                "Achieved Numeric"
            ] = convert_percentage(

                comparison_df[

                    detected_columns[
                        "achieved"
                    ]

                ]

            )


        if detected_columns["projection"]:

            comparison_df[
                "Projection Numeric"
            ] = convert_percentage(

                comparison_df[

                    detected_columns[
                        "projection"
                    ]

                ]

            )


        if detected_columns["backlog_percent"]:

            comparison_df[
                "Backlog Percent Numeric"
            ] = convert_percentage(

                comparison_df[

                    detected_columns[
                        "backlog_percent"
                    ]

                ]

            )


        if detected_columns["backlog_units"]:

            comparison_df[
                "Backlog Units Numeric"
            ] = safe_numeric(

                comparison_df[

                    detected_columns[
                        "backlog_units"
                    ]

                ]

            )


        aggregation = {}


        if "Achieved Numeric" in comparison_df.columns:

            aggregation[
                "Achieved"
            ] = (
                "Achieved Numeric",
                "mean"
            )


        if "Projection Numeric" in comparison_df.columns:

            aggregation[
                "Projection"
            ] = (
                "Projection Numeric",
                "mean"
            )


        if "Backlog Percent Numeric" in comparison_df.columns:

            aggregation[
                "Backlog %"
            ] = (
                "Backlog Percent Numeric",
                "mean"
            )


        if "Backlog Units Numeric" in comparison_df.columns:

            aggregation[
                "Backlog Units"
            ] = (
                "Backlog Units Numeric",
                "sum"
            )


        ranking_df = (

            comparison_df

            .groupby(

                business_area_column,

                as_index=False

            )

            .agg(
                **aggregation
            )

        )


        # ====================================================
        # PERFORMANCE RANKING
        # ====================================================

        if (
            "Achieved" in ranking_df.columns
            and
            "Projection" in ranking_df.columns
        ):


            performance_df = (

                ranking_df

                .sort_values(

                    "Achieved",

                    ascending=False

                )

            )


            fig_ranking = go.Figure()


            fig_ranking.add_trace(

                go.Bar(

                    x=performance_df[
                        business_area_column
                    ],

                    y=performance_df[
                        "Achieved"
                    ],

                    name="Achieved",

                    marker_color=COLORS[
                        "blue"
                    ]

                )

            )


            fig_ranking.add_trace(

                go.Bar(

                    x=performance_df[
                        business_area_column
                    ],

                    y=performance_df[
                        "Projection"
                    ],

                    name="Projection",

                    marker_color=COLORS[
                        "gold"
                    ]

                )

            )


            fig_ranking.update_layout(

                title="Performance Ranking",

                barmode="group",

                height=500,

                paper_bgcolor=COLORS[
                    "background"
                ],

                plot_bgcolor=COLORS[
                    "background"
                ],

                legend=dict(

                    orientation="h",

                    y=1.08,

                    x=0.5,

                    xanchor="center",

                    font=dict(

                        color=COLORS[
                            "text"
                        ],

                        size=13

                    )

                )

            )


            fig_ranking.update_xaxes(

                tickfont=dict(
                    color=COLORS["text"]
                ),

                showgrid=False

            )


            fig_ranking.update_yaxes(

                ticksuffix="%",

                tickfont=dict(
                    color=COLORS["text"]
                ),

                gridcolor=
                    "rgba(255,255,255,0.08)"

            )


            st.plotly_chart(

                fig_ranking,

                use_container_width=True,

                config={
                    "displayModeBar": False
                }

            )


        # ====================================================
        # COMPETITIVE + OPERATIONAL ANALYSIS
        # ====================================================

        col_competitive, col_pressure = st.columns(2)


        # ----------------------------------------------------
        # COMPETITIVE RANKING
        # ----------------------------------------------------

        with col_competitive:


            if "Backlog %" in ranking_df.columns:


                competitive_df = (

                    ranking_df

                    .sort_values(

                        "Backlog %",

                        ascending=True

                    )

                )


                fig_competitive = go.Figure()


                fig_competitive.add_trace(

                    go.Bar(

                        x=competitive_df[
                            business_area_column
                        ],

                        y=competitive_df[
                            "Backlog %"
                        ],

                        name="Backlog %",

                        marker_color=COLORS[
                            "red_light"
                        ]

                    )

                )


                fig_competitive.update_layout(

                    title="Competitive Gap Ranking",

                    height=420,

                    paper_bgcolor=COLORS[
                        "background"
                    ],

                    plot_bgcolor=COLORS[
                        "background"
                    ],

                    showlegend=False

                )


                fig_competitive.update_xaxes(

                    tickfont=dict(
                        color=COLORS["text"]
                    ),

                    showgrid=False

                )


                fig_competitive.update_yaxes(

                    ticksuffix="%",

                    tickfont=dict(
                        color=COLORS["text"]
                    ),

                    gridcolor=
                        "rgba(255,255,255,0.08)"

                )


                st.plotly_chart(

                    fig_competitive,

                    use_container_width=True,

                    config={
                        "displayModeBar": False
                    }

                )


        # ----------------------------------------------------
        # OPERATIONAL PRESSURE
        # ----------------------------------------------------

        with col_pressure:


            if "Backlog Units" in ranking_df.columns:


                pressure_df = (

                    ranking_df

                    .sort_values(

                        "Backlog Units",

                        ascending=False

                    )

                )


                fig_pressure = go.Figure()


                fig_pressure.add_trace(

                    go.Bar(

                        x=pressure_df[
                            business_area_column
                        ],

                        y=pressure_df[
                            "Backlog Units"
                        ],

                        name="Backlog Units",

                        marker_color=COLORS[
                            "purple"
                        ]

                    )

                )


                fig_pressure.update_layout(

                    title="Operational Pressure",

                    height=420,

                    paper_bgcolor=COLORS[
                        "background"
                    ],

                    plot_bgcolor=COLORS[
                        "background"
                    ],

                    showlegend=False

                )


                fig_pressure.update_xaxes(

                    tickfont=dict(
                        color=COLORS["text"]
                    ),

                    showgrid=False

                )


                fig_pressure.update_yaxes(

                    tickfont=dict(
                        color=COLORS["text"]
                    ),

                    gridcolor=
                        "rgba(255,255,255,0.08)"

                )


                st.plotly_chart(

                    fig_pressure,

                    use_container_width=True,

                    config={
                        "displayModeBar": False
                    }

                )


# ============================================================
# FOOTER
# ============================================================

st.markdown(

    """
<div class="footer">

<div>
CONFIDENTIAL
</div>

<div>
BMW / MINI · BENCHMARK INTELLIGENCE
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