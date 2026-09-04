import streamlit as st
import pandas as pd
import requests
import time
import re
import calendar
import numpy as np
import plotly.graph_objects as go

from io import StringIO
from datetime import datetime, date


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
    "excess": "Excess",
    "target_remaining": "Target need to achive",
    "backlog_per_day": "Backlog Units ( Per day )",
    "target_per_day": "Target need to achive ( per day )",
    "daily_target": "Daily total Target"
}


# ============================================================
# LUXURY COLOR PALETTE
# ============================================================

COLORS = {

    "background": "#0B0E12",
    "card": "#121820",
    "card_2": "#171E27",
    "border": "#27313D",

    "text": "#F4F6F8",
    "muted": "#8C98A5",

    "blue": "#1C69D4",
    "blue_light": "#5D9EFF",

    "gold": "#C8A75B",
    "gold_light": "#E2C77B",

    "silver": "#AEB7C2",

    "red": "#C95C5C",
    "red_light": "#E07A7A",

    "green": "#4F9D7A",
    "green_light": "#6CC59B",

    "purple": "#8C7AE6"
}


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
<style>

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
            rgba(200,167,91,0.07),
            transparent 30%
        ),

        linear-gradient(
            135deg,
            #080B0F,
            #0B0E12,
            #10151C
        );

    color: {COLORS["text"]};

}}


.block-container {{

    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1650px;

}}


/* ============================================================
   STREAMLIT HEADER
============================================================ */

[data-testid="stHeader"] {{

    background: transparent !important;

}}


#MainMenu {{

    visibility: hidden;

}}


footer {{

    visibility: hidden;

}}


/* ============================================================
   SIDEBAR COLLAPSE CONTROL
============================================================ */

button[data-testid="stSidebarCollapsedControl"] {{

    position: fixed !important;

    top: 18px !important;
    left: 18px !important;

    width: 44px !important;
    height: 44px !important;

    display: flex !important;

    align-items: center !important;
    justify-content: center !important;

    background:
        linear-gradient(
            135deg,
            #1C69D4,
            #123E7A
        ) !important;

    border:
        1px solid #5D9EFF !important;

    border-radius:
        9px !important;

    color:
        #FFFFFF !important;

    z-index:
        999999 !important;

    box-shadow:
        0 6px 24px rgba(28,105,212,0.60) !important;

}}


button[data-testid="stSidebarCollapsedControl"] svg {{

    fill: #FFFFFF !important;
    color: #FFFFFF !important;
    stroke: #FFFFFF !important;

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

    padding-top: 2rem;

}}


.sidebar-brand {{

    font-size: 9px;

    letter-spacing: 4px;

    color: #6F7B87;

    text-transform: uppercase;

    margin-bottom: 8px;

}}


.sidebar-title {{

    font-size: 29px;

    font-weight: 600;

    letter-spacing: -1px;

    line-height: 1.05;

    color: #FFFFFF;

    margin-bottom: 28px;

}}


.sidebar-divider {{

    height: 1px;

    background:

        linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.15),
            transparent
        );

    margin: 24px 0;

}}


section[data-testid="stSidebar"] label {{

    color: #C8D0D8 !important;

    font-size: 11px !important;

    letter-spacing: 0.8px;

}}


/* ============================================================
   HEADER
============================================================ */

.top-label {{

    display: inline-block;

    font-size: 9px;

    letter-spacing: 4px;

    color: {COLORS["blue_light"]};

    text-transform: uppercase;

    border-bottom:
        2px solid {COLORS["blue"]};

    padding-bottom: 8px;

    margin-bottom: 20px;

}}


.main-title {{

    font-size:
        clamp(40px, 5vw, 68px);

    font-weight: 650;

    letter-spacing: -3px;

    color: #F7F9FB;

    line-height: 1;

}}


.main-title span {{

    color: #697581;

    font-weight: 300;

}}


.subtitle {{

    font-size: 14px;

    color: #87929D;

    max-width: 850px;

    line-height: 1.8;

    margin-top: 16px;

    margin-bottom: 30px;

}}


/* ============================================================
   STATUS CARD
============================================================ */

.status-card {{

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 16px 20px;

    margin-bottom: 35px;

    background:

        linear-gradient(
            135deg,
            #141B24,
            #10151C
        );

    border:
        1px solid {COLORS["border"]};

    border-radius: 6px;

}}


.status-left {{

    display: flex;

    align-items: center;

    font-size: 10px;

    letter-spacing: 2px;

    color: #DCE2E8;

}}


.live-dot {{

    width: 9px;

    height: 9px;

    border-radius: 50%;

    background: {COLORS["blue"]};

    margin-right: 10px;

    box-shadow:
        0 0 14px rgba(28,105,212,0.9);

}}


.status-right {{

    font-size: 10px;

    color: #75818D;

    letter-spacing: 1px;

}}


/* ============================================================
   SECTION
============================================================ */

.section-number {{

    font-size: 9px;

    color: {COLORS["blue_light"]};

    letter-spacing: 3px;

    font-weight: 700;

    margin-bottom: 8px;

}}


.section-title {{

    font-size: 29px;

    font-weight: 600;

    color: #F5F7F9;

    letter-spacing: -1px;

    margin-bottom: 6px;

}}


.section-description {{

    font-size: 12px;

    color: #84909C;

    margin-bottom: 25px;

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

    border-radius: 7px;

    padding: 22px;

    min-height: 135px;

    position: relative;

    overflow: hidden;

    transition: 0.25s;

}}


/* ============================================================
   STANDARD SCORECARD SIZE
============================================================ */

.scorecard {{

    height: 135px;

    min-height: 135px;

    max-height: 135px;

    box-sizing: border-box;

    display: flex;

    flex-direction: column;

    justify-content: flex-start;

}}


.kpi-card:hover {{

    transform:
        translateY(-4px);

    border-color:
        rgba(28,105,212,0.6);

}}


.kpi-card::before {{

    content: "";

    position: absolute;

    top: 0;

    left: 0;

    width: 100%;

    height: 3px;

    background:

        linear-gradient(
            90deg,
            {COLORS["blue"]},
            {COLORS["blue_light"]},
            {COLORS["gold"]}
        );

}}


.kpi-label {{

    font-size: 9px;

    letter-spacing: 2px;

    text-transform: uppercase;

    color: #7E8995;

    margin-bottom: 15px;

}}


.scorecard .kpi-label {{

    min-height: 11px;

}}


.kpi-value {{

    font-size: 30px;

    font-weight: 650;

    color: #F6F8FA;

    letter-spacing: -1px;

}}


.scorecard .kpi-value {{

    line-height: 1.15;

    min-height: 35px;

    display: flex;

    align-items: center;

}}


.kpi-sub {{

    font-size: 10px;

    color: #77828D;

    margin-top: 8px;

}}


.scorecard .kpi-sub {{

    line-height: 1.3;

    min-height: 13px;

}}


/* ============================================================
   NEW UNIT SCORECARD
============================================================ */

.unit-scorecard .kpi-value {{

    color: #F6F8FA;

}}


/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {{

    width: 100%;

    background:

        linear-gradient(
            135deg,
            #182331,
            #101820
        );

    color: #FFFFFF;

    border:
        1px solid #2A3745;

    border-radius: 5px;

    font-size: 10px;

    letter-spacing: 1.5px;

    text-transform: uppercase;

}}


/* ============================================================
   FOOTER
============================================================ */

.footer {{

    margin-top: 70px;

    padding-top: 25px;

    border-top:
        1px solid #222B35;

    display: flex;

    justify-content: space-between;

    color: #65707B;

    font-size: 9px;

    letter-spacing: 1.5px;

}}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# NORMALIZE COLUMN NAME
# ============================================================

def normalize_column_name(column_name):

    column_name = str(column_name).strip()

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

    target = normalize_column_name(target_column)

    for column in dataframe.columns:

        if normalize_column_name(column) == target:

            return column

    return None


# ============================================================
# SAFE NUMERIC CONVERSION
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
# PERCENTAGE CONVERSION
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
# MONTH SORT FUNCTION
# ============================================================

def get_month_sort_value(month_value):

    if pd.isna(month_value):

        return 999999

    month_text = str(month_value).strip()

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
                + dt.month
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

                year_value = datetime.now().year


            return (
                year_value * 100
                + month_number
            )


    return 999999


# ============================================================
# DAYS REMAINING IN CURRENT MONTH
# ============================================================

def get_days_remaining_in_month():

    today = date.today()

    last_day = calendar.monthrange(
        today.year,
        today.month
    )[1]

    return last_day - today.day


# ============================================================
# LOAD DATA
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

                "Cache-Control": "no-cache",
                "Pragma": "no-cache"

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
            "02  Target Recovery",
            "03  Business Area Comparison",
            "04  Target & Achievement Intelligence",
            "05  Backlog & Excess Intelligence",
            "06  Business Area Intelligence",
            "07  Monthly Trend Intelligence"

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


    month_filter_df = df.copy()


    if (
        business_area_column
        and selected_business_area != "All"
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
    and selected_business_area != "All"
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
    and selected_months
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
# ANALYSIS DATA
# ============================================================

analysis_df = filtered_df.copy()


for key in [

    "input_1",
    "input_2",
    "backlog_units",
    "excess",
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

days_remaining = get_days_remaining_in_month()


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

&nbsp;&nbsp; | &nbsp;&nbsp;

DAYS REMAINING: {days_remaining}

</div>

</div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_average(column_name):

    if column_name not in analysis_df.columns:

        return np.nan

    values = analysis_df[
        column_name
    ]

    values = values[
        values.notna()
        & (values != 0)
    ]

    if values.empty:

        return np.nan

    return values.mean()


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


def status_html(label, value, color):

    return f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
{label}
</div>

<div class="kpi-value"
style="color:{color};">
{value}
</div>

</div>
"""


def create_status_message(
    condition,
    positive_text,
    negative_text,
    neutral_text=None
):

    if condition is True:

        return positive_text

    if condition is False:

        return negative_text

    return neutral_text or "Insufficient data to determine status."


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

excess_sum = calculate_sum(
    "excess_numeric"
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

target_per_day_avg = calculate_average(
    "target_per_day_numeric"
)

daily_target_avg = calculate_average(
    "daily_target_numeric"
)

backlog_per_day_avg = calculate_average(
    "backlog_per_day_numeric"
)


# ============================================================
# PROJECTED UNITS
#
# TOTAL INPUT 1 × PROJECTION % ÷ 100
# ============================================================

if (
    pd.notna(projection_avg)
    and input_1_sum != 0
):

    projected_units = (

        input_1_sum
        *
        projection_avg
        /
        100

    )

else:

    projected_units = np.nan


# ============================================================
# PAGE 1 — SCORECARD 3
#
# ABSOLUTE DIFFERENCE BETWEEN:
# ACHIEVED AND PROJECTION
# ============================================================

if (
    pd.notna(achieved_avg)
    and pd.notna(projection_avg)
):

    performance_gap_value = abs(

        achieved_avg
        -
        projection_avg

    )

else:

    performance_gap_value = np.nan


# ============================================================
# PAGE 1 — SCORECARD 4
#
# TOTAL INPUT 1
# ×
# (PERFORMANCE GAP / 100)
# ============================================================

if pd.notna(performance_gap_value):

    scorecard_4_value = round(

        input_1_sum
        *
        (
            performance_gap_value
            /
            100
        )

    )

else:

    scorecard_4_value = np.nan


# ============================================================
# PAGE 1 — SCORECARD 5
#
# SCORECARD 4
# ÷
# REMAINING DAYS
# ============================================================

if (
    pd.notna(scorecard_4_value)
    and days_remaining > 0
):

    scorecard_5_value = round(

        scorecard_4_value
        /
        days_remaining

    )

else:

    scorecard_5_value = np.nan


# ============================================================
# ADDITIONAL INTELLIGENCE CALCULATIONS
# ============================================================

if input_2_sum != 0:

    target_achievement_pct = (
        input_1_sum
        /
        input_2_sum
    ) * 100

else:

    target_achievement_pct = np.nan


target_gap_units = (
    input_2_sum
    -
    input_1_sum
)


if input_2_sum != 0:

    target_gap_pct = (
        target_gap_units
        /
        input_2_sum
    ) * 100

else:

    target_gap_pct = np.nan


# ============================================================
# PAGE 1 — SCORECARD 7 VALUE
#
# MOVED FROM PAGE 4 SCORECARD 4
#
# CALCULATION:
# (INPUT 1 × PERFORMANCE GAP) + INPUT 1
# ============================================================

if pd.notna(performance_gap_value):

    page1_scorecard_7_value = round(

        (
            input_1_sum
            *
            (performance_gap_value / 100)
        )
        +
        input_1_sum

    )

else:

    page1_scorecard_7_value = np.nan


# ============================================================
# PROJECTED TARGET GAP
# ============================================================

if pd.notna(projected_units):

    projected_target_gap_units = (
        projected_units
        -
        input_2_sum
    )

else:

    projected_target_gap_units = np.nan


if backlog_units_sum > 0:

    excess_coverage_pct = (
        excess_sum
        /
        backlog_units_sum
    ) * 100

else:

    excess_coverage_pct = np.nan


net_backlog_after_excess = (
    backlog_units_sum
    -
    excess_sum
)


# ============================================================
# PAGE 01 — EXECUTIVE OVERVIEW
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
    # SCORECARDS 1–5 — ORIGINAL EXECUTIVE SCORECARDS
    # ========================================================

    c1, c2, c3, c4, c5 = st.columns(5)


    with c1:

        st.markdown(
            f"""
<div class="kpi-card scorecard">

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
<div class="kpi-card scorecard">

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
<div class="kpi-card scorecard">

<div class="kpi-label">
PERFORMANCE GAP
</div>

<div class="kpi-value">
{format_percent(performance_gap_value)}
</div>

<div class="kpi-sub">
(Achieved - Projection)
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    with c4:

        st.markdown(
            f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
PERFORMANCE GAP UNITS
</div>

<div class="kpi-value">
{format_number(scorecard_4_value)}
</div>

<div class="kpi-sub">
Total Input 1 × Performance Gap %
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    with c5:

        st.markdown(
            f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
DAILY GAP UNITS
</div>

<div class="kpi-value">
{format_number(scorecard_5_value)}
</div>

<div class="kpi-sub">
Gap Units ÷ Remaining Days
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # ========================================================
    # SCORECARD 6–7 — UNIT POSITION
    # ========================================================

    st.markdown(
        """
<div class="section-number">
UNIT POSITION
</div>

<div class="section-title">
Actual vs Projection Units
</div>

<div class="section-description">
Total achieved input compared with the units indicated by the current projection.
</div>
        """,
        unsafe_allow_html=True
    )


    u1, u2 = st.columns(2)


    # ========================================================
    # SCORECARD 6 — TOTAL INPUT 1
    # ========================================================

    with u1:

        st.markdown(
            f"""
<div class="kpi-card scorecard unit-scorecard">

<div class="kpi-label">
TOTAL INPUT 1
</div>

<div class="kpi-value">
{format_number(input_1_sum)}
</div>

<div class="kpi-sub">
Total current achieved units
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # SCORECARD 7 — MOVED FROM PAGE 4 SCORECARD 4
    # ========================================================

    with u2:

        st.markdown(
            f"""
<div class="kpi-card scorecard unit-scorecard">

<div class="kpi-label">
PROJECTED UNITS
</div>

<div class="kpi-value">
{format_number(page1_scorecard_7_value)}
</div>

<div class="kpi-sub">
(Input 1 × Performance Gap %) + Input 1
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # ========================================================
    # NEW HORIZONTAL BAR CHART
    #
    # TOTAL INPUT 1
    # VS
    # PROJECTION UNITS
    # ========================================================

    st.markdown(
        """
<div class="section-number">
UNIT COMPARISON
</div>

<div class="section-title">
Total Input 1 vs Projection Units
</div>

<div class="section-description">
Horizontal comparison of current achieved units against projected units.
</div>
        """,
        unsafe_allow_html=True
    )


    if (
        pd.notna(input_1_sum)
        and pd.notna(page1_scorecard_7_value)
    ):

        unit_chart_df = pd.DataFrame({

            "Metric": [
                "Total Input 1",
                "Projection Units"
            ],

            "Units": [
                input_1_sum,
                page1_scorecard_7_value
            ]

        })


        fig_unit_comparison = go.Figure()


        # ----------------------------------------------------
        # TOTAL INPUT 1
        # ----------------------------------------------------

        fig_unit_comparison.add_trace(

            go.Bar(

                y=unit_chart_df[
                    "Metric"
                ],

                x=unit_chart_df[
                    "Units"
                ],

                orientation="h",

                name="Units",

                marker_color=[
                    COLORS["blue"],
                    COLORS["gold"]
                ],

                text=[
                    format_number(input_1_sum),
                    format_number(page1_scorecard_7_value)
                ],

                textposition="outside",

                hovertemplate=
                    "<b>%{y}</b><br>"
                    "Units: %{x:,.0f}"
                    "<extra></extra>"

            )

        )


        fig_unit_comparison.update_layout(

            height=300,

            paper_bgcolor=COLORS[
                "background"
            ],

            plot_bgcolor=COLORS[
                "background"
            ],

            showlegend=False,

            margin=dict(

                l=30,

                r=100,

                t=25,

                b=40

            )

        )


        fig_unit_comparison.update_xaxes(

            title="Units",

            tickfont=dict(
                color=COLORS["text"]
            ),

            title_font=dict(
                color=COLORS["muted"]
            ),

            gridcolor="rgba(255,255,255,0.08)",

            zeroline=False

        )


        fig_unit_comparison.update_yaxes(

            tickfont=dict(
                color=COLORS["text"],
                size=13
            ),

            showgrid=False

        )


        st.plotly_chart(

            fig_unit_comparison,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

        )

    else:

        st.info(
            "Insufficient data available to create the unit comparison chart."
        )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # ========================================================
    # EXISTING MONTHLY PERFORMANCE TREND
    # ========================================================

    if selected_business_area == "All":

        st.info(
            "Please select a Business Area to view the monthly performance trend."
        )


    elif (
        month_column
        and "achieved_numeric" in analysis_df.columns
        and "projection_numeric" in analysis_df.columns
    ):

        st.markdown(
            """
<div class="section-number">
MONTHLY PERFORMANCE
</div>

<div class="section-title">
Achieved vs Projection Trend
</div>

<div class="section-description">
Monthly movement of achieved performance against competitor projection.
</div>
            """,
            unsafe_allow_html=True
        )


        trend_df = (

            analysis_df

            .groupby(
                [month_column, "Month Sort"],
                as_index=False
            )

            .agg(

                Achieved=(

                    "achieved_numeric",

                    lambda x:
                    x[x != 0].mean()
                    if (x != 0).any()
                    else np.nan

                ),

                Projection=(

                    "projection_numeric",

                    lambda x:
                    x[x != 0].mean()
                    if (x != 0).any()
                    else np.nan

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


        fig.update_layout(

            height=480,

            paper_bgcolor=COLORS["background"],

            plot_bgcolor=COLORS["background"],

            hovermode="x unified",

            legend=dict(

                orientation="h",

                yanchor="bottom",

                y=1.05,

                xanchor="center",

                x=0.5,

                font=dict(
                    color=COLORS["text"],
                    size=13
                )

            ),

            margin=dict(
                l=20,
                r=20,
                t=80,
                b=60
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


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # ========================================================
    # EXECUTIVE INSIGHTS
    # ========================================================

    st.markdown(
        """
<div class="section-number">
KEY INSIGHTS
</div>

<div class="section-title">
Executive Interpretation
</div>
        """,
        unsafe_allow_html=True
    )


    insights = []


    if (
        pd.notna(achieved_avg)
        and pd.notna(projection_avg)
    ):

        if achieved_avg >= projection_avg:

            insights.append(
                f"Performance is currently ahead of competitor projection by "
                f"{performance_gap_value:.1f}%."
            )

        else:

            insights.append(
                f"Performance remains behind competitor projection by "
                f"{performance_gap_value:.1f}%."
            )


    # NEW INSIGHT — INPUT 1 VS PROJECTED UNITS

    if (
        pd.notna(input_1_sum)
        and pd.notna(projected_units)
    ):

        unit_difference = (
            input_1_sum
            -
            projected_units
        )


        if unit_difference > 0:

            insights.append(
                f"Total Input 1 is currently "
                f"{format_number(unit_difference)} units above "
                f"the calculated projection."
            )

        elif unit_difference < 0:

            insights.append(
                f"Total Input 1 is currently "
                f"{format_number(abs(unit_difference))} units below "
                f"the calculated projection."
            )

        else:

            insights.append(
                "Total Input 1 is currently aligned with the calculated projection."
            )


    if pd.notna(scorecard_4_value):

        insights.append(
            f"Based on Total Input 1 and the Performance Gap, "
            f"approximately {format_number(scorecard_4_value)} units "
            f"represent the current performance gap."
        )


    if pd.notna(scorecard_5_value):

        insights.append(
            f"To close the performance gap within the remaining "
            f"{days_remaining} day(s), approximately "
            f"{format_number(scorecard_5_value)} gap units per day "
            f"would be required."
        )


    if target_remaining_sum > 0:

        insights.append(
            f"{format_number(target_remaining_sum)} units remain "
            f"to achieve the current target."
        )


    insights.append(
        f"There are {days_remaining} day(s) remaining "
        f"to complete the current month."
    )


    for index, insight in enumerate(
        insights,
        start=1
    ):

        st.markdown(
            f"""
<div class="kpi-card"
style="
min-height:80px;
margin-bottom:12px;
">

<div class="kpi-label">
INSIGHT {index:02d}
</div>

<div style="
font-size:14px;
color:#DCE2E8;
line-height:1.7;
">

{insight}

</div>

</div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PAGE 02 — TARGET RECOVERY
# ============================================================

elif page == "02  Target Recovery":

    st.markdown(
        """
<div class="section-number">
02 / TARGET RECOVERY
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


    c1, c2, c3, c4, c5 = st.columns(5)


    with c1:

        st.markdown(
            f"""
<div class="kpi-card scorecard">

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
<div class="kpi-card scorecard">

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
<div class="kpi-card scorecard">

<div class="kpi-label">
REMAINING
</div>

<div class="kpi-value">
{format_number(input_1_sum - input_2_sum)}
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
<div class="kpi-card scorecard">

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


    with c5:

        st.markdown(
            f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
DAYS REMAINING
</div>

<div class="kpi-value">
{days_remaining}
</div>

<div class="kpi-sub">
Days left in current month
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    if selected_business_area == "All":

        st.info(
            "Please select a Business Area to view the Actual vs Target trend."
        )


    elif (
        month_column
        and "input_1_numeric" in analysis_df.columns
        and "input_2_numeric" in analysis_df.columns
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
                    color=COLORS["blue"],
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
                    color=COLORS["gold"],
                    width=4
                ),

                marker=dict(
                    size=9
                )

            )

        )


        fig_actual_target.update_layout(

            height=500,

            paper_bgcolor=COLORS[
                "background"
            ],

            plot_bgcolor=COLORS[
                "background"
            ],

            hovermode="x unified"

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
# PAGE 03 — BUSINESS AREA COMPARISON
# ============================================================

elif page == "03  Business Area Comparison":

    st.markdown(
        """
<div class="section-number">
03 / BUSINESS AREA COMPARISON
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


    c1, c2 = st.columns([3, 1])


    with c2:

        st.markdown(
            f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
DAYS REMAINING
</div>

<div class="kpi-value">
{days_remaining}
</div>

<div class="kpi-sub">
Days left in current month
</div>

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


        ranking_df = (

            comparison_df

            .groupby(
                business_area_column,
                as_index=False
            )

            .agg(

                Achieved=(

                    "Achieved Numeric",

                    lambda x:
                    x[x != 0].mean()
                    if (x != 0).any()
                    else np.nan

                ),

                Projection=(

                    "Projection Numeric",

                    lambda x:
                    x[x != 0].mean()
                    if (x != 0).any()
                    else np.nan

                )

            )

        )


        ranking_df[
            "Performance Gap"
        ] = abs(

            ranking_df[
                "Achieved"
            ]

            -

            ranking_df[
                "Projection"
            ]

        )


        ranking_df = ranking_df.sort_values(

            "Achieved",

            ascending=False

        )


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

            gridcolor="rgba(255,255,255,0.08)"

        )


        st.plotly_chart(

            fig_ranking,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

        )


        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        display_ranking_df = ranking_df.copy()


        display_ranking_df[
            "Achieved"
        ] = display_ranking_df[
            "Achieved"
        ].apply(
            format_percent
        )


        display_ranking_df[
            "Projection"
        ] = display_ranking_df[
            "Projection"
        ].apply(
            format_percent
        )


        display_ranking_df[
            "Performance Gap"
        ] = display_ranking_df[
            "Performance Gap"
        ].apply(
            format_percent
        )


        st.dataframe(

            display_ranking_df,

            use_container_width=True,

            hide_index=True

        )


# ============================================================
# PAGE 04 — TARGET & ACHIEVEMENT INTELLIGENCE
# ============================================================

elif page == "04  Target & Achievement Intelligence":

    st.markdown(
        """
<div class="section-number">
04 / TARGET & ACHIEVEMENT INTELLIGENCE
</div>

<div class="section-title">
Target Position
</div>

<div class="section-description">
Understand current achievement, target exposure and expected closing position.
</div>
        """,
        unsafe_allow_html=True
    )


    c1, c2, c3, c4, c5 = st.columns(5)


    with c1:

        st.markdown(
            status_html(
                "TARGET ACHIEVEMENT",
                format_percent(target_achievement_pct),
                COLORS["green"]
                if pd.notna(target_achievement_pct)
                and target_achievement_pct >= 100
                else COLORS["gold"]
            ),
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
TARGET GAP
</div>

<div class="kpi-value">
{format_number(abs(target_gap_units))}
</div>

<div class="kpi-sub">
{"Surplus" if target_gap_units < 0 else "Units still required"}
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
TARGET GAP %
</div>

<div class="kpi-value">
{format_percent(abs(target_gap_pct))}
</div>

<div class="kpi-sub">
Distance from target
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    # SCORECARD 4 REMOVED FROM PAGE 4

    # Page 4 now contains four scorecards.
    # The former Page 4 Scorecard 4 has been moved to Page 1 Scorecard 7.


    with c5:

        projection_status = (
            "ABOVE TARGET"
            if pd.notna(projection_avg)
            and projection_avg >= 100
            else "BELOW TARGET"
        )

        projection_color = (
            COLORS["green"]
            if projection_status == "ABOVE TARGET"
            else COLORS["red"]
        )

        st.markdown(
            f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
TARGET POSITION
</div>

<div class="kpi-value"
style="color:{projection_color};font-size:22px;">
{projection_status}
</div>

<div class="kpi-sub">
Projection: {format_percent(projection_avg)}
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown(
        """
<div class="section-number">
TARGET DIAGNOSTIC
</div>

<div class="section-title">
What the numbers indicate
</div>
        """,
        unsafe_allow_html=True
    )


    target_insights = []


    if pd.notna(target_achievement_pct):

        if target_achievement_pct >= 100:

            target_insights.append(
                f"Current achievement has reached {target_achievement_pct:.1f}% of target. "
                f"The business is currently at or above the required target level."
            )

        else:

            target_insights.append(
                f"Current achievement is {target_achievement_pct:.1f}% of target, "
                f"leaving {format_number(abs(target_gap_units))} units to close."
            )


    if pd.notna(projected_units):

        if projected_units >= input_2_sum:

            target_insights.append(
                f"Based on the current projection level, approximately "
                f"{format_number(projected_units)} units are indicated against "
                f"a target of {format_number(input_2_sum)} units."
            )

        else:

            target_insights.append(
                f"At the current projection level, projected output is approximately "
                f"{format_number(abs(projected_target_gap_units))} units below target."
            )


    if target_remaining_sum > 0:

        target_insights.append(
            f"{format_number(target_remaining_sum)} units remain in the current "
            f"target-recovery position."
        )


    for index, insight in enumerate(
        target_insights,
        start=1
    ):

        st.markdown(
            f"""
<div class="kpi-card"
style="min-height:80px;margin-bottom:12px;">

<div class="kpi-label">
TARGET INSIGHT {index:02d}
</div>

<div style="
font-size:14px;
color:#DCE2E8;
line-height:1.7;
">
{insight}
</div>

</div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PAGE 05 — BACKLOG & EXCESS INTELLIGENCE
# ============================================================

elif page == "05  Backlog & Excess Intelligence":

    st.markdown(
        """
<div class="section-number">
05 / BACKLOG & EXCESS INTELLIGENCE
</div>

<div class="section-title">
Backlog Pressure
</div>

<div class="section-description">
Measure operational backlog, available excess and the net exposure after excess.
</div>
        """,
        unsafe_allow_html=True
    )


    c1, c2, c3, c4, c5 = st.columns(5)


    with c1:

        st.markdown(
            f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
PERFORMANCE GAP UNITS
</div>

<div class="kpi-value">
{format_number(scorecard_4_value)}
</div>

<div class="kpi-sub">
Backlog Units
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
TARGET GAP
</div>

<div class="kpi-value">
{format_number(abs(target_gap_units))}
</div>

<div class="kpi-sub">
Same as Page 4 Scorecard 2
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        net_color = (
            COLORS["green"]
            if net_backlog_after_excess <= 0
            else COLORS["red"]
        )

        st.markdown(
            f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
NET BACKLOG AFTER EXCESS
</div>

<div class="kpi-value"
style="color:{net_color};">
{format_number(max(net_backlog_after_excess, 0))}
</div>

<div class="kpi-sub">
Backlog less available excess
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    with c4:

        st.markdown(
            f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
BACKLOG COVERAGE
</div>

<div class="kpi-value">
{format_percent(excess_coverage_pct)}
</div>

<div class="kpi-sub">
Excess covering backlog
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    with c5:

        if backlog_units_sum <= 0:

            backlog_status = "NO BACKLOG"
            backlog_color = COLORS["green"]

        elif net_backlog_after_excess <= 0:

            backlog_status = "COVERED"
            backlog_color = COLORS["green"]

        elif excess_coverage_pct >= 75:

            backlog_status = "LOW PRESSURE"
            backlog_color = COLORS["green"]

        elif excess_coverage_pct >= 40:

            backlog_status = "MODERATE"
            backlog_color = COLORS["gold"]

        elif excess_coverage_pct >= 20:

            backlog_status = "HIGH"
            backlog_color = COLORS["red"]

        else:

            backlog_status = "CRITICAL"
            backlog_color = COLORS["red_light"]


        st.markdown(
            f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
BACKLOG STATUS
</div>

<div class="kpi-value"
style="color:{backlog_color};font-size:22px;">
{backlog_status}
</div>

<div class="kpi-sub">
Operational pressure indicator
</div>

</div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    if business_area_column:

        backlog_df = filtered_df.copy()


        if detected_columns["backlog_units"]:

            backlog_df[
                "Backlog"
            ] = safe_numeric(
                backlog_df[
                    detected_columns[
                        "backlog_units"
                    ]
                ]
            )

        else:

            backlog_df["Backlog"] = 0


        if detected_columns["excess"]:

            backlog_df[
                "Excess"
            ] = safe_numeric(
                backlog_df[
                    detected_columns[
                        "excess"
                    ]
                ]
            )

        else:

            backlog_df["Excess"] = 0


        area_backlog = (

            backlog_df

            .groupby(
                business_area_column,
                as_index=False
            )

            .agg(

                Backlog=(
                    "Backlog",
                    "sum"
                ),

                Excess=(
                    "Excess",
                    "sum"
                )

            )

        )


        area_backlog[
            "Net Exposure"
        ] = (

            area_backlog["Backlog"]
            -
            area_backlog["Excess"]

        )


        area_backlog = area_backlog.sort_values(
            "Backlog",
            ascending=False
        )


        fig_backlog = go.Figure()


        fig_backlog.add_trace(

            go.Bar(

                x=area_backlog[
                    business_area_column
                ],

                y=area_backlog[
                    "Backlog"
                ],

                name="Backlog",

                marker_color=COLORS[
                    "red"
                ]

            )

        )


        fig_backlog.add_trace(

            go.Bar(

                x=area_backlog[
                    business_area_column
                ],

                y=area_backlog[
                    "Excess"
                ],

                name="Excess",

                marker_color=COLORS[
                    "green"
                ]

            )

        )


        fig_backlog.update_layout(

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
                    color=COLORS["text"],
                    size=13
                )

            )

        )


        fig_backlog.update_xaxes(

            tickfont=dict(
                color=COLORS["text"]
            ),

            showgrid=False

        )


        fig_backlog.update_yaxes(

            title="Units",

            tickfont=dict(
                color=COLORS["text"]
            ),

            gridcolor="rgba(255,255,255,0.08)"

        )


        st.plotly_chart(

            fig_backlog,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

        )


        display_backlog = area_backlog.copy()


        display_backlog[
            "Backlog"
        ] = display_backlog[
            "Backlog"
        ].apply(format_number)


        display_backlog[
            "Excess"
        ] = display_backlog[
            "Excess"
        ].apply(format_number)


        display_backlog[
            "Net Exposure"
        ] = display_backlog[
            "Net Exposure"
        ].apply(format_number)


        st.dataframe(

            display_backlog,

            use_container_width=True,

            hide_index=True

        )


    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown(
        """
<div class="section-number">
BACKLOG INTERPRETATION
</div>

<div class="section-title">
Operational Exposure
</div>
        """,
        unsafe_allow_html=True
    )


    backlog_insights = []


    if backlog_units_sum > 0:

        backlog_insights.append(
            f"Current backlog exposure is {format_number(backlog_units_sum)} units."
        )

    else:

        backlog_insights.append(
            "No backlog exposure is currently recorded."
        )


    if excess_sum > 0:

        backlog_insights.append(
            f"Available excess of {format_number(excess_sum)} units can offset "
            f"approximately {format_percent(excess_coverage_pct)} of the current backlog."
        )


    if net_backlog_after_excess > 0:

        backlog_insights.append(
            f"After considering excess, approximately "
            f"{format_number(net_backlog_after_excess)} units remain exposed."
        )

    else:

        backlog_insights.append(
            "Available excess is sufficient to cover the current recorded backlog."
        )


    for index, insight in enumerate(
        backlog_insights,
        start=1
    ):

        st.markdown(
            f"""
<div class="kpi-card"
style="min-height:80px;margin-bottom:12px;">

<div class="kpi-label">
BACKLOG INSIGHT {index:02d}
</div>

<div style="
font-size:14px;
color:#DCE2E8;
line-height:1.7;
">
{insight}
</div>

</div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PAGE 06 — BUSINESS AREA INTELLIGENCE
# ============================================================

elif page == "06  Business Area Intelligence":

    st.markdown(
        """
<div class="section-number">
06 / BUSINESS AREA INTELLIGENCE
</div>

<div class="section-title">
Business Area Diagnostic
</div>

<div class="section-description">
Identify the strongest performer, weakest performer and areas requiring attention.
</div>
        """,
        unsafe_allow_html=True
    )


    if not business_area_column:

        st.warning(
            "Business Area column is not available."
        )

    else:

        area_df = filtered_df.copy()


        if detected_columns["achieved"]:

            area_df[
                "Achieved"
            ] = convert_percentage(
                area_df[
                    detected_columns["achieved"]
                ]
            )

        else:

            area_df["Achieved"] = np.nan


        if detected_columns["projection"]:

            area_df[
                "Projection"
            ] = convert_percentage(
                area_df[
                    detected_columns["projection"]
                ]
            )

        else:

            area_df["Projection"] = np.nan


        if detected_columns["backlog_units"]:

            area_df[
                "Backlog"
            ] = safe_numeric(
                area_df[
                    detected_columns["backlog_units"]
                ]
            )

        else:

            area_df["Backlog"] = 0


        if detected_columns["excess"]:

            area_df[
                "Excess"
            ] = safe_numeric(
                area_df[
                    detected_columns["excess"]
                ]
            )

        else:

            area_df["Excess"] = 0


        area_intelligence = (

            area_df

            .groupby(
                business_area_column,
                as_index=False
            )

            .agg(

                Achieved=(

                    "Achieved",

                    lambda x:
                    x[x != 0].mean()
                    if (x != 0).any()
                    else np.nan

                ),

                Projection=(

                    "Projection",

                    lambda x:
                    x[x != 0].mean()
                    if (x != 0).any()
                    else np.nan

                ),

                Backlog=(
                    "Backlog",
                    "sum"
                ),

                Excess=(
                    "Excess",
                    "sum"
                )

            )

        )


        area_intelligence[
            "Performance Gap"
        ] = abs(

            area_intelligence["Achieved"]
            -
            area_intelligence["Projection"]

        )


        area_intelligence[
            "Net Exposure"
        ] = (

            area_intelligence["Backlog"]
            -
            area_intelligence["Excess"]

        )


        if not area_intelligence.empty:

            best_area_row = area_intelligence.loc[
                area_intelligence["Achieved"].idxmax()
            ]

            worst_area_row = area_intelligence.loc[
                area_intelligence["Achieved"].idxmin()
            ]

            backlog_area_row = area_intelligence.loc[
                area_intelligence["Backlog"].idxmax()
            ]

            excess_area_row = area_intelligence.loc[
                area_intelligence["Excess"].idxmax()
            ]


            c1, c2, c3, c4 = st.columns(4)


            with c1:

                st.markdown(
                    f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
BEST PERFORMING AREA
</div>

<div class="kpi-value"
style="font-size:21px;">
{best_area_row[business_area_column]}
</div>

<div class="kpi-sub">
Achieved: {format_percent(best_area_row["Achieved"])}
</div>

</div>
                    """,
                    unsafe_allow_html=True
                )


            with c2:

                st.markdown(
                    f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
LOWEST PERFORMING AREA
</div>

<div class="kpi-value"
style="font-size:21px;color:{COLORS["red"]};">
{worst_area_row[business_area_column]}
</div>

<div class="kpi-sub">
Achieved: {format_percent(worst_area_row["Achieved"])}
</div>

</div>
                    """,
                    unsafe_allow_html=True
                )


            with c3:

                st.markdown(
                    f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
HIGHEST BACKLOG AREA
</div>

<div class="kpi-value"
style="font-size:21px;">
{backlog_area_row[business_area_column]}
</div>

<div class="kpi-sub">
Backlog: {format_number(backlog_area_row["Backlog"])}
</div>

</div>
                    """,
                    unsafe_allow_html=True
                )


            with c4:

                st.markdown(
                    f"""
<div class="kpi-card scorecard">

<div class="kpi-label">
HIGHEST EXCESS AREA
</div>

<div class="kpi-value"
style="font-size:21px;color:{COLORS["green"]};">
{excess_area_row[business_area_column]}
</div>

<div class="kpi-sub">
Excess: {format_number(excess_area_row["Excess"])}
</div>

</div>
                    """,
                    unsafe_allow_html=True
                )


            st.markdown("<br>", unsafe_allow_html=True)


            display_area = area_intelligence.copy()


            display_area[
                "Achieved"
            ] = display_area[
                "Achieved"
            ].apply(format_percent)


            display_area[
                "Projection"
            ] = display_area[
                "Projection"
            ].apply(format_percent)


            display_area[
                "Performance Gap"
            ] = display_area[
                "Performance Gap"
            ].apply(format_percent)


            display_area[
                "Backlog"
            ] = display_area[
                "Backlog"
            ].apply(format_number)


            display_area[
                "Excess"
            ] = display_area[
                "Excess"
            ].apply(format_number)


            display_area[
                "Net Exposure"
            ] = display_area[
                "Net Exposure"
            ].apply(format_number)


            st.dataframe(

                display_area,

                use_container_width=True,

                hide_index=True

            )


            st.markdown("<br>", unsafe_allow_html=True)


            area_chart_df = area_intelligence.sort_values(
                "Achieved",
                ascending=True
            )


            fig_area = go.Figure()


            fig_area.add_trace(

                go.Bar(

                    x=area_chart_df[
                        "Achieved"
                    ],

                    y=area_chart_df[
                        business_area_column
                    ],

                    orientation="h",

                    name="Achieved",

                    marker_color=COLORS[
                        "blue"
                    ]

                )

            )


            fig_area.update_layout(

                height=max(
                    400,
                    len(area_chart_df) * 60
                ),

                paper_bgcolor=COLORS[
                    "background"
                ],

                plot_bgcolor=COLORS[
                    "background"
                ],

                showlegend=False

            )


            fig_area.update_xaxes(

                ticksuffix="%",

                tickfont=dict(
                    color=COLORS["text"]
                ),

                gridcolor="rgba(255,255,255,0.08)"

            )


            fig_area.update_yaxes(

                tickfont=dict(
                    color=COLORS["text"]
                ),

                showgrid=False

            )


            st.plotly_chart(

                fig_area,

                use_container_width=True,

                config={
                    "displayModeBar": False
                }

            )


# ============================================================
# PAGE 07 — MONTHLY TREND INTELLIGENCE
# ============================================================

elif page == "07  Monthly Trend Intelligence":

    st.markdown(
        """
<div class="section-number">
07 / MONTHLY TREND INTELLIGENCE
</div>

<div class="section-title">
Performance Movement
</div>

<div class="section-description">
Track how achievement, projection, backlog and target position are moving across reporting periods.
</div>
        """,
        unsafe_allow_html=True
    )


    if not month_column:

        st.warning(
            "Month column is not available in the current dataset."
        )

    else:

        monthly_df = filtered_df.copy()


        monthly_df[
            "Month Sort"
        ] = monthly_df[
            month_column
        ].apply(
            get_month_sort_value
        )


        if detected_columns["achieved"]:

            monthly_df[
                "Achieved"
            ] = convert_percentage(
                monthly_df[
                    detected_columns["achieved"]
                ]
            )

        else:

            monthly_df["Achieved"] = np.nan


        if detected_columns["projection"]:

            monthly_df[
                "Projection"
            ] = convert_percentage(
                monthly_df[
                    detected_columns["projection"]
                ]
            )

        else:

            monthly_df["Projection"] = np.nan


        if detected_columns["input_1"]:

            monthly_df[
                "Actual Units"
            ] = safe_numeric(
                monthly_df[
                    detected_columns["input_1"]
                ]
            )

        else:

            monthly_df["Actual Units"] = 0


        if detected_columns["input_2"]:

            monthly_df[
                "Target Units"
            ] = safe_numeric(
                monthly_df[
                    detected_columns["input_2"]
                ]
            )

        else:

            monthly_df["Target Units"] = 0


        if detected_columns["backlog_units"]:

            monthly_df[
                "Backlog"
            ] = safe_numeric(
                monthly_df[
                    detected_columns["backlog_units"]
                ]
            )

        else:

            monthly_df["Backlog"] = 0


        if detected_columns["excess"]:

            monthly_df[
                "Excess"
            ] = safe_numeric(
                monthly_df[
                    detected_columns["excess"]
                ]
            )

        else:

            monthly_df["Excess"] = 0


        monthly_summary = (

            monthly_df

            .groupby(
                [month_column, "Month Sort"],
                as_index=False
            )

            .agg(

                Achieved=(

                    "Achieved",

                    lambda x:
                    x[x != 0].mean()
                    if (x != 0).any()
                    else np.nan

                ),

                Projection=(

                    "Projection",

                    lambda x:
                    x[x != 0].mean()
                    if (x != 0).any()
                    else np.nan

                ),

                ActualUnits=(
                    "Actual Units",
                    "sum"
                ),

                TargetUnits=(
                    "Target Units",
                    "sum"
                ),

                Backlog=(
                    "Backlog",
                    "sum"
                ),

                Excess=(
                    "Excess",
                    "sum"
                )

            )

            .sort_values(
                "Month Sort"
            )

        )


        # ====================================================
        # PERFORMANCE TREND
        # ====================================================

        st.markdown(
            """
<div class="section-number">
PERFORMANCE TREND
</div>

<div class="section-title">
Achieved vs Projection
</div>
            """,
            unsafe_allow_html=True
        )


        fig_monthly_performance = go.Figure()


        fig_monthly_performance.add_trace(

            go.Scatter(

                x=monthly_summary[
                    month_column
                ],

                y=monthly_summary[
                    "Achieved"
                ],

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


        fig_monthly_performance.add_trace(

            go.Scatter(

                x=monthly_summary[
                    month_column
                ],

                y=monthly_summary[
                    "Projection"
                ],

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


        fig_monthly_performance.add_hline(

            y=100,

            line_dash="dash",

            line_color=COLORS["silver"],

            annotation_text="100% Target Level",

            annotation_position="top left"

        )


        fig_monthly_performance.update_layout(

            height=500,

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
                    color=COLORS["text"],
                    size=13
                )

            )

        )


        fig_monthly_performance.update_xaxes(

            title="Month",

            tickfont=dict(
                color=COLORS["text"]
            ),

            showgrid=False

        )


        fig_monthly_performance.update_yaxes(

            title="Performance %",

            ticksuffix="%",
            
            tickfont=dict(
                color=COLORS["text"]
            ),

            gridcolor="rgba(255,255,255,0.08)"

        )


        st.plotly_chart(

            fig_monthly_performance,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

        )


        st.markdown("<br>", unsafe_allow_html=True)


        # ====================================================
        # BACKLOG VS EXCESS TREND
        # ====================================================

        st.markdown(
            """
<div class="section-number">
OPERATIONAL TREND
</div>

<div class="section-title">
Backlog vs Excess
</div>
            """,
            unsafe_allow_html=True
        )


        fig_monthly_backlog = go.Figure()


        fig_monthly_backlog.add_trace(

            go.Scatter(

                x=monthly_summary[
                    month_column
                ],

                y=monthly_summary[
                    "Backlog"
                ],

                mode="lines+markers",

                name="Backlog",

                line=dict(
                    color=COLORS["red"],
                    width=4
                ),

                marker=dict(
                    size=9
                )

            )

        )


        fig_monthly_backlog.add_trace(

            go.Scatter(

                x=monthly_summary[
                    month_column
                ],

                y=monthly_summary[
                    "Excess"
                ],

                mode="lines+markers",

                name="Excess",

                line=dict(
                    color=COLORS["green"],
                    width=4
                ),

                marker=dict(
                    size=9
                )

            )

        )


        fig_monthly_backlog.update_layout(

            height=500,

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
                    color=COLORS["text"],
                    size=13
                )

            )

        )


        fig_monthly_backlog.update_xaxes(

            title="Month",

            tickfont=dict(
                color=COLORS["text"]
            ),

            showgrid=False

        )


        fig_monthly_backlog.update_yaxes(

            title="Units",

            tickfont=dict(
                color=COLORS["text"]
            ),

            gridcolor="rgba(255,255,255,0.08)"

        )


        st.plotly_chart(

            fig_monthly_backlog,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

        )


        st.markdown("<br>", unsafe_allow_html=True)


        # ====================================================
        # MONTHLY DATA TABLE
        # ====================================================

        st.markdown(
            """
<div class="section-number">
MONTHLY DIAGNOSTIC
</div>

<div class="section-title">
Reporting Period Summary
</div>
            """,
            unsafe_allow_html=True
        )


        display_monthly = monthly_summary.copy()


        display_monthly[
            "Achieved"
        ] = display_monthly[
            "Achieved"
        ].apply(format_percent)


        display_monthly[
            "Projection"
        ] = display_monthly[
            "Projection"
        ].apply(format_percent)


        display_monthly[
            "ActualUnits"
        ] = display_monthly[
            "ActualUnits"
        ].apply(format_number)


        display_monthly[
            "TargetUnits"
        ] = display_monthly[
            "TargetUnits"
        ].apply(format_number)


        display_monthly[
            "Backlog"
        ] = display_monthly[
            "Backlog"
        ].apply(format_number)

        st.dataframe(

            display_monthly,

            use_container_width=True,

            hide_index=True

        )


        # ====================================================
        # TREND INTERPRETATION
        # ====================================================

        if len(monthly_summary) >= 2:

            latest = monthly_summary.iloc[-1]

            previous = monthly_summary.iloc[-2]


            trend_insights = []


            if (
                pd.notna(latest["Achieved"])
                and pd.notna(previous["Achieved"])
            ):

                achieved_change = (
                    latest["Achieved"]
                    -
                    previous["Achieved"]
                )


                if achieved_change > 0:

                    trend_insights.append(
                        f"Achievement improved by {achieved_change:.1f} percentage points "
                        f"versus the previous reporting period."
                    )

                elif achieved_change < 0:

                    trend_insights.append(
                        f"Achievement declined by {abs(achieved_change):.1f} percentage points "
                        f"versus the previous reporting period."
                    )

                else:

                    trend_insights.append(
                        "Achievement remained stable versus the previous reporting period."
                    )


            if (
                latest["Backlog"]
                >
                previous["Backlog"]
            ):

                trend_insights.append(
                    f"Backlog increased by "
                    f"{format_number(latest['Backlog'] - previous['Backlog'])} units."
                )

            elif (
                latest["Backlog"]
                <
                previous["Backlog"]
            ):

                trend_insights.append(
                    f"Backlog reduced by "
                    f"{format_number(previous['Backlog'] - latest['Backlog'])} units."
                )

                trend_insights.append(
                    f"Excess reduced by "
                    f"{format_number(previous['Excess'] - latest['Excess'])} units."
                )


            st.markdown("<br>", unsafe_allow_html=True)


            st.markdown(
                """
<div class="section-number">
TREND INTERPRETATION
</div>

<div class="section-title">
What Changed
</div>
                """,
                unsafe_allow_html=True
            )


            for index, insight in enumerate(
                trend_insights,
                start=1
            ):

                st.markdown(
                    f"""
<div class="kpi-card"
style="min-height:80px;margin-bottom:12px;">

<div class="kpi-label">
TREND INSIGHT {index:02d}
</div>

<div style="
font-size:14px;
color:#DCE2E8;
line-height:1.7;
">
{insight}
</div>

</div>
                    """,
                    unsafe_allow_html=True
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
