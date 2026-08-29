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

    "card": "#121820",
    "card_2": "#171E27",

    "border": "#27313D",

    "text": "#F4F6F8",
    "muted": "#87929D",

    "blue": "#1C69D4",
    "blue_light": "#5D9EFF",

    "gold": "#C8A75B",
    "gold_light": "#E2C77B",

    "silver": "#AEB7C2",

    "red": "#D46363",
    "red_light": "#F08A8A",

    "green": "#4FA47A",
    "green_light": "#6FC89B",

    "purple": "#917EE8",

    "cyan": "#4FAFC7"
}


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
<style>


/* ============================================================
   HIDE STREAMLIT ELEMENTS
============================================================ */

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header {{
    visibility: hidden;
}}

[data-testid="stToolbar"] {{
    visibility: hidden;
}}

[data-testid="stDecoration"] {{
    display: none;
}}

[data-testid="stStatusWidget"] {{
    display: none;
}}


/* ============================================================
   GLOBAL
============================================================ */

.stApp {{

    background:

        radial-gradient(
            circle at 85% 0%,
            rgba(28,105,212,0.12),
            transparent 28%
        ),

        radial-gradient(
            circle at 5% 90%,
            rgba(200,167,91,0.08),
            transparent 32%
        ),

        linear-gradient(
            135deg,
            #080B0F,
            #0B0E12,
            #10151C
        );

    color:
        {COLORS["text"]};

}}


.block-container {{

    padding-top:
        2rem;

    padding-bottom:
        3rem;

    max-width:
        1700px;

}}


/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {{

    background:

        linear-gradient(
            180deg,
            #0C1117,
            #111820,
            #080B0F
        );

    border-right:
        1px solid rgba(255,255,255,0.06);

}}


section[data-testid="stSidebar"] > div {{

    padding-top:
        2rem;

}}


.sidebar-brand {{

    font-size:
        9px;

    letter-spacing:
        4px;

    color:
        #6F7B87;

    text-transform:
        uppercase;

    margin-bottom:
        8px;

}}


.sidebar-title {{

    font-size:
        29px;

    font-weight:
        600;

    letter-spacing:
        -1px;

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
            rgba(255,255,255,0.15),
            transparent
        );

    margin:
        24px 0;

}}


section[data-testid="stSidebar"] label {{

    color:
        #C8D0D8 !important;

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
        20px;

}}


.main-title {{

    font-size:
        clamp(40px, 5vw, 68px);

    font-weight:
        650;

    letter-spacing:
        -3px;

    color:
        #F7F9FB;

    line-height:
        1;

}}


.main-title span {{

    color:
        #697581;

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
        30px;

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
        35px;

    background:

        linear-gradient(
            135deg,
            #141B24,
            #10151C
        );

    border:
        1px solid {COLORS["border"]};

    border-radius:
        6px;

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
        #DCE2E8;

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
        0 0 14px rgba(79,164,122,0.9);

}}


.status-right {{

    font-size:
        10px;

    color:
        #75818D;

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
        29px;

    font-weight:
        600;

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
        #84909C;

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
            #151C25,
            #10151C
        );

    border:
        1px solid {COLORS["border"]};

    border-radius:
        7px;

    padding:
        22px;

    min-height:
        135px;

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
        rgba(28,105,212,0.6);

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
        #7E8995;

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
        #77828D;

    margin-top:
        8px;

}}


/* ============================================================
   INSIGHT CARD
============================================================ */

.insight-card {{

    background:
        linear-gradient(
            145deg,
            #141B24,
            #0F141A
        );

    border:
        1px solid #26313D;

    border-left:
        3px solid {COLORS["gold"]};

    border-radius:
        5px;

    padding:
        18px;

    margin-bottom:
        12px;

}}


.insight-title {{

    font-size:
        10px;

    letter-spacing:
        1.5px;

    color:
        {COLORS["gold_light"]};

    margin-bottom:
        8px;

    text-transform:
        uppercase;

}}


.insight-text {{

    font-size:
        12px;

    line-height:
        1.7;

    color:
        #C8D0D8;

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
        5px;

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
# FIND COLUMN
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

        except:

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
# SORT VALUE TO MONTH
# ============================================================

def sort_value_to_month(sort_value):

    year = int(sort_value // 100)

    month = int(sort_value % 100)

    if month > 12 or month < 1:

        return "Forecast"


    return f"{calendar.month_abbr[month]}'{str(year)[-2:]}"


# ============================================================
# GET FUTURE MONTHS
# ============================================================

def get_future_months(last_sort_value, periods=3):

    future_months = []

    year = int(last_sort_value // 100)

    month = int(last_sort_value % 100)


    for _ in range(periods):

        month += 1

        if month > 12:

            month = 1

            year += 1


        future_months.append(
            f"{calendar.month_abbr[month]}'{str(year)[-2:]}"
        )


    return future_months


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


    forecast_periods = st.selectbox(

        "Forecast Period",

        [

            1,
            2,
            3,
            4,
            6

        ],

        index=2

    )


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
# ANALYSIS DATAFRAME
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


def create_forecast(values, periods):

    values = pd.Series(values).dropna()

    if len(values) == 0:

        return []


    if len(values) == 1:

        growth = 0

    else:

        recent_values = values.tail(
            min(3, len(values))
        )

        growth = (

            recent_values.iloc[-1]
            -
            recent_values.iloc[0]

        ) / max(
            len(recent_values) - 1,
            1
        )


    forecast_values = []

    last_value = values.iloc[-1]


    for _ in range(periods):

        last_value = (

            last_value
            +
            growth
        )

        forecast_values.append(
            max(last_value, 0)
        )


    return forecast_values


def calculate_health_score():

    score = 0


    if pd.notna(achieved_avg):

        score += min(
            max(achieved_avg, 0),
            100
        ) * 0.50


    performance_gap = (

        projection_avg
        -
        achieved_avg

        if (
            pd.notna(projection_avg)
            and
            pd.notna(achieved_avg)
        )

        else 0

    )


    gap_score = max(
        0,
        100 - abs(performance_gap)
    )


    score += gap_score * 0.30


    if pd.notna(backlog_percent_avg):

        backlog_score = max(
            0,
            100 - abs(backlog_percent_avg)
        )

        score += backlog_score * 0.20


    return min(
        max(score, 0),
        100
    )


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


performance_gap = (

    projection_avg
    -
    achieved_avg

    if (
        pd.notna(projection_avg)
        and
        pd.notna(achieved_avg)
    )

    else np.nan

)


business_health_score = calculate_health_score()


# ============================================================
# MAIN HEADER
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
High-level business performance and competitor benchmarking.
</div>
        """,

        unsafe_allow_html=True
    )


    # ========================================================
    # KPI SCORECARDS
    # ========================================================

    c1, c2, c3, c4, c5 = st.columns(5)


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
PROJECTION
</div>

<div class="kpi-value">
{format_percent(projection_avg)}
</div>

<div class="kpi-sub">
Competitor performance
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
Gap vs projection
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


    with c5:

        st.markdown(

            f"""
<div class="kpi-card">

<div class="kpi-label">
BUSINESS HEALTH
</div>

<div class="kpi-value">
{business_health_score:.0f}
</div>

<div class="kpi-sub">
Overall performance score / 100
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

                [month_column, "Month Sort"],

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


        fig = go.Figure()


        fig.add_trace(

            go.Scatter(

                x=trend_df[month_column],

                y=trend_df["Achieved"],

                mode="lines+markers",

                name="Achieved",

                line=dict(

                    color=COLORS["blue"],

                    width=4

                ),

                marker=dict(
                    size=9
                )

            )

        )


        fig.add_trace(

            go.Scatter(

                x=trend_df[month_column],

                y=trend_df["Projection"],

                mode="lines+markers",

                name="Projection",

                line=dict(

                    color=COLORS["gold"],

                    width=4

                ),

                marker=dict(
                    size=9
                )

            )

        )


        # ====================================================
        # FUTURE FORECAST
        # ====================================================

        if len(trend_df) >= 2:


            future_months = get_future_months(

                trend_df[
                    "Month Sort"
                ].iloc[-1],

                forecast_periods

            )


            achieved_forecast = create_forecast(

                trend_df["Achieved"],

                forecast_periods

            )


            projection_forecast = create_forecast(

                trend_df["Projection"],

                forecast_periods

            )


            forecast_x = [

                trend_df[
                    month_column
                ].iloc[-1]

            ] + future_months


            forecast_achieved_y = [

                trend_df[
                    "Achieved"
                ].iloc[-1]

            ] + achieved_forecast


            forecast_projection_y = [

                trend_df[
                    "Projection"
                ].iloc[-1]

            ] + projection_forecast


            fig.add_trace(

                go.Scatter(

                    x=forecast_x,

                    y=forecast_achieved_y,

                    mode="lines+markers",

                    name="Achieved Forecast",

                    line=dict(

                        color=COLORS[
                            "blue_light"
                        ],

                        width=3,

                        dash="dash"

                    )

                )

            )


            fig.add_trace(

                go.Scatter(

                    x=forecast_x,

                    y=forecast_projection_y,

                    mode="lines+markers",

                    name="Projection Forecast",

                    line=dict(

                        color=COLORS[
                            "gold_light"
                        ],

                        width=3,

                        dash="dash"

                    )

                )

            )


        fig.update_layout(

            height=500,

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

                b=60

            ),

            legend=dict(

                orientation="h",

                y=1.08,

                x=0.5,

                xanchor="center",

                font=dict(

                    color=COLORS[
                        "text"
                    ],

                    size=12

                )

            )

        )


        fig.update_xaxes(

            title="Month",

            tickfont=dict(
                color=COLORS["text"]
            ),

            showgrid=False

        )


        fig.update_yaxes(

            title="Performance %",

            ticksuffix="%",

            tickfont=dict(
                color=COLORS["text"]
            ),

            gridcolor="rgba(255,255,255,0.08)",

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
    # AUTOMATIC INSIGHTS
    # ========================================================

    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown(

        """
<div class="section-number">
KEY INSIGHTS
</div>

<div class="section-title">
Management Intelligence
</div>
        """,

        unsafe_allow_html=True
    )


    insights = []


    if pd.notna(performance_gap):

        if performance_gap > 5:

            insights.append(
                (
                    "Competitive Risk",
                    f"Current performance is {performance_gap:.1f}% "
                    "behind competitor projection. Immediate recovery "
                    "action may be required."
                )
            )

        else:

            insights.append(
                (
                    "Competitive Position",
                    "Performance is relatively close to competitor "
                    "projection, indicating controlled competitive pressure."
                )
            )


    if pd.notna(backlog_percent_avg):

        insights.append(
            (
                "Backlog Pressure",
                f"Average backlog is currently "
                f"{backlog_percent_avg:.1f}%."
            )
        )


    if target_remaining_sum > 0:

        insights.append(
            (
                "Target Recovery",
                f"{format_number(target_remaining_sum)} units "
                "remain to achieve the current target."
            )
        )


    if business_health_score >= 80:

        health_message = (
            "Overall business health is strong."
        )

    elif business_health_score >= 60:

        health_message = (
            "Overall business health is stable but requires "
            "continued monitoring."
        )

    else:

        health_message = (
            "Overall business health requires management attention."
        )


    insights.append(

        (
            "Business Health",
            health_message
        )

    )


    for insight_title, insight_text in insights:

        st.markdown(

            f"""
<div class="insight-card">

<div class="insight-title">
{insight_title}
</div>

<div class="insight-text">
{insight_text}
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
Performance gap, backlog exposure and competitor pressure analysis.
</div>
        """,

        unsafe_allow_html=True
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(

            "Average Backlog %",

            format_percent(
                backlog_percent_avg
            )

        )


    with c2:

        st.metric(

            "Total Backlog Units",

            format_number(
                backlog_units_sum
            )

        )


    with c3:

        st.metric(

            "Competitor Gap",

            format_percent(
                performance_gap
            )

        )


    with c4:

        risk_level = "LOW"


        if pd.notna(performance_gap):

            if performance_gap > 10:

                risk_level = "HIGH"

            elif performance_gap > 5:

                risk_level = "MEDIUM"


        st.metric(

            "Competitive Risk",

            risk_level

        )


    st.markdown("<br>", unsafe_allow_html=True)


    if month_column:


        gap_df = (

            analysis_df

            .groupby(

                [month_column, "Month Sort"],

                as_index=False

            )

            .agg(

                Backlog_Percent=(

                    "backlog_percent_numeric",

                    "mean"

                ),

                Backlog_Units=(

                    "backlog_units_numeric",

                    "sum"

                )

            )

            .sort_values(
                "Month Sort"
            )

        )


        # ====================================================
        # BACKLOG PERCENT
        # ====================================================

        fig_gap = go.Figure()


        fig_gap.add_trace(

            go.Scatter(

                x=gap_df[month_column],

                y=gap_df[
                    "Backlog_Percent"
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
                    size=9
                )

            )

        )


        if len(gap_df) >= 2:


            future_months = get_future_months(

                gap_df[
                    "Month Sort"
                ].iloc[-1],

                forecast_periods

            )


            forecast_values = create_forecast(

                gap_df[
                    "Backlog_Percent"
                ],

                forecast_periods

            )


            fig_gap.add_trace(

                go.Scatter(

                    x=[

                        gap_df[
                            month_column
                        ].iloc[-1]

                    ] + future_months,

                    y=[

                        gap_df[
                            "Backlog_Percent"
                        ].iloc[-1]

                    ] + forecast_values,

                    mode="lines+markers",

                    name="Backlog Forecast",

                    line=dict(

                        color=COLORS[
                            "purple"
                        ],

                        width=3,

                        dash="dash"

                    )

                )

            )


        fig_gap.update_layout(

            height=450,

            paper_bgcolor=COLORS[
                "background"
            ],

            plot_bgcolor=COLORS[
                "background"
            ],

            hovermode="x unified",

            legend=dict(

                orientation="h",

                y=1.08,

                x=0.5,

                xanchor="center",

                font=dict(

                    color=COLORS[
                        "text"
                    ],

                    size=12

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

            gridcolor="rgba(255,255,255,0.08)"

        )


        st.plotly_chart(

            fig_gap,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

        )


        # ====================================================
        # BACKLOG UNITS TREND
        # ====================================================

        fig_units = go.Figure()


        fig_units.add_trace(

            go.Bar(

                x=gap_df[month_column],

                y=gap_df[
                    "Backlog_Units"
                ],

                name="Backlog Units",

                marker_color=COLORS[
                    "cyan"
                ]

            )

        )


        fig_units.update_layout(

            height=420,

            paper_bgcolor=COLORS[
                "background"
            ],

            plot_bgcolor=COLORS[
                "background"
            ],

            showlegend=False

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

            gridcolor="rgba(255,255,255,0.08)"

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

                [month_column, "Month Sort"],

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


        # ====================================================
        # FORECAST
        # ====================================================

        if len(actual_target_df) >= 2:


            future_months = get_future_months(

                actual_target_df[
                    "Month Sort"
                ].iloc[-1],

                forecast_periods

            )


            actual_forecast = create_forecast(

                actual_target_df[
                    "Actual"
                ],

                forecast_periods

            )


            target_forecast = create_forecast(

                actual_target_df[
                    "Target"
                ],

                forecast_periods

            )


            forecast_x = [

                actual_target_df[
                    month_column
                ].iloc[-1]

            ] + future_months


            fig_actual_target.add_trace(

                go.Scatter(

                    x=forecast_x,

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

                    x=forecast_x,

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

                y=1.08,

                x=0.5,

                xanchor="center",

                font=dict(

                    color=COLORS[
                        "text"
                    ],

                    size=12

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

            gridcolor="rgba(255,255,255,0.08)",

            zeroline=False

        )


        st.plotly_chart(

            fig_actual_target,

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
Comparison of business areas across performance,
competitive positioning and operational pressure.
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


        if month_column and selected_months:

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

        for key in [

            "achieved",
            "projection",
            "backlog_percent"

        ]:

            column = detected_columns[key]

            if column:

                comparison_df[
                    f"{key}_numeric"
                ] = convert_percentage(
                    comparison_df[column]
                )


        for key in [

            "backlog_units",
            "backlog_per_day",
            "target_per_day"

        ]:

            column = detected_columns[key]

            if column:

                comparison_df[
                    f"{key}_numeric"
                ] = safe_numeric(
                    comparison_df[column]
                )


        # ====================================================
        # RANKING DATA
        # ====================================================

        aggregation_dict = {}


        if "achieved_numeric" in comparison_df.columns:

            aggregation_dict[
                "Achieved"
            ] = (
                "achieved_numeric",
                "mean"
            )


        if "projection_numeric" in comparison_df.columns:

            aggregation_dict[
                "Projection"
            ] = (
                "projection_numeric",
                "mean"
            )


        if "backlog_percent_numeric" in comparison_df.columns:

            aggregation_dict[
                "Backlog %"
            ] = (
                "backlog_percent_numeric",
                "mean"
            )


        if "backlog_units_numeric" in comparison_df.columns:

            aggregation_dict[
                "Backlog Units"
            ] = (
                "backlog_units_numeric",
                "sum"
            )


        if "backlog_per_day_numeric" in comparison_df.columns:

            aggregation_dict[
                "Daily Pressure"
            ] = (
                "backlog_per_day_numeric",
                "mean"
            )


        ranking_df = (

            comparison_df

            .groupby(

                business_area_column,

                as_index=False

            )

            .agg(
                **aggregation_dict
            )

        )


        if "Achieved" in ranking_df.columns:

            ranking_df = ranking_df.sort_values(

                "Achieved",

                ascending=False

            )


        # ====================================================
        # PERFORMANCE RANKING
        # ====================================================

        if (

            "Achieved" in ranking_df.columns
            and
            "Projection" in ranking_df.columns

        ):


            fig_ranking = go.Figure()


            fig_ranking.add_trace(

                go.Bar(

                    x=ranking_df[
                        business_area_column
                    ],

                    y=ranking_df[
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

                    x=ranking_df[
                        business_area_column
                    ],

                    y=ranking_df[
                        "Projection"
                    ],

                    name="Projection",

                    marker_color=COLORS[
                        "gold"
                    ]

                )

            )


            fig_ranking.update_layout(

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

                        size=12

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

                gridcolor="rgba(255,255,255,0.08)"

            )


            st.plotly_chart(

                fig_ranking,

                use_container_width=True,

                config={
                    "displayModeBar": False
                }

            )


        # ====================================================
        # RANKING SCORECARDS
        # ====================================================

        st.markdown("<br>", unsafe_allow_html=True)


        st.markdown(

            """
<div class="section-number">
BUSINESS AREA LEADERS
</div>

<div class="section-title">
Performance Ranking
</div>
            """,

            unsafe_allow_html=True
        )


        if "Achieved" in ranking_df.columns:


            top_areas = ranking_df.head(3)


            columns = st.columns(
                min(3, len(top_areas))
            )


            for index, (_, row) in enumerate(
                top_areas.iterrows()
            ):


                with columns[index]:

                    area_name = row[
                        business_area_column
                    ]


                    achieved_value = row[
                        "Achieved"
                    ]


                    projection_value = (

                        row["Projection"]

                        if "Projection"
                        in row.index

                        else np.nan

                    )


                    st.markdown(

                        f"""
<div class="kpi-card">

<div class="kpi-label">
#{index + 1} RANK
</div>

<div class="kpi-value">
{area_name}
</div>

<div class="kpi-sub">

Achieved:
{format_percent(achieved_value)}

&nbsp; | &nbsp;

Projection:
{format_percent(projection_value)}

</div>

</div>
                        """,

                        unsafe_allow_html=True
                    )


        # ====================================================
        # OPERATIONAL PRESSURE HEATMAP
        # ====================================================

        if (

            "Backlog %" in ranking_df.columns
            and
            "Daily Pressure" in ranking_df.columns

        ):


            st.markdown("<br>", unsafe_allow_html=True)


            st.markdown(

                """
<div class="section-number">
OPERATIONAL PRESSURE
</div>

<div class="section-title">
Business Area Heatmap
</div>
                """,

                unsafe_allow_html=True
            )


            heatmap_values = np.array(

                [

                    ranking_df[
                        "Backlog %"
                    ].fillna(0).values,

                    ranking_df[
                        "Daily Pressure"
                    ].fillna(0).values

                ]

            )


            fig_heatmap = go.Figure(

                data=

                go.Heatmap(

                    z=heatmap_values,

                    x=ranking_df[
                        business_area_column
                    ],

                    y=[

                        "Backlog %",
                        "Daily Pressure"

                    ],

                    colorscale=[

                        [0, "#163A2A"],
                        [0.4, "#4F9D7A"],
                        [0.65, "#C8A75B"],
                        [1, "#C95C5C"]

                    ],

                    text=np.round(
                        heatmap_values,
                        1
                    ),

                    texttemplate="%{text}",

                    hovertemplate=(

                        "<b>%{x}</b>"

                        "<br>%{y}: %{z:.1f}"

                        "<extra></extra>"

                    )

                )

            )


            fig_heatmap.update_layout(

                height=350,

                paper_bgcolor=COLORS[
                    "background"
                ],

                plot_bgcolor=COLORS[
                    "background"
                ],

                margin=dict(

                    l=100,

                    r=30,

                    t=30,

                    b=80

                )

            )


            fig_heatmap.update_xaxes(

                tickfont=dict(
                    color=COLORS["text"]
                )

            )


            fig_heatmap.update_yaxes(

                tickfont=dict(
                    color=COLORS["text"]
                )

            )


            st.plotly_chart(

                fig_heatmap,

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
