from pathlib import Path
from datetime import datetime
import importlib.util
import json
import os
import sys

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# APP CONFIG
# =========================================================

st.set_page_config(
    page_title="Rossmann Retail Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent

BURGUNDY = "#4A2630"
BURGUNDY_DARK = "#241418"
BURGUNDY_SOFT = "#6B3A44"
COPPER = "#B87A49"
COPPER_LIGHT = "#E6C4A1"
IVORY = "#F7F4F0"
PAPER = "#FFFFFF"
TEXT = "#2F2928"
MUTED = "#766B67"
GRID = "#ECE6E1"
SAGE = "#708075"
ROSE = "#9A626C"
DANGER = "#A65347"
SLATE = "#68717A"

EXCLUDE_DIRS = {
    ".venv",
    "venv",
    ".git",
    "__pycache__",
    "site-packages",
    "node_modules",
    ".ipynb_checkpoints",
}


# =========================================================
# SAFE HTML
# =========================================================

def html(content):

    content = content.strip()

    if hasattr(st, "html"):

        st.html(content)

    else:

        st.markdown(
            content,
            unsafe_allow_html=True,
        )


html(
    f"""
    <style>

    .stApp {{
        background: {IVORY};
        color: {TEXT};
    }}

    .block-container {{
        max-width: 1480px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }}

    [data-testid="stHeader"] {{
        background: rgba(247,244,240,.94);
        backdrop-filter: blur(8px);
        border-bottom: 1px solid rgba(70,50,45,.07);
    }}

    [data-testid="stSidebar"] {{
        background:
            radial-gradient(
                circle at 12% 8%,
                rgba(184,122,73,.15),
                transparent 27%
            ),
            linear-gradient(
                180deg,
                #201216 0%,
                #351D24 55%,
                #4A2630 100%
            );

        border-right:
            1px solid rgba(255,255,255,.06);
    }}

    [data-testid="stSidebar"] * {{
        color: #F4ECE8;
    }}

    [data-testid="stSidebar"]
    div[role="radiogroup"] label {{

        background:
            rgba(255,255,255,.035);

        border:
            1px solid rgba(255,255,255,.055);

        border-radius: 9px;

        padding:
            .5rem .62rem;

        margin-bottom:
            .26rem;
    }}

    [data-testid="stSidebar"]
    div[role="radiogroup"] label:hover {{

        background:
            rgba(255,255,255,.075);

        border-color:
            rgba(230,196,161,.22);
    }}

    [data-testid="stSidebar"] hr {{
        border-color:
            rgba(255,255,255,.1);
    }}

    h1,
    h2,
    h3 {{
        font-family:
            Georgia,
            "Times New Roman",
            serif;

        color:
            {BURGUNDY_DARK};

        letter-spacing:
            -.015em;
    }}

    .hero {{
        position:
            relative;

        overflow:
            hidden;

        padding:
            2.45rem 2.65rem 2.3rem;

        border-radius:
            18px;

        background:
            radial-gradient(
                circle at 86% 12%,
                rgba(230,196,161,.16),
                transparent 27%
            ),
            linear-gradient(
                135deg,
                #211217 0%,
                #4A2630 55%,
                #6B3A44 100%
            );

        box-shadow:
            0 18px 45px
            rgba(53,29,36,.15);

        margin:
            .25rem 0 1rem;
    }}

    .hero::after {{
        content:
            "";

        position:
            absolute;

        bottom:
            0;

        left:
            0;

        width:
            43%;

        height:
            4px;

        background:
            linear-gradient(
                90deg,
                {COPPER},
                transparent
            );
    }}

    .hero-kicker {{
        color:
            {COPPER_LIGHT};

        font-size:
            .66rem;

        font-weight:
            800;

        letter-spacing:
            .18em;

        text-transform:
            uppercase;

        margin-bottom:
            .7rem;
    }}

    .hero-title {{
        max-width:
            940px;

        color:
            #FFFFFF;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            2.55rem;

        line-height:
            1.15;

        font-weight:
            500;

        letter-spacing:
            -.025em;
    }}

    .hero-subtitle {{
        max-width:
            1020px;

        margin-top:
            .9rem;

        color:
            #EEE5E1;

        font-size:
            .97rem;

        line-height:
            1.7;
    }}

    .hero-meta {{
        display:
            flex;

        gap:
            .5rem;

        flex-wrap:
            wrap;

        margin-top:
            1.25rem;
    }}

    .hero-chip {{
        padding:
            .4rem .68rem;

        border:
            1px solid
            rgba(230,196,161,.27);

        border-radius:
            999px;

        background:
            rgba(255,255,255,.045);

        color:
            #F3E9E4;

        font-size:
            .68rem;
    }}

    .section-eyebrow {{
        color:
            {COPPER};

        font-size:
            .64rem;

        font-weight:
            800;

        letter-spacing:
            .15em;

        text-transform:
            uppercase;

        margin-top:
            .25rem;
    }}

    .section-title {{
        color:
            {BURGUNDY_DARK};

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            1.65rem;

        font-weight:
            600;

        margin-top:
            .15rem;
    }}

    .section-copy {{
        max-width:
            980px;

        color:
            {MUTED};

        font-size:
            .84rem;

        line-height:
            1.6;

        margin:
            .2rem 0 .9rem;
    }}

    .summary-grid {{
        display:
            grid;

        grid-template-columns:
            repeat(3,1fr);

        background:
            #FFFFFF;

        border:
            1px solid #DED6CF;

        border-radius:
            12px;

        overflow:
            hidden;

        margin:
            .45rem 0 1.15rem;

        box-shadow:
            0 6px 18px
            rgba(61,45,38,.035);
    }}

    .summary-cell {{
        padding:
            1rem 1.1rem;

        border-right:
            1px solid #EEE8E3;
    }}

    .summary-cell:last-child {{
        border-right:
            none;
    }}

    .summary-label {{
        color:
            {COPPER};

        font-size:
            .61rem;

        font-weight:
            800;

        letter-spacing:
            .12em;

        text-transform:
            uppercase;

        margin-bottom:
            .32rem;
    }}

    .summary-text {{
        color:
            #4F4643;

        font-size:
            .78rem;

        line-height:
            1.55;
    }}

    .callout {{
        background:
            #FFFFFF;

        border:
            1px solid #DED6CF;

        border-left:
            4px solid {COPPER};

        border-radius:
            0 11px 11px 0;

        padding:
            .95rem 1rem;

        margin:
            .55rem 0 1rem;

        box-shadow:
            0 4px 14px
            rgba(61,45,38,.03);
    }}

    .callout-title {{
        color:
            {COPPER};

        font-size:
            .61rem;

        font-weight:
            800;

        letter-spacing:
            .11em;

        text-transform:
            uppercase;

        margin-bottom:
            .3rem;
    }}

    .callout-text {{
        color:
            #4E4542;

        font-size:
            .82rem;

        line-height:
            1.62;
    }}

    div[data-testid="stMetric"] {{
        min-height:
            116px;

        background:
            #FFFFFF;

        border:
            1px solid #DED6CF;

        border-radius:
            12px;

        padding:
            .88rem 1rem;

        box-shadow:
            0 7px 18px
            rgba(61,45,38,.035);
    }}

    div[data-testid="stMetric"]::before {{
        content:
            "";

        display:
            block;

        width:
            34px;

        height:
            3px;

        border-radius:
            6px;

        background:
            {COPPER};

        margin-bottom:
            .45rem;
    }}

    div[data-testid="stMetricLabel"] {{
        color:
            #875A3B;

        font-size:
            .72rem;
    }}

    div[data-testid="stMetricValue"] {{
        color:
            {BURGUNDY_DARK};

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            1.43rem;
    }}

    div[data-testid="stExpander"] {{
        background:
            #FFFFFF;

        border:
            1px solid #DED6CF;

        border-radius:
            11px;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap:
            .32rem;

        border-bottom:
            1px solid #E5DDD7;
    }}

    .stTabs [data-baseweb="tab"] {{
        height:
            42px;

        background:
            transparent;

        border-radius:
            8px 8px 0 0;

        padding:
            0 .88rem;

        color:
            #665B57;

        font-size:
            .78rem;
    }}

    .stTabs [aria-selected="true"] {{
        background:
            {BURGUNDY} !important;

        color:
            #FFFFFF !important;
    }}

    [data-testid="stDataFrame"] {{
        border:
            1px solid #E4DDD7;

        border-radius:
            10px;

        overflow:
            hidden;
    }}

    .stButton > button,
    .stDownloadButton > button {{
        min-height:
            40px;

        border-radius:
            8px;

        border:
            1px solid {BURGUNDY};

        background:
            {BURGUNDY};

        color:
            #FFFFFF;

        font-weight:
            650;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        background:
            {BURGUNDY_SOFT};

        color:
            #FFFFFF;

        border-color:
            {COPPER};
    }}

    #MainMenu {{
        visibility:
            hidden;
    }}

    footer {{
        visibility:
            hidden;
    }}

    @media (max-width:900px) {{

        .hero {{
            padding:
                1.65rem 1.35rem;
        }}

        .hero-title {{
            font-size:
                2rem;
        }}

        .summary-grid {{
            grid-template-columns:
                1fr;
        }}

        .summary-cell {{
            border-right:
                none;

            border-bottom:
                1px solid #EEE8E3;
        }}
    }}

    </style>
    """
)


# =========================================================
# FILE DISCOVERY
# =========================================================

@st.cache_data(
    show_spinner=False
)
def scan_files(root):

    files = []

    for current, dirs, names in os.walk(root):

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in EXCLUDE_DIRS
        ]

        for name in names:

            files.append(
                str(
                    Path(current)
                    /
                    name
                )
            )

    return files


def project_files(
    suffixes=None
):

    files = [
        Path(path)
        for path in scan_files(
            str(ROOT)
        )
    ]

    if suffixes is None:

        return files

    return [
        path
        for path in files
        if path.suffix.lower()
        in suffixes
    ]


def newest_file(
    *names
):

    wanted = {
        name.lower()
        for name in names
    }

    matches = [
        path
        for path in project_files()
        if path.name.lower()
        in wanted
    ]

    return (
        max(
            matches,
            key=lambda path:
                path.stat().st_mtime
        )
        if matches
        else None
    )


def csv_by_columns(
    required,
    preferred=()
):

    required = set(
        required
    )

    preferred = {
        name.lower()
        for name in preferred
    }

    candidates = project_files(
        {".csv"}
    )

    candidates.sort(
        key=lambda path:
            (
                path.name.lower()
                not in preferred,

                -
                path.stat().st_mtime
            )
    )

    for path in candidates:

        try:

            columns = set(
                pd.read_csv(
                    path,
                    nrows=2,
                    low_memory=False
                )
                .columns
            )

            if required.issubset(
                columns
            ):

                return path

        except Exception:

            pass

    return None


def parquet_by_columns(
    required
):

    required = set(
        required
    )

    candidates = sorted(
        project_files(
            {".parquet"}
        ),

        key=lambda path:
            -
            path.stat().st_mtime
    )

    for path in candidates:

        try:

            columns = set(
                pd.read_parquet(
                    path
                )
                .columns
            )

            if required.issubset(
                columns
            ):

                return path

        except Exception:

            pass

    return None


EDA_PARQUET = parquet_by_columns(
    {
        "Store",
        "Date",
        "Sales",
        "Customers"
    }
)


TRAIN = csv_by_columns(
    {
        "Store",
        "Date",
        "Sales",
        "Customers",
        "Open",
        "Promo"
    },

    (
        "train.csv",
        "train_clean.csv",
        "rossmann_eda_train.csv"
    )
)


STORE = csv_by_columns(
    {
        "Store",
        "StoreType",
        "Assortment",
        "CompetitionDistance"
    },

    (
        "store.csv",
        "store_clean.csv"
    )
)


FORECAST = newest_file(
    "rossmann_42_day_forecast_with_intervals.csv",
    "rossmann_42_day_forecast.csv",
    "future_forecast.csv"
)


VALIDATION = newest_file(
    "validation_predictions.csv"
)


MODEL = newest_file(
    "rossmann_lstm_model.h5",
    "rossmann_lstm.keras"
)


FSCALER = newest_file(
    "feature_scaler.pkl",
    "feature_scaler.joblib"
)


TSCALER = newest_file(
    "target_scaler.pkl",
    "target_scaler.joblib"
)


SCHEMA = newest_file(
    "feature_schema.json",
    "forecast_contract.json"
)


METADATA = newest_file(
    "metadata.json"
)


METRICS = newest_file(
    "evaluation_metrics.json"
)


FIMPORT = newest_file(
    "feature_importance.csv"
)


GIMPORT = newest_file(
    "feature_group_importance.csv"
)


METHOD = newest_file(
    "forecast_methodology.txt"
)


# =========================================================
# LOADERS
# =========================================================

@st.cache_data(
    show_spinner=False
)
def read_csv(
    path
):

    return pd.read_csv(
        path,
        low_memory=False
    )


@st.cache_data(
    show_spinner=False
)
def read_parquet(
    path
):

    return pd.read_parquet(
        path
    )


@st.cache_data(
    show_spinner=False
)
def read_json(
    path
):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(
            file
        )


@st.cache_data(
    show_spinner=False
)
def read_text(
    path
):

    return Path(
        path
    ).read_text(
        encoding="utf-8"
    )


def safe_csv(
    path
):

    try:

        return (
            read_csv(
                str(path)
            )
            if path
            else None
        )

    except Exception:

        return None


def safe_json(
    path
):

    try:

        return (
            read_json(
                str(path)
            )
            if path
            else {}
        )

    except Exception:

        return {}


# =========================================================
# DATA PREPARATION
# =========================================================

def prepare_eda():

    data = None


    if EDA_PARQUET:

        try:

            data = (
                read_parquet(
                    str(
                        EDA_PARQUET
                    )
                )
                .copy()
            )

        except Exception:

            data = None


    if data is None:

        train = safe_csv(
            TRAIN
        )


        if train is None:

            return None


        data = train.copy()

        store = safe_csv(
            STORE
        )


        if (
            store is not None
            and
            "Store"
            in store.columns
        ):

            data = data.merge(
                store.drop_duplicates(
                    "Store"
                ),

                on="Store",

                how="left"
            )


    if "Date" in data.columns:

        data[
            "Date"
        ] = pd.to_datetime(
            data[
                "Date"
            ],
            errors="coerce"
        )


    for column in [
        "Store",
        "DayOfWeek",
        "Sales",
        "Customers",
        "Open",
        "Promo",
        "SchoolHoliday",
        "CompetitionDistance"
    ]:

        if column in data.columns:

            data[
                column
            ] = pd.to_numeric(
                data[
                    column
                ],
                errors="coerce"
            )


    if "StateHoliday" in data.columns:

        data[
            "StateHoliday"
        ] = (
            data[
                "StateHoliday"
            ]
            .astype(
                "string"
            )
            .str.strip()
            .str.lower()
        )


        data[
            "HolidayType"
        ] = (
            data[
                "StateHoliday"
            ]
            .map(
                {
                    "0":
                        "No State Holiday",

                    "a":
                        "Public Holiday",

                    "b":
                        "Easter Holiday",

                    "c":
                        "Christmas"
                }
            )
            .fillna(
                "Other / Unknown"
            )
        )


    if "Date" in data.columns:

        data[
            "MonthName"
        ] = (
            data[
                "Date"
            ]
            .dt.month_name()
        )


        data[
            "DayName"
        ] = (
            data[
                "Date"
            ]
            .dt.day_name()
        )


        data[
            "Quarter"
        ] = (
            data[
                "Date"
            ]
            .dt.quarter
        )


    if {
        "Sales",
        "Customers"
    }.issubset(
        data.columns
    ):

        data[
            "SalesPerCustomer"
        ] = np.where(
            data[
                "Customers"
            ] > 0,

            data[
                "Sales"
            ]
            /
            data[
                "Customers"
            ],

            np.nan
        )


    return data


def prepare_forecast():

    data = safe_csv(
        FORECAST
    )


    if data is None:

        return None


    data = data.copy()


    if "Date" in data.columns:

        data[
            "Date"
        ] = pd.to_datetime(
            data[
                "Date"
            ],
            errors="coerce"
        )


    if "Store" in data.columns:

        data[
            "Store"
        ] = (
            pd.to_numeric(
                data[
                    "Store"
                ],
                errors="coerce"
            )
            .astype(
                "Int64"
            )
        )


    for column in [
        "PredictedSales",
        "Lower90",
        "Upper90",
        "RelativeWidth",
        "Open",
        "Promo",
        "ForecastWeek"
    ]:

        if column in data.columns:

            data[
                column
            ] = pd.to_numeric(
                data[
                    column
                ],
                errors="coerce"
            )


    if {
        "Store",
        "Date",
        "PredictedSales"
    }.issubset(
        data.columns
    ):

        data = (
            data
            .dropna(
                subset=[
                    "Store",
                    "Date",
                    "PredictedSales"
                ]
            )
            .sort_values(
                [
                    "Date",
                    "Store"
                ]
            )
            .reset_index(
                drop=True
            )
        )


        if (
            "ForecastWeek"
            not in data.columns
            and
            not data.empty
        ):

            start = (
                data[
                    "Date"
                ]
                .min()
            )


            data[
                "ForecastWeek"
            ] = (
                (
                    data[
                        "Date"
                    ]
                    -
                    start
                )
                .dt.days
                //
                7
                +
                1
            )


        if (
            "RelativeWidth"
            not in data.columns
            and
            {
                "Lower90",
                "Upper90"
            }.issubset(
                data.columns
            )
        ):

            data[
                "RelativeWidth"
            ] = np.where(
                data[
                    "PredictedSales"
                ] > 0,

                (
                    data[
                        "Upper90"
                    ]
                    -
                    data[
                        "Lower90"
                    ]
                )
                /
                data[
                    "PredictedSales"
                ],

                np.nan
            )


    return data


eda = prepare_eda()

fc = prepare_forecast()

validation = safe_csv(
    VALIDATION
)

metadata = safe_json(
    METADATA
)

metrics_json = safe_json(
    METRICS
)

schema = safe_json(
    SCHEMA
)

feature_importance = safe_csv(
    FIMPORT
)

group_importance = safe_csv(
    GIMPORT
)


EDA_READY = (
    eda is not None
    and
    {
        "Store",
        "Sales"
    }.issubset(
        eda.columns
    )
)


FORECAST_READY = (
    fc is not None
    and
    {
        "Store",
        "Date",
        "PredictedSales"
    }.issubset(
        fc.columns
    )
)


INTERVAL_READY = (
    FORECAST_READY
    and
    {
        "Lower90",
        "Upper90"
    }.issubset(
        fc.columns
    )
)


MODEL_READY = all(
    asset is not None
    for asset in [
        MODEL,
        FSCALER,
        TSCALER,
        SCHEMA
    ]
)


# =========================================================
# PRESENTATION HELPERS
# =========================================================

def fmt_number(
    value,
    decimals=0
):

    try:

        value = float(
            value
        )

        return (
            f"{value:,.{decimals}f}"
            if np.isfinite(
                value
            )
            else "—"
        )

    except Exception:

        return "—"


def fmt_pct(
    value,
    decimals=1
):

    try:

        value = float(
            value
        )

        return (
            f"{value:,.{decimals}f}%"
            if np.isfinite(
                value
            )
            else "—"
        )

    except Exception:

        return "—"


def style_chart(
    fig,
    height=420,
    hovermode="closest"
):

    fig.update_layout(
        height=
            height,

        paper_bgcolor=
            PAPER,

        plot_bgcolor=
            PAPER,

        margin=dict(
            l=18,
            r=18,
            t=52,
            b=18
        ),

        hovermode=
            hovermode,

        font=dict(
            family=
                "Arial",

            color=
                TEXT,

            size=
                12
        ),

        legend=dict(
            orientation=
                "h",

            y=
                1.08,

            bgcolor=
                "rgba(0,0,0,0)"
        ),

        hoverlabel=dict(
            bgcolor=
                "#FFFFFF",

            bordercolor=
                "#D8CEC7"
        )
    )


    fig.update_xaxes(
        gridcolor=
            GRID,

        zeroline=
            False
    )


    fig.update_yaxes(
        gridcolor=
            GRID,

        zeroline=
            False
    )


    return fig


def hero(
    title,
    subtitle,
    chips
):

    chip_html = "".join(
        f'<span class="hero-chip">{chip}</span>'
        for chip in chips
    )


    html(
        f"""
        <div class="hero">

            <div class="hero-kicker">
                Rossmann Retail Decision Intelligence
            </div>

            <div class="hero-title">
                {title}
            </div>

            <div class="hero-subtitle">
                {subtitle}
            </div>

            <div class="hero-meta">
                {chip_html}
            </div>

        </div>
        """
    )


def section(
    eyebrow,
    title,
    copy=""
):

    html(
        f"""
        <div class="section-eyebrow">
            {eyebrow}
        </div>

        <div class="section-title">
            {title}
        </div>

        <div class="section-copy">
            {copy}
        </div>
        """
    )


def summary_grid(
    purpose,
    questions,
    use
):

    html(
        f"""
        <div class="summary-grid">

            <div class="summary-cell">

                <div class="summary-label">
                    Purpose
                </div>

                <div class="summary-text">
                    {purpose}
                </div>

            </div>

            <div class="summary-cell">

                <div class="summary-label">
                    Questions answered
                </div>

                <div class="summary-text">
                    {questions}
                </div>

            </div>

            <div class="summary-cell">

                <div class="summary-label">
                    Decision use
                </div>

                <div class="summary-text">
                    {use}
                </div>

            </div>

        </div>
        """
    )


def callout(
    title,
    text
):

    html(
        f"""
        <div class="callout">

            <div class="callout-title">
                {title}
            </div>

            <div class="callout-text">
                {text}
            </div>

        </div>
        """
    )


def explain(
    what,
    reading,
    why,
    use
):

    with st.expander(
        "Interpretation & decision guidance",
        expanded=True
    ):

        left, right = (
            st.columns(2)
        )


        with left:

            st.markdown(
                "**What this shows**"
            )

            st.write(
                what
            )


            st.markdown(
                "**What the current data says**"
            )

            st.write(
                reading
            )


        with right:

            st.markdown(
                "**Why it matters**"
            )

            st.write(
                why
            )


            st.markdown(
                "**Decision use**"
            )

            st.write(
                use
            )


def top_share(
    store_df,
    fraction
):

    n = max(
        1,
        int(
            np.ceil(
                len(
                    store_df
                )
                *
                fraction
            )
        )
    )


    total = (
        store_df[
            "PredictedSales"
        ]
        .sum()
    )


    return (
        store_df
        .head(n)[
            "PredictedSales"
        ]
        .sum()
        /
        total
        *
        100
        if total
        else np.nan
    )


# =========================================================
# VALIDATION METRICS
# =========================================================

def compute_validation_metrics():

    if validation is None:

        return {}


    actual_col = next(
        (
            column
            for column in [
                "ActualSales",
                "Actual",
                "Sales"
            ]
            if column
            in validation.columns
        ),
        None
    )


    pred_col = next(
        (
            column
            for column in [
                "PredictedSales",
                "Prediction",
                "Predicted"
            ]
            if column
            in validation.columns
        ),
        None
    )


    if (
        actual_col is None
        or
        pred_col is None
    ):

        return {}


    actual = pd.to_numeric(
        validation[
            actual_col
        ],
        errors="coerce"
    )


    pred = pd.to_numeric(
        validation[
            pred_col
        ],
        errors="coerce"
    )


    valid = (
        actual.notna()
        &
        pred.notna()
    )


    actual = (
        actual[
            valid
        ]
        .to_numpy(
            dtype=float
        )
    )


    pred = (
        pred[
            valid
        ]
        .to_numpy(
            dtype=float
        )
    )


    if not len(
        actual
    ):

        return {}


    error = (
        pred
        -
        actual
    )


    total = (
        np.abs(
            actual
        )
        .sum()
    )


    variance = (
        (
            actual
            -
            actual.mean()
        )
        **
        2
    ).sum()


    return {
        "MAE":
            np.abs(
                error
            )
            .mean(),

        "RMSE":
            np.sqrt(
                np.mean(
                    error
                    **
                    2
                )
            ),

        "WAPE":
            (
                np.abs(
                    error
                )
                .sum()
                /
                total
                *
                100
                if total
                else np.nan
            ),

        "Bias":
            (
                error.sum()
                /
                total
                *
                100
                if total
                else np.nan
            ),

        "R2":
            (
                1
                -
                np.sum(
                    (
                        actual
                        -
                        pred
                    )
                    **
                    2
                )
                /
                variance
                if variance
                else np.nan
            )
    }


computed_metrics = (
    compute_validation_metrics()
)


def metric_value(
    name
):

    normalized = {
        str(key)
        .lower()
        .replace(
            "_",
            ""
        )
        .replace(
            " ",
            ""
        ):
            value

        for key, value
        in metrics_json.items()
    }


    key = (
        name
        .lower()
        .replace(
            "_",
            ""
        )
        .replace(
            " ",
            ""
        )
    )


    if key in normalized:

        try:

            return float(
                normalized[
                    key
                ]
            )

        except Exception:

            pass


    return computed_metrics.get(
        name,
        np.nan
    )


MAE = metric_value(
    "MAE"
)

RMSE = metric_value(
    "RMSE"
)

WAPE = metric_value(
    "WAPE"
)

R2 = metric_value(
    "R2"
)

BIAS = metric_value(
    "Bias"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title(
        "Rossmann Intelligence"
    )


    st.caption(
        "Sales Forecasting & Retail Decision Intelligence"
    )


    st.markdown("")


    st.caption(
        "WORKSPACES"
    )


    page = st.radio(
        "Navigation",

        [
            "Executive Overview",
            "Retail Intelligence",
            "Forecast Intelligence",
            "Store Portfolio",
            "Model Governance",
            "Forecast Service",
            "Application Governance"
        ],

        label_visibility=
            "collapsed"
    )


    st.divider()


    st.caption(
        "SYSTEM STATUS"
    )


    status_1, status_2 = (
        st.columns(2)
    )


    status_1.metric(
        "History",
        (
            "Ready"
            if EDA_READY
            else "Review"
        )
    )


    status_2.metric(
        "Forecast",
        (
            "Ready"
            if FORECAST_READY
            else "Review"
        )
    )


    st.caption(
        "Model package: "
        +
        (
            "ready"
            if MODEL_READY
            else "partial"
        )
    )


# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

if page == "Executive Overview":

    hero(
        "Sales Forecasting & Retail Decision Intelligence",

        (
            "A unified management environment connecting historical retail "
            "behaviour with six-week Store-level forecasting, uncertainty, "
            "prioritisation and model governance."
        ),

        [
            "Historical Intelligence",
            "42-Day Forecast",
            "Store Prioritisation",
            "Uncertainty-Aware Planning"
        ]
    )


    summary_grid(
        (
            "Connect observed retail behaviour "
            "with forward-looking demand."
        ),

        (
            "What shaped demand? When will demand peak? "
            "Which Stores matter most? Where is forecast risk higher?"
        ),

        (
            "Demand readiness, Store prioritisation, commercial review "
            "and forecast governance."
        )
    )


    historical = None


    if EDA_READY:

        historical = (
            eda.copy()
        )


        if "Open" in historical.columns:

            historical = (
                historical[
                    historical[
                        "Open"
                    ]
                    .fillna(0)
                    .eq(1)
                ]
            )


    k1, k2, k3, k4, k5 = (
        st.columns(5)
    )


    if (
        historical is not None
        and
        not historical.empty
    ):

        historical_sales = (
            historical[
                "Sales"
            ]
            .sum()
        )


        historical_customers = (
            historical[
                "Customers"
            ]
            .sum()
            if "Customers"
            in historical.columns
            else np.nan
        )


        k1.metric(
            "Stores Analysed",
            f"{historical['Store'].nunique():,}"
        )


        k2.metric(
            "Historical Sales",
            fmt_number(
                historical_sales
            )
        )


        k3.metric(
            "Sales / Customer",
            fmt_number(
                historical_sales
                /
                historical_customers
                if historical_customers
                else np.nan,

                2
            )
        )


    else:

        k1.metric(
            "Stores Analysed",
            "—"
        )

        k2.metric(
            "Historical Sales",
            "—"
        )

        k3.metric(
            "Sales / Customer",
            "—"
        )


    if FORECAST_READY:

        daily = (
            fc
            .groupby(
                "Date",
                as_index=False
            )[
                "PredictedSales"
            ]
            .sum()
        )


        peak = daily.loc[
            daily[
                "PredictedSales"
            ]
            .idxmax()
        ]


        k4.metric(
            "Six-Week Forecast",
            fmt_number(
                fc[
                    "PredictedSales"
                ]
                .sum()
            )
        )


        k5.metric(
            "Peak Demand Date",
            f"{peak['Date']:%d %b %Y}",
            f"{peak['PredictedSales']:,.0f} Sales"
        )


    else:

        k4.metric(
            "Six-Week Forecast",
            "—"
        )

        k5.metric(
            "Peak Demand Date",
            "—"
        )


    section(
        "Executive demand view",

        "Historical context and forward outlook",

        (
            "A clean view of how the network behaved historically "
            "and what the approved forecast expects next."
        )
    )


    left, right = (
        st.columns(2)
    )


    with left:

        if (
            historical is not None
            and
            "Date"
            in historical.columns
        ):

            historical_daily = (
                historical
                .groupby(
                    "Date",
                    as_index=False
                )[
                    "Sales"
                ]
                .sum()
            )


            figure = go.Figure(
                go.Scatter(
                    x=
                        historical_daily[
                            "Date"
                        ],

                    y=
                        historical_daily[
                            "Sales"
                        ],

                    mode=
                        "lines",

                    line=dict(
                        color=
                            BURGUNDY,

                        width=
                            2.2
                    ),

                    fill=
                        "tozeroy",

                    fillcolor=
                        "rgba(74,38,48,.06)",

                    name=
                        "Historical Sales"
                )
            )


            figure.update_layout(
                title=
                    "Historical Network Demand"
            )


            st.plotly_chart(
                style_chart(
                    figure,
                    360,
                    "x unified"
                ),
                use_container_width=True,
                config={
                    "displaylogo":
                        False
                }
            )


    with right:

        if FORECAST_READY:

            figure = go.Figure(
                go.Scatter(
                    x=
                        daily[
                            "Date"
                        ],

                    y=
                        daily[
                            "PredictedSales"
                        ],

                    mode=
                        "lines",

                    line=dict(
                        color=
                            COPPER,

                        width=
                            3
                    ),

                    name=
                        "Forecast Sales"
                )
            )


            figure.update_layout(
                title=
                    "Forward Network Demand"
            )


            st.plotly_chart(
                style_chart(
                    figure,
                    360,
                    "x unified"
                ),
                use_container_width=True,
                config={
                    "displaylogo":
                        False
                }
            )


    if FORECAST_READY:

        stores = (
            fc
            .groupby(
                "Store",
                as_index=False
            )[
                "PredictedSales"
            ]
            .sum()
            .sort_values(
                "PredictedSales",
                ascending=False
            )
        )


        uncertainty = (
            fc[
                "RelativeWidth"
            ]
            .replace(
                [
                    np.inf,
                    -np.inf
                ],
                np.nan
            )
            .median()
            *
            100
            if "RelativeWidth"
            in fc.columns
            else np.nan
        )


        section(
            "Management brief",

            "What deserves attention",

            (
                "Key points generated from the currently detected "
                "analytical outputs."
            )
        )


        brief_1, brief_2, brief_3 = (
            st.columns(3)
        )


        with brief_1:

            callout(
                "Demand timing",

                (
                    f"Peak network demand is expected on "
                    f"<b>{peak['Date']:%d %B %Y}</b> at "
                    f"<b>{peak['PredictedSales']:,.0f}</b> Sales."
                )
            )


        with brief_2:

            callout(
                "Demand concentration",

                (
                    f"The highest-demand 10% of Stores contribute "
                    f"<b>{top_share(stores,.10):.1f}%</b> "
                    f"of forecast network Sales."
                )
            )


        with brief_3:

            callout(
                "Forecast precision",

                (
                    f"Median relative forecast uncertainty is "
                    f"<b>{fmt_pct(uncertainty)}</b>."
                    if np.isfinite(
                        uncertainty
                    )
                    else
                    "Prediction interval information is not available."
                )
            )


# =========================================================
# RETAIL INTELLIGENCE
# =========================================================

elif page == "Retail Intelligence":

    hero(
        "Historical Retail Intelligence",

        (
            "Explore the commercial conditions associated with Sales across "
            "customers, calendar effects, promotions, Store formats, "
            "assortment and competitive context."
        ),

        [
            "Demand & Seasonality",
            "Customer Behaviour",
            "Promotion & Holidays",
            "Store Structure"
        ]
    )


    if not EDA_READY:

        st.error(
            "Historical Rossmann data was not detected."
        )

        st.stop()


    data = (
        eda.copy()
    )


    with st.expander(
        "Analysis controls",
        expanded=True
    ):

        f1, f2, f3, f4 = (
            st.columns(4)
        )


        if (
            "Date"
            in data.columns
            and
            data[
                "Date"
            ]
            .notna()
            .any()
        ):

            minimum_date = (
                data[
                    "Date"
                ]
                .min()
                .date()
            )


            maximum_date = (
                data[
                    "Date"
                ]
                .max()
                .date()
            )


            selected_dates = (
                f1.date_input(
                    "Historical period",

                    value=(
                        minimum_date,
                        maximum_date
                    ),

                    min_value=
                        minimum_date,

                    max_value=
                        maximum_date
                )
            )


            if (
                isinstance(
                    selected_dates,
                    (
                        tuple,
                        list
                    )
                )
                and
                len(
                    selected_dates
                )
                ==
                2
            ):

                data = (
                    data[
                        data[
                            "Date"
                        ]
                        .between(
                            pd.Timestamp(
                                selected_dates[0]
                            ),

                            pd.Timestamp(
                                selected_dates[1]
                            )
                        )
                    ]
                )


        if "StoreType" in data.columns:

            options = sorted(
                data[
                    "StoreType"
                ]
                .dropna()
                .astype(str)
                .unique()
            )


            selected = (
                f2.multiselect(
                    "Store Type",
                    options,
                    default=
                        options
                )
            )


            if selected:

                data = (
                    data[
                        data[
                            "StoreType"
                        ]
                        .astype(str)
                        .isin(
                            selected
                        )
                    ]
                )


        if "Assortment" in data.columns:

            options = sorted(
                data[
                    "Assortment"
                ]
                .dropna()
                .astype(str)
                .unique()
            )


            selected = (
                f3.multiselect(
                    "Assortment",
                    options,
                    default=
                        options
                )
            )


            if selected:

                data = (
                    data[
                        data[
                            "Assortment"
                        ]
                        .astype(str)
                        .isin(
                            selected
                        )
                    ]
                )


        open_only = (
            f4.toggle(
                "Open Store days only",
                value=True
            )
        )


        if (
            open_only
            and
            "Open"
            in data.columns
        ):

            data = (
                data[
                    data[
                        "Open"
                    ]
                    .fillna(0)
                    .eq(1)
                ]
            )


    if data.empty:

        st.warning(
            "No observations remain after filtering."
        )

        st.stop()


    total_sales = (
        data[
            "Sales"
        ]
        .sum()
    )


    total_customers = (
        data[
            "Customers"
        ]
        .sum()
        if "Customers"
        in data.columns
        else np.nan
    )


    k1, k2, k3, k4, k5 = (
        st.columns(5)
    )


    k1.metric(
        "Sales",
        fmt_number(
            total_sales
        )
    )


    k2.metric(
        "Average Sales",
        fmt_number(
            data[
                "Sales"
            ]
            .mean()
        )
    )


    k3.metric(
        "Customers",
        fmt_number(
            total_customers
        )
    )


    k4.metric(
        "Average Customers",
        fmt_number(
            data[
                "Customers"
            ]
            .mean()
            if "Customers"
            in data.columns
            else np.nan
        )
    )


    k5.metric(
        "Sales / Customer",
        fmt_number(
            total_sales
            /
            total_customers
            if total_customers
            else np.nan,

            2
        )
    )


    (
        demand_tab,
        customer_tab,
        promo_tab,
        store_tab
    ) = st.tabs(
        [
            "Demand & Seasonality",
            "Customer Behaviour",
            "Promotion & Holidays",
            "Store & Competition"
        ]
    )


    with demand_tab:

        resolution = (
            st.selectbox(
                "Trend resolution",
                [
                    "Daily",
                    "Weekly",
                    "Monthly"
                ],
                index=1
            )
        )


        rule = {
            "Daily":
                "D",

            "Weekly":
                "W",

            "Monthly":
                "MS"
        }[
            resolution
        ]


        if "Date" in data.columns:

            trend = (
                data
                .dropna(
                    subset=[
                        "Date"
                    ]
                )
                .set_index(
                    "Date"
                )
                .resample(
                    rule
                )[
                    "Sales"
                ]
                .sum()
                .reset_index()
            )


            figure = go.Figure(
                go.Scatter(
                    x=
                        trend[
                            "Date"
                        ],

                    y=
                        trend[
                            "Sales"
                        ],

                    mode=
                        "lines",

                    line=dict(
                        color=
                            BURGUNDY,

                        width=
                            2.5
                    ),

                    fill=
                        "tozeroy",

                    fillcolor=
                        "rgba(74,38,48,.06)",

                    name=
                        "Sales"
                )
            )


            figure.update_layout(
                title=
                    f"{resolution} Historical Sales Trend"
            )


            st.plotly_chart(
                style_chart(
                    figure,
                    420,
                    "x unified"
                ),
                use_container_width=True,
                config={
                    "displaylogo":
                        False
                }
            )


            if len(
                trend
            ) > 1:

                highest = (
                    trend.loc[
                        trend[
                            "Sales"
                        ]
                        .idxmax()
                    ]
                )


                lowest = (
                    trend.loc[
                        trend[
                            "Sales"
                        ]
                        .idxmin()
                    ]
                )


                explain(
                    (
                        f"Historical Sales aggregated at "
                        f"{resolution.lower()} resolution."
                    ),

                    (
                        f"The strongest displayed period is "
                        f"{highest['Date']:%d %b %Y} "
                        f"({highest['Sales']:,.0f} Sales), while the weakest is "
                        f"{lowest['Date']:%d %b %Y} "
                        f"({lowest['Sales']:,.0f})."
                    ),

                    (
                        "Recurring demand peaks and troughs reveal "
                        "seasonality and calendar structure."
                    ),

                    (
                        "Use repeated high-demand periods for demand-readiness "
                        "planning and investigate exceptional spikes separately."
                    )
                )


        if "DayName" in data.columns:

            day_order = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ]


            weekday = (
                data
                .groupby(
                    "DayName",
                    as_index=False
                )[
                    "Sales"
                ]
                .mean()
            )


            weekday[
                "DayName"
            ] = pd.Categorical(
                weekday[
                    "DayName"
                ],
                categories=
                    day_order,
                ordered=True
            )


            weekday = (
                weekday
                .sort_values(
                    "DayName"
                )
            )


            figure = go.Figure(
                go.Bar(
                    x=
                        weekday[
                            "DayName"
                        ],

                    y=
                        weekday[
                            "Sales"
                        ],

                    marker_color=
                        COPPER,

                    text=
                        weekday[
                            "Sales"
                        ],

                    texttemplate=
                        "%{text:,.0f}",

                    textposition=
                        "outside"
                )
            )


            figure.update_layout(
                title=
                    "Average Sales by Weekday"
            )


            st.plotly_chart(
                style_chart(
                    figure,
                    390
                ),
                use_container_width=True,
                config={
                    "displaylogo":
                        False
                }
            )


    with customer_tab:

        if "Customers" not in data.columns:

            st.info(
                "Customer information is unavailable."
            )


        else:

            valid = (
                data[
                    (
                        data[
                            "Customers"
                        ] > 0
                    )
                    &
                    data[
                        "Sales"
                    ]
                    .notna()
                ]
                .copy()
            )


            correlation = (
                valid[
                    [
                        "Sales",
                        "Customers"
                    ]
                ]
                .corr()
                .iloc[
                    0,
                    1
                ]
            )


            a, b, c = (
                st.columns(3)
            )


            a.metric(
                "Sales–Customer Correlation",
                f"{correlation:.3f}"
            )


            b.metric(
                "Average Customers",
                fmt_number(
                    valid[
                        "Customers"
                    ]
                    .mean()
                )
            )


            c.metric(
                "Sales / Customer",
                fmt_number(
                    valid[
                        "Sales"
                    ]
                    .sum()
                    /
                    valid[
                        "Customers"
                    ]
                    .sum(),

                    2
                )
            )


            sample = (
                valid.sample(
                    min(
                        25000,
                        len(
                            valid
                        )
                    ),
                    random_state=42
                )
                if len(
                    valid
                ) > 25000
                else valid
            )


            left, right = (
                st.columns(
                    [
                        1.35,
                        1
                    ]
                )
            )


            with left:

                figure = go.Figure(
                    go.Scattergl(
                        x=
                            sample[
                                "Customers"
                            ],

                        y=
                            sample[
                                "Sales"
                            ],

                        mode=
                            "markers",

                        marker=dict(
                            size=
                                5,

                            color=
                                COPPER,

                            opacity=
                                .28
                        ),

                        hovertemplate=(
                            "Customers: %{x:,.0f}"
                            "<br>"
                            "Sales: %{y:,.0f}"
                            "<extra></extra>"
                        )
                    )
                )


                figure.update_layout(
                    title=
                        "Sales vs Customer Traffic",

                    xaxis_title=
                        "Customers",

                    yaxis_title=
                        "Sales"
                )


                st.plotly_chart(
                    style_chart(
                        figure,
                        430
                    ),
                    use_container_width=True,
                    config={
                        "displaylogo":
                            False
                    }
                )


            with right:

                if "SalesPerCustomer" in valid.columns:

                    values = (
                        valid[
                            "SalesPerCustomer"
                        ]
                        .replace(
                            [
                                np.inf,
                                -np.inf
                            ],
                            np.nan
                        )
                        .dropna()
                    )


                    if not values.empty:

                        values = (
                            values[
                                values
                                <=
                                values.quantile(
                                    .99
                                )
                            ]
                        )


                        figure = go.Figure(
                            go.Histogram(
                                x=
                                    values,

                                nbinsx=
                                    38,

                                marker_color=
                                    BURGUNDY
                            )
                        )


                        figure.update_layout(
                            title=
                                "Sales per Customer Distribution",

                            xaxis_title=
                                "Sales per Customer",

                            yaxis_title=
                                "Store-Days"
                        )


                        st.plotly_chart(
                            style_chart(
                                figure,
                                430
                            ),
                            use_container_width=True,
                            config={
                                "displaylogo":
                                    False
                            }
                        )


            explain(
                (
                    "Each point represents a Store-day, comparing customer "
                    "traffic with realised Sales."
                ),

                (
                    f"The current filtered data has a Sales–Customer "
                    f"correlation of {correlation:.3f}."
                ),

                (
                    "This helps distinguish traffic-driven Sales from "
                    "changes in customer value."
                ),

                (
                    "Use the association descriptively; correlation does not "
                    "prove causation."
                )
            )


    with promo_tab:

        if "Promo" in data.columns:

            promo = (
                data
                .groupby(
                    "Promo",
                    as_index=False
                )
                .agg(
                    AverageSales=(
                        "Sales",
                        "mean"
                    ),

                    AverageCustomers=(
                        "Customers",
                        "mean"
                    )
                    if "Customers"
                    in data.columns
                    else
                    (
                        "Sales",
                        "size"
                    ),

                    Observations=(
                        "Sales",
                        "size"
                    )
                )
            )


            promo[
                "Condition"
            ] = (
                promo[
                    "Promo"
                ]
                .map(
                    {
                        0:
                            "No Promotion",

                        1:
                            "Promotion"
                    }
                )
            )


            figure = go.Figure(
                go.Bar(
                    x=
                        promo[
                            "Condition"
                        ],

                    y=
                        promo[
                            "AverageSales"
                        ],

                    marker_color=
                        [
                            SAGE,
                            BURGUNDY
                        ][
                            :
                            len(
                                promo
                            )
                        ],

                    text=
                        promo[
                            "AverageSales"
                        ],

                    texttemplate=
                        "%{text:,.0f}",

                    textposition=
                        "outside"
                )
            )


            figure.update_layout(
                title=
                    "Average Sales by Promotion Status"
            )


            st.plotly_chart(
                style_chart(
                    figure,
                    390
                ),
                use_container_width=True,
                config={
                    "displaylogo":
                        False
                }
            )


            non_promo = (
                promo.loc[
                    promo[
                        "Promo"
                    ]
                    .eq(0),
                    "AverageSales"
                ]
            )


            promoted = (
                promo.loc[
                    promo[
                        "Promo"
                    ]
                    .eq(1),
                    "AverageSales"
                ]
            )


            difference = (
                (
                    promoted.iloc[0]
                    /
                    non_promo.iloc[0]
                    -
                    1
                )
                *
                100
                if (
                    len(
                        non_promo
                    )
                    and
                    len(
                        promoted
                    )
                    and
                    non_promo.iloc[0]
                )
                else np.nan
            )


            callout(
                "Promotion effectiveness",

                (
                    f"Promotion-labelled Store-days show an observed average "
                    f"Sales difference of <b>{difference:+.1f}%</b> relative to "
                    f"non-promotion Store-days. This is descriptive "
                    f"effectiveness, not causal ROI."
                )
            )


        left, right = (
            st.columns(2)
        )


        with left:

            if "HolidayType" in data.columns:

                holiday = (
                    data
                    .groupby(
                        "HolidayType",
                        as_index=False
                    )[
                        "Sales"
                    ]
                    .mean()
                    .sort_values(
                        "Sales",
                        ascending=False
                    )
                )


                figure = go.Figure(
                    go.Bar(
                        x=
                            holiday[
                                "HolidayType"
                            ],

                        y=
                            holiday[
                                "Sales"
                            ],

                        marker_color=
                            COPPER
                    )
                )


                figure.update_layout(
                    title=
                        "State Holiday Demand Profile"
                )


                st.plotly_chart(
                    style_chart(
                        figure,
                        370
                    ),
                    use_container_width=True,
                    config={
                        "displaylogo":
                            False
                    }
                )


        with right:

            if "SchoolHoliday" in data.columns:

                school = (
                    data
                    .groupby(
                        "SchoolHoliday",
                        as_index=False
                    )[
                        "Sales"
                    ]
                    .mean()
                )


                school[
                    "Condition"
                ] = (
                    school[
                        "SchoolHoliday"
                    ]
                    .map(
                        {
                            0:
                                "No School Holiday",

                            1:
                                "School Holiday"
                        }
                    )
                )


                figure = go.Figure(
                    go.Bar(
                        x=
                            school[
                                "Condition"
                            ],

                        y=
                            school[
                                "Sales"
                            ],

                        marker_color=
                            [
                                SAGE,
                                ROSE
                            ][
                                :
                                len(
                                    school
                                )
                            ]
                    )
                )


                figure.update_layout(
                    title=
                        "School Holiday Sales Behaviour"
                )


                st.plotly_chart(
                    style_chart(
                        figure,
                        370
                    ),
                    use_container_width=True,
                    config={
                        "displaylogo":
                            False
                    }
                )


    with store_tab:

        left, right = (
            st.columns(2)
        )


        with left:

            if "StoreType" in data.columns:

                store_type = (
                    data
                    .groupby(
                        "StoreType",
                        as_index=False
                    )
                    .agg(
                        AverageSales=(
                            "Sales",
                            "mean"
                        ),

                        Stores=(
                            "Store",
                            "nunique"
                        )
                    )
                    .sort_values(
                        "AverageSales",
                        ascending=False
                    )
                )


                figure = go.Figure(
                    go.Bar(
                        x=
                            store_type[
                                "StoreType"
                            ],

                        y=
                            store_type[
                                "AverageSales"
                            ],

                        marker_color=
                            BURGUNDY
                    )
                )


                figure.update_layout(
                    title=
                        "Average Sales by Store Type"
                )


                st.plotly_chart(
                    style_chart(
                        figure,
                        380
                    ),
                    use_container_width=True,
                    config={
                        "displaylogo":
                            False
                    }
                )


        with right:

            if "Assortment" in data.columns:

                assortment = (
                    data
                    .groupby(
                        "Assortment",
                        as_index=False
                    )
                    .agg(
                        AverageSales=(
                            "Sales",
                            "mean"
                        ),

                        Stores=(
                            "Store",
                            "nunique"
                        )
                    )
                    .sort_values(
                        "AverageSales",
                        ascending=False
                    )
                )


                figure = go.Figure(
                    go.Bar(
                        x=
                            assortment[
                                "Assortment"
                            ],

                        y=
                            assortment[
                                "AverageSales"
                            ],

                        marker_color=
                            COPPER
                    )
                )


                figure.update_layout(
                    title=
                        "Average Sales by Assortment"
                )


                st.plotly_chart(
                    style_chart(
                        figure,
                        380
                    ),
                    use_container_width=True,
                    config={
                        "displaylogo":
                            False
                    }
                )


        if "CompetitionDistance" in data.columns:

            competition = (
                data[
                    [
                        "CompetitionDistance",
                        "Sales"
                    ]
                ]
                .dropna()
                .copy()
            )


            if not competition.empty:

                competition[
                    "CompetitionBand"
                ] = pd.cut(
                    competition[
                        "CompetitionDistance"
                    ],

                    bins=[
                        -np.inf,
                        500,
                        1500,
                        5000,
                        15000,
                        np.inf
                    ],

                    labels=[
                        "Very Near",
                        "Near",
                        "Moderate",
                        "Far",
                        "Very Far"
                    ]
                )


                competition_view = (
                    competition
                    .groupby(
                        "CompetitionBand",
                        observed=False,
                        as_index=False
                    )[
                        "Sales"
                    ]
                    .mean()
                )


                figure = go.Figure(
                    go.Bar(
                        x=
                            competition_view[
                                "CompetitionBand"
                            ],

                        y=
                            competition_view[
                                "Sales"
                            ],

                        marker_color=
                            COPPER
                    )
                )


                figure.update_layout(
                    title=
                        "Average Sales by Competitive Proximity",

                    xaxis_title=
                        "Competition Distance Band",

                    yaxis_title=
                        "Average Sales"
                )


                st.plotly_chart(
                    style_chart(
                        figure,
                        400
                    ),
                    use_container_width=True,
                    config={
                        "displaylogo":
                            False
                    }
                )


                correlation = (
                    competition[
                        [
                            "CompetitionDistance",
                            "Sales"
                        ]
                    ]
                    .corr()
                    .iloc[
                        0,
                        1
                    ]
                )


                callout(
                    "Competition context",

                    (
                        f"The simple Sales–CompetitionDistance correlation is "
                        f"<b>{correlation:.3f}</b>. Competitive proximity should be "
                        f"used as one contextual signal, not as a stand-alone "
                        f"explanation of Store performance."
                    )
                )


# =========================================================
# FORECAST INTELLIGENCE
# =========================================================

elif page == "Forecast Intelligence":

    hero(
        "Forecast & Risk Intelligence",

        (
            "Explore the six-week network outlook, Store concentration, "
            "prediction uncertainty and management priorities."
        ),

        [
            "Network Outlook",
            "Demand Concentration",
            "Forecast Risk",
            "Management Priorities"
        ]
    )


    if not FORECAST_READY:

        st.error(
            "The six-week forecast output was not detected."
        )

        st.stop()


    daily = (
        fc
        .groupby(
            "Date",
            as_index=False
        )[
            "PredictedSales"
        ]
        .sum()
    )


    peak = (
        daily.loc[
            daily[
                "PredictedSales"
            ]
            .idxmax()
        ]
    )


    k1, k2, k3, k4 = (
        st.columns(4)
    )


    k1.metric(
        "Forecast Sales",
        fmt_number(
            fc[
                "PredictedSales"
            ]
            .sum()
        )
    )


    k2.metric(
        "Stores Covered",
        f"{fc['Store'].nunique():,}"
    )


    k3.metric(
        "Forecast Horizon",
        f"{fc['Date'].nunique()} Days"
    )


    k4.metric(
        "Peak Demand Date",
        f"{peak['Date']:%d %b %Y}",
        f"{peak['PredictedSales']:,.0f} Sales"
    )


    (
        outlook_tab,
        concentration_tab,
        risk_tab,
        priority_tab
    ) = st.tabs(
        [
            "Network Outlook",
            "Demand Concentration",
            "Forecast Risk",
            "Management Priorities"
        ]
    )


    with outlook_tab:

        aggregation = {
            "PredictedSales":
                "sum"
        }


        if INTERVAL_READY:

            aggregation.update(
                {
                    "Lower90":
                        "sum",

                    "Upper90":
                        "sum"
                }
            )


        network = (
            fc
            .groupby(
                "Date",
                as_index=False
            )
            .agg(
                aggregation
            )
        )


        figure = go.Figure()


        if INTERVAL_READY:

            figure.add_trace(
                go.Scatter(
                    x=
                        network[
                            "Date"
                        ],

                    y=
                        network[
                            "Upper90"
                        ],

                    mode=
                        "lines",

                    line=dict(
                        width=0
                    ),

                    showlegend=
                        False,

                    hoverinfo=
                        "skip"
                )
            )


            figure.add_trace(
                go.Scatter(
                    x=
                        network[
                            "Date"
                        ],

                    y=
                        network[
                            "Lower90"
                        ],

                    mode=
                        "lines",

                    line=dict(
                        width=0
                    ),

                    fill=
                        "tonexty",

                    fillcolor=
                        "rgba(184,122,73,.18)",

                    name=
                        "90% Prediction Interval"
                )
            )


        figure.add_trace(
            go.Scatter(
                x=
                    network[
                        "Date"
                    ],

                y=
                    network[
                        "PredictedSales"
                    ],

                mode=
                    "lines",

                line=dict(
                    color=
                        BURGUNDY,

                    width=
                        3
                ),

                name=
                    "Forecast Sales"
            )
        )


        figure.update_layout(
            title=
                "Network-Level Six-Week Forecast"
        )


        st.plotly_chart(
            style_chart(
                figure,
                455,
                "x unified"
            ),
            use_container_width=True,
            config={
                "displaylogo":
                    False
            }
        )


        highest = (
            network.loc[
                network[
                    "PredictedSales"
                ]
                .idxmax()
            ]
        )


        lowest = (
            network.loc[
                network[
                    "PredictedSales"
                ]
                .idxmin()
            ]
        )


        explain(
            (
                "Total expected Sales across the Store network by future date. "
                "The shaded band shows the aggregated 90% prediction interval "
                "when available."
            ),

            (
                f"Average expected demand is "
                f"{network['PredictedSales'].mean():,.0f} Sales per day. "
                f"The highest date is {highest['Date']:%d %B %Y} "
                f"({highest['PredictedSales']:,.0f}), while the lowest is "
                f"{lowest['Date']:%d %B %Y} "
                f"({lowest['PredictedSales']:,.0f})."
            ),

            (
                "This reveals when network demand pressure is likely to be "
                "higher or lower."
            ),

            (
                "Use peak dates for demand-readiness planning and wider "
                "intervals as a signal to preserve flexibility."
            )
        )


        weekly = (
            fc
            .groupby(
                "ForecastWeek",
                as_index=False
            )[
                "PredictedSales"
            ]
            .sum()
        )


        figure = go.Figure(
            go.Bar(
                x=
                    weekly[
                        "ForecastWeek"
                    ],

                y=
                    weekly[
                        "PredictedSales"
                    ],

                marker_color=
                    COPPER,

                text=
                    weekly[
                        "PredictedSales"
                    ],

                texttemplate=
                    "%{text:,.0f}",

                textposition=
                    "outside"
            )
        )


        figure.update_layout(
            title=
                "Weekly Forecast Profile",

            xaxis_title=
                "Forecast Week",

            yaxis_title=
                "Forecast Sales"
        )


        st.plotly_chart(
            style_chart(
                figure,
                380
            ),
            use_container_width=True,
            config={
                "displaylogo":
                    False
            }
        )


    with concentration_tab:

        store_forecast = (
            fc
            .groupby(
                "Store",
                as_index=False
            )[
                "PredictedSales"
            ]
            .sum()
            .sort_values(
                "PredictedSales",
                ascending=False
            )
            .reset_index(
                drop=True
            )
        )


        store_forecast[
            "ContributionPct"
        ] = (
            store_forecast[
                "PredictedSales"
            ]
            /
            store_forecast[
                "PredictedSales"
            ]
            .sum()
            *
            100
        )


        shares = {
            "Top 1%":
                top_share(
                    store_forecast,
                    .01
                ),

            "Top 5%":
                top_share(
                    store_forecast,
                    .05
                ),

            "Top 10%":
                top_share(
                    store_forecast,
                    .10
                ),

            "Top 20%":
                top_share(
                    store_forecast,
                    .20
                )
        }


        columns = (
            st.columns(4)
        )


        for column, (
            label,
            value
        ) in zip(
            columns,
            shares.items()
        ):

            column.metric(
                f"{label} Contribution",
                fmt_pct(
                    value
                )
            )


        if len(
            store_forecast
        ) >= 5:

            displayed_stores = (
                st.slider(
                    "Stores displayed",

                    min_value=5,

                    max_value=min(
                        50,
                        len(
                            store_forecast
                        )
                    ),

                    value=min(
                        15,
                        len(
                            store_forecast
                        )
                    )
                )
            )


        else:

            displayed_stores = len(
                store_forecast
            )


        visible = (
            store_forecast
            .head(
                displayed_stores
            )
        )


        figure = go.Figure(
            go.Bar(
                x=
                    visible[
                        "PredictedSales"
                    ],

                y=[
                    f"Store {int(store)}"
                    for store
                    in visible[
                        "Store"
                    ]
                ],

                orientation=
                    "h",

                marker_color=
                    BURGUNDY,

                customdata=
                    visible[
                        "ContributionPct"
                    ],

                hovertemplate=(
                    "%{y}"
                    "<br>"
                    "Forecast Sales: %{x:,.0f}"
                    "<br>"
                    "Contribution: %{customdata:.2f}%"
                    "<extra></extra>"
                )
            )
        )


        figure.update_yaxes(
            autorange=
                "reversed"
        )


        figure.update_layout(
            title=
                "Forecast Demand Concentration"
        )


        st.plotly_chart(
            style_chart(
                figure,
                max(
                    400,
                    displayed_stores
                    *
                    27
                )
            ),
            use_container_width=True,
            config={
                "displaylogo":
                    False
            }
        )


        callout(
            "Portfolio concentration",

            (
                f"The top 10% of Stores contribute "
                f"<b>{shares['Top 10%']:.1f}%</b> of forecast network Sales. "
                f"This represents demand concentration, not profitability."
            )
        )


    with risk_tab:

        if not INTERVAL_READY:

            st.info(
                "Prediction intervals are not available."
            )


        else:

            risk = (
                fc
                .groupby(
                    "Store",
                    as_index=False
                )
                .agg(
                    ForecastSales=(
                        "PredictedSales",
                        "sum"
                    ),

                    Lower90=(
                        "Lower90",
                        "sum"
                    ),

                    Upper90=(
                        "Upper90",
                        "sum"
                    )
                )
            )


            risk[
                "RelativeUncertainty"
            ] = (
                (
                    risk[
                        "Upper90"
                    ]
                    -
                    risk[
                        "Lower90"
                    ]
                )
                /
                risk[
                    "ForecastSales"
                ]
                *
                100
            )


            demand_threshold = (
                risk[
                    "ForecastSales"
                ]
                .quantile(
                    .75
                )
            )


            uncertainty_threshold = (
                risk[
                    "RelativeUncertainty"
                ]
                .quantile(
                    .75
                )
            )


            risk[
                "Priority"
            ] = np.select(
                [
                    (
                        risk[
                            "ForecastSales"
                        ]
                        .ge(
                            demand_threshold
                        )
                        &
                        risk[
                            "RelativeUncertainty"
                        ]
                        .ge(
                            uncertainty_threshold
                        )
                    ),

                    risk[
                        "ForecastSales"
                    ]
                    .ge(
                        demand_threshold
                    ),

                    risk[
                        "RelativeUncertainty"
                    ]
                    .ge(
                        uncertainty_threshold
                    )
                ],

                [
                    "Demand-Critical",
                    "High Demand",
                    "Elevated Uncertainty"
                ],

                default=
                    "Standard"
            )


            colors = {
                "Demand-Critical":
                    DANGER,

                "High Demand":
                    BURGUNDY,

                "Elevated Uncertainty":
                    COPPER,

                "Standard":
                    "#A69D98"
            }


            figure = go.Figure()


            for category, color in colors.items():

                subset = (
                    risk[
                        risk[
                            "Priority"
                        ]
                        .eq(
                            category
                        )
                    ]
                )


                figure.add_trace(
                    go.Scatter(
                        x=
                            subset[
                                "ForecastSales"
                            ],

                        y=
                            subset[
                                "RelativeUncertainty"
                            ],

                        mode=
                            "markers",

                        name=
                            category,

                        marker=dict(
                            size=
                                9,

                            color=
                                color,

                            opacity=
                                .78,

                            line=dict(
                                width=
                                    .5,

                                color=
                                    "#FFFFFF"
                            )
                        ),

                        text=[
                            f"Store {int(store)}"
                            for store
                            in subset[
                                "Store"
                            ]
                        ],

                        hovertemplate=(
                            "<b>%{text}</b>"
                            "<br>"
                            "Forecast Sales: %{x:,.0f}"
                            "<br>"
                            "Relative Uncertainty: %{y:.1f}%"
                            "<extra></extra>"
                        )
                    )
                )


            figure.update_layout(
                title=
                    "Demand Exposure vs Forecast Uncertainty",

                xaxis_title=
                    "Forecast Sales",

                yaxis_title=
                    "Relative Uncertainty %"
            )


            st.plotly_chart(
                style_chart(
                    figure,
                    465
                ),
                use_container_width=True,
                config={
                    "displaylogo":
                        False
                }
            )


            critical = int(
                risk[
                    "Priority"
                ]
                .eq(
                    "Demand-Critical"
                )
                .sum()
            )


            callout(
                "Risk interpretation",

                (
                    f"<b>{critical}</b> Stores are currently classified as "
                    f"Demand-Critical because they combine high expected demand "
                    f"with comparatively high forecast uncertainty."
                )
            )


            st.dataframe(
                risk.sort_values(
                    [
                        "Priority",
                        "ForecastSales"
                    ],
                    ascending=[
                        True,
                        False
                    ]
                ),
                use_container_width=True,
                hide_index=True
            )


    with priority_tab:

        priority = (
            fc
            .groupby(
                "Store",
                as_index=False
            )
            .agg(
                ForecastSales=(
                    "PredictedSales",
                    "sum"
                ),

                ForecastDailyAvg=(
                    "PredictedSales",
                    "mean"
                ),

                PeakDailyForecast=(
                    "PredictedSales",
                    "max"
                )
            )
        )


        if "RelativeWidth" in fc.columns:

            uncertainty = (
                fc
                .groupby(
                    "Store",
                    as_index=False
                )[
                    "RelativeWidth"
                ]
                .median()
                .rename(
                    columns={
                        "RelativeWidth":
                            "RelativeUncertainty"
                    }
                )
            )


            uncertainty[
                "RelativeUncertainty"
            ] *= 100


            priority = (
                priority.merge(
                    uncertainty,
                    on="Store",
                    how="left"
                )
            )


        else:

            priority[
                "RelativeUncertainty"
            ] = np.nan


        if (
            EDA_READY
            and
            "Date"
            in eda.columns
        ):

            history = (
                eda.copy()
            )


            if "Open" in history.columns:

                history = (
                    history[
                        history[
                            "Open"
                        ]
                        .fillna(0)
                        .eq(1)
                    ]
                )


            latest = (
                history[
                    "Date"
                ]
                .max()
            )


            recent = (
                history[
                    history[
                        "Date"
                    ]
                    .between(
                        latest
                        -
                        pd.Timedelta(
                            days=41
                        ),

                        latest
                    )
                ]
            )


            recent_store = (
                recent
                .groupby(
                    "Store",
                    as_index=False
                )[
                    "Sales"
                ]
                .mean()
                .rename(
                    columns={
                        "Sales":
                            "RecentDailyAvg"
                    }
                )
            )


            priority = (
                priority.merge(
                    recent_store,
                    on="Store",
                    how="left"
                )
            )


            priority[
                "ForwardVsRecentPct"
            ] = (
                priority[
                    "ForecastDailyAvg"
                ]
                /
                priority[
                    "RecentDailyAvg"
                ]
                -
                1
            ) * 100


        else:

            priority[
                "RecentDailyAvg"
            ] = np.nan


            priority[
                "ForwardVsRecentPct"
            ] = np.nan


        demand_threshold = (
            priority[
                "ForecastSales"
            ]
            .quantile(
                .75
            )
        )


        uncertainty_threshold = (
            priority[
                "RelativeUncertainty"
            ]
            .quantile(
                .75
            )
            if priority[
                "RelativeUncertainty"
            ]
            .notna()
            .any()
            else np.nan
        )


        priority[
            "ManagementPriority"
        ] = "Standard Review"


        priority.loc[
            priority[
                "ForecastSales"
            ]
            .ge(
                demand_threshold
            ),

            "ManagementPriority"
        ] = "High Demand"


        if np.isfinite(
            uncertainty_threshold
        ):

            priority.loc[
                priority[
                    "RelativeUncertainty"
                ]
                .ge(
                    uncertainty_threshold
                ),

                "ManagementPriority"
            ] = "Elevated Uncertainty"


            priority.loc[
                (
                    priority[
                        "ForecastSales"
                    ]
                    .ge(
                        demand_threshold
                    )
                    &
                    priority[
                        "RelativeUncertainty"
                    ]
                    .ge(
                        uncertainty_threshold
                    )
                ),

                "ManagementPriority"
            ] = "Demand-Critical"


        if priority[
            "ForwardVsRecentPct"
        ].notna().any():

            priority.loc[
                priority[
                    "ForwardVsRecentPct"
                ]
                .ge(
                    20
                ),

                "ManagementPriority"
            ] = "Forward Upside Review"


            priority.loc[
                priority[
                    "ForwardVsRecentPct"
                ]
                .le(
                    -20
                ),

                "ManagementPriority"
            ] = "Forward Downside Review"


            if np.isfinite(
                uncertainty_threshold
            ):

                priority.loc[
                    (
                        priority[
                            "ForecastSales"
                        ]
                        .ge(
                            demand_threshold
                        )
                        &
                        priority[
                            "RelativeUncertainty"
                        ]
                        .ge(
                            uncertainty_threshold
                        )
                    ),

                    "ManagementPriority"
                ] = "Demand-Critical"


        counts = (
            priority[
                "ManagementPriority"
            ]
            .value_counts()
        )


        a, b, c, d = (
            st.columns(4)
        )


        a.metric(
            "Demand-Critical",
            int(
                counts.get(
                    "Demand-Critical",
                    0
                )
            )
        )


        b.metric(
            "High Demand",
            int(
                counts.get(
                    "High Demand",
                    0
                )
            )
        )


        c.metric(
            "Elevated Uncertainty",
            int(
                counts.get(
                    "Elevated Uncertainty",
                    0
                )
            )
        )


        d.metric(
            "Forward Exceptions",
            int(
                counts.get(
                    "Forward Upside Review",
                    0
                )
                +
                counts.get(
                    "Forward Downside Review",
                    0
                )
            )
        )


        categories = sorted(
            priority[
                "ManagementPriority"
            ]
            .unique()
        )


        selected = (
            st.multiselect(
                "Priority categories",

                categories,

                default=[
                    category
                    for category
                    in categories
                    if category
                    !=
                    "Standard Review"
                ]
            )
        )


        view = (
            priority[
                priority[
                    "ManagementPriority"
                ]
                .isin(
                    selected
                )
            ]
            .sort_values(
                "ForecastSales",
                ascending=False
            )
        )


        st.dataframe(
            view,
            use_container_width=True,
            hide_index=True
        )


        st.download_button(
            "Download Management Exception Register",

            data=
                view
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8"
                ),

            file_name=
                "rossmann_management_exception_register.csv",

            mime=
                "text/csv",

            use_container_width=True
        )


# =========================================================
# STORE PORTFOLIO
# =========================================================

elif page == "Store Portfolio":

    hero(
        "Store Portfolio Intelligence",

        (
            "Review one Store across historical performance, structural "
            "attributes, future demand, ranking and forecast uncertainty."
        ),

        [
            "Store Scorecard",
            "Historical Profile",
            "Forward Outlook",
            "Network Ranking"
        ]
    )


    stores = sorted(
        set(
            (
                eda[
                    "Store"
                ]
                .dropna()
                .astype(int)
                .tolist()
                if EDA_READY
                else []
            )
            +
            (
                fc[
                    "Store"
                ]
                .dropna()
                .astype(int)
                .tolist()
                if FORECAST_READY
                else []
            )
        )
    )


    if not stores:

        st.warning(
            "No Store identifiers are available."
        )

        st.stop()


    selected_store = (
        st.selectbox(
            "Select Store",
            stores
        )
    )


    historical_store = (
        eda[
            eda[
                "Store"
            ]
            .eq(
                selected_store
            )
        ]
        .copy()
        if EDA_READY
        else None
    )


    future_store = (
        fc[
            fc[
                "Store"
            ]
            .eq(
                selected_store
            )
        ]
        .copy()
        .sort_values(
            "Date"
        )
        if FORECAST_READY
        else None
    )


    historical_rank = np.nan

    forecast_rank = np.nan


    if EDA_READY:

        ranking = (
            eda
            .groupby(
                "Store",
                as_index=False
            )[
                "Sales"
            ]
            .sum()
            .sort_values(
                "Sales",
                ascending=False
            )
            .reset_index(
                drop=True
            )
        )


        ranking[
            "Rank"
        ] = np.arange(
            1,
            len(
                ranking
            )
            +
            1
        )


        match = (
            ranking.loc[
                ranking[
                    "Store"
                ]
                .eq(
                    selected_store
                ),

                "Rank"
            ]
        )


        if len(
            match
        ):

            historical_rank = int(
                match.iloc[0]
            )


    if FORECAST_READY:

        ranking = (
            fc
            .groupby(
                "Store",
                as_index=False
            )[
                "PredictedSales"
            ]
            .sum()
            .sort_values(
                "PredictedSales",
                ascending=False
            )
            .reset_index(
                drop=True
            )
        )


        ranking[
            "Rank"
        ] = np.arange(
            1,
            len(
                ranking
            )
            +
            1
        )


        match = (
            ranking.loc[
                ranking[
                    "Store"
                ]
                .eq(
                    selected_store
                ),

                "Rank"
            ]
        )


        if len(
            match
        ):

            forecast_rank = int(
                match.iloc[0]
            )


    metrics_row = (
        st.columns(6)
    )


    if (
        historical_store is not None
        and
        not historical_store.empty
    ):

        open_history = (
            historical_store[
                historical_store[
                    "Open"
                ]
                .fillna(0)
                .eq(1)
            ]
            if "Open"
            in historical_store.columns
            else historical_store
        )


        metrics_row[
            0
        ].metric(
            "Historical Sales",
            fmt_number(
                open_history[
                    "Sales"
                ]
                .sum()
            )
        )


        metrics_row[
            1
        ].metric(
            "Average Sales",
            fmt_number(
                open_history[
                    "Sales"
                ]
                .mean()
            )
        )


        metrics_row[
            2
        ].metric(
            "Historical Rank",
            (
                f"#{historical_rank}"
                if np.isfinite(
                    historical_rank
                )
                else "—"
            )
        )


    else:

        metrics_row[
            0
        ].metric(
            "Historical Sales",
            "—"
        )

        metrics_row[
            1
        ].metric(
            "Average Sales",
            "—"
        )

        metrics_row[
            2
        ].metric(
            "Historical Rank",
            "—"
        )


    if (
        future_store is not None
        and
        not future_store.empty
    ):

        peak_store = (
            future_store.loc[
                future_store[
                    "PredictedSales"
                ]
                .idxmax()
            ]
        )


        metrics_row[
            3
        ].metric(
            "Forecast Sales",
            fmt_number(
                future_store[
                    "PredictedSales"
                ]
                .sum()
            )
        )


        metrics_row[
            4
        ].metric(
            "Forecast Rank",
            (
                f"#{forecast_rank}"
                if np.isfinite(
                    forecast_rank
                )
                else "—"
            )
        )


        metrics_row[
            5
        ].metric(
            "Forecast Peak",
            f"{peak_store['Date']:%d %b}",
            f"{peak_store['PredictedSales']:,.0f} Sales"
        )


    else:

        metrics_row[
            3
        ].metric(
            "Forecast Sales",
            "—"
        )

        metrics_row[
            4
        ].metric(
            "Forecast Rank",
            "—"
        )

        metrics_row[
            5
        ].metric(
            "Forecast Peak",
            "—"
        )


    (
        history_tab,
        forward_tab,
        profile_tab
    ) = st.tabs(
        [
            "Historical Profile",
            "Forward Outlook",
            "Store Profile"
        ]
    )


    with history_tab:

        if (
            historical_store is None
            or
            historical_store.empty
        ):

            st.info(
                "Historical information is unavailable for this Store."
            )


        else:

            if "Date" in historical_store.columns:

                trend = (
                    historical_store
                    .groupby(
                        "Date",
                        as_index=False
                    )[
                        "Sales"
                    ]
                    .sum()
                )


                figure = go.Figure(
                    go.Scatter(
                        x=
                            trend[
                                "Date"
                            ],

                        y=
                            trend[
                                "Sales"
                            ],

                        mode=
                            "lines",

                        line=dict(
                            color=
                                BURGUNDY,

                            width=
                                2.25
                        )
                    )
                )


                figure.update_layout(
                    title=
                        f"Store {selected_store} Historical Sales"
                )


                st.plotly_chart(
                    style_chart(
                        figure,
                        410,
                        "x unified"
                    ),
                    use_container_width=True,
                    config={
                        "displaylogo":
                            False
                    }
                )


    with forward_tab:

        if (
            future_store is None
            or
            future_store.empty
        ):

            st.info(
                "Forecast information is unavailable for this Store."
            )


        else:

            figure = go.Figure()


            if {
                "Lower90",
                "Upper90"
            }.issubset(
                future_store.columns
            ):

                figure.add_trace(
                    go.Scatter(
                        x=
                            future_store[
                                "Date"
                            ],

                        y=
                            future_store[
                                "Upper90"
                            ],

                        mode=
                            "lines",

                        line=dict(
                            width=0
                        ),

                        showlegend=
                            False,

                        hoverinfo=
                            "skip"
                    )
                )


                figure.add_trace(
                    go.Scatter(
                        x=
                            future_store[
                                "Date"
                            ],

                        y=
                            future_store[
                                "Lower90"
                            ],

                        mode=
                            "lines",

                        line=dict(
                            width=0
                        ),

                        fill=
                            "tonexty",

                        fillcolor=
                            "rgba(184,122,73,.18)",

                        name=
                            "90% Prediction Interval"
                    )
                )


            figure.add_trace(
                go.Scatter(
                    x=
                        future_store[
                            "Date"
                        ],

                    y=
                        future_store[
                            "PredictedSales"
                        ],

                    mode=
                        "lines+markers",

                    line=dict(
                        color=
                            BURGUNDY,

                        width=
                            3
                    ),

                    marker=dict(
                        color=
                            COPPER,

                        size=
                            6
                    ),

                    name=
                        "Predicted Sales"
                )
            )


            figure.update_layout(
                title=
                    f"Store {selected_store} Six-Week Outlook"
            )


            st.plotly_chart(
                style_chart(
                    figure,
                    435,
                    "x unified"
                ),
                use_container_width=True,
                config={
                    "displaylogo":
                        False
                }
            )


            uncertainty = (
                future_store[
                    "RelativeWidth"
                ]
                .replace(
                    [
                        np.inf,
                        -np.inf
                    ],
                    np.nan
                )
                .median()
                *
                100
                if "RelativeWidth"
                in future_store.columns
                else np.nan
            )


            callout(
                "Store outlook",

                (
                    f"Store {selected_store} has a six-week forecast of "
                    f"<b>{future_store['PredictedSales'].sum():,.0f}</b> Sales. "
                    f"Peak expected daily demand is "
                    f"<b>{peak_store['PredictedSales']:,.0f}</b> on "
                    f"<b>{peak_store['Date']:%d %B %Y}</b>. "
                    f"Median relative uncertainty is "
                    f"<b>{fmt_pct(uncertainty)}</b>."
                )
            )


            st.download_button(
                "Download Store Forecast",

                data=
                    future_store
                    .to_csv(
                        index=False
                    )
                    .encode(
                        "utf-8"
                    ),

                file_name=
                    f"rossmann_store_{selected_store}_forecast.csv",

                mime=
                    "text/csv",

                use_container_width=True
            )


    with profile_tab:

        if (
            historical_store is not None
            and
            not historical_store.empty
        ):

            profile_columns = [
                column
                for column
                in [
                    "StoreType",
                    "Assortment",
                    "CompetitionDistance",
                    "Promo2",
                    "PromoInterval"
                ]
                if column
                in historical_store.columns
            ]


            if profile_columns:

                profile = (
                    historical_store[
                        profile_columns
                    ]
                    .drop_duplicates()
                    .head(1)
                    .T
                    .reset_index()
                )


                profile.columns = [
                    "Store Attribute",
                    "Value"
                ]


                st.dataframe(
                    profile,
                    use_container_width=True,
                    hide_index=True
                )


        score = pd.DataFrame(
            [
                [
                    "Historical Rank",
                    (
                        f"#{historical_rank}"
                        if np.isfinite(
                            historical_rank
                        )
                        else "—"
                    )
                ],

                [
                    "Forecast Rank",
                    (
                        f"#{forecast_rank}"
                        if np.isfinite(
                            forecast_rank
                        )
                        else "—"
                    )
                ]
            ],

            columns=[
                "Indicator",
                "Value"
            ]
        )


        st.dataframe(
            score,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# MODEL GOVERNANCE
# =========================================================

elif page == "Model Governance":

    hero(
        "Model Governance",

        (
            "Inspect validation quality, production configuration, "
            "feature contracts and explainability evidence."
        ),

        [
            "Validation",
            "Feature Contract",
            "Explainability",
            "Methodology"
        ]
    )


    a, b, c, d, e = (
        st.columns(5)
    )


    a.metric(
        "Model",
        metadata.get(
            "model_type",
            "Two-Layer LSTM"
        )
    )


    b.metric(
        "Lookback",
        f"{metadata.get('lookback_days',42)} Days"
    )


    c.metric(
        "Forecast Horizon",
        f"{metadata.get('forecast_horizon_days',42)} Days"
    )


    d.metric(
        "Feature Count",
        metadata.get(
            "feature_count",
            schema.get(
                "feature_count",
                "—"
            )
        )
    )


    e.metric(
        "Training Loss",
        metadata.get(
            "loss",
            "Huber"
        )
    )


    (
        validation_tab,
        contract_tab,
        importance_tab,
        methodology_tab
    ) = st.tabs(
        [
            "Validation Performance",
            "Feature Contract",
            "Feature Intelligence",
            "Forecast Methodology"
        ]
    )


    with validation_tab:

        k1, k2, k3, k4, k5 = (
            st.columns(5)
        )


        k1.metric(
            "MAE",
            fmt_number(
                MAE
            )
        )


        k2.metric(
            "RMSE",
            fmt_number(
                RMSE
            )
        )


        k3.metric(
            "WAPE",
            fmt_pct(
                WAPE
            )
        )


        k4.metric(
            "R²",
            (
                f"{R2:.4f}"
                if np.isfinite(
                    R2
                )
                else "—"
            )
        )


        k5.metric(
            "Bias",
            fmt_pct(
                BIAS
            )
        )


        if validation is not None:

            actual_col = next(
                (
                    column
                    for column in [
                        "ActualSales",
                        "Actual",
                        "Sales"
                    ]
                    if column
                    in validation.columns
                ),
                None
            )


            predicted_col = next(
                (
                    column
                    for column in [
                        "PredictedSales",
                        "Prediction",
                        "Predicted"
                    ]
                    if column
                    in validation.columns
                ),
                None
            )


            if (
                actual_col
                and
                predicted_col
                and
                "Date"
                in validation.columns
            ):

                validation_view = (
                    validation.copy()
                )


                validation_view[
                    "Date"
                ] = pd.to_datetime(
                    validation_view[
                        "Date"
                    ],
                    errors="coerce"
                )


                comparison = (
                    validation_view
                    .groupby(
                        "Date",
                        as_index=False
                    )
                    .agg(
                        Actual=(
                            actual_col,
                            "sum"
                        ),

                        Predicted=(
                            predicted_col,
                            "sum"
                        )
                    )
                )


                figure = go.Figure()


                figure.add_trace(
                    go.Scatter(
                        x=
                            comparison[
                                "Date"
                            ],

                        y=
                            comparison[
                                "Actual"
                            ],

                        mode=
                            "lines",

                        name=
                            "Actual Sales",

                        line=dict(
                            color=
                                BURGUNDY_DARK,

                            width=
                                2.7
                        )
                    )
                )


                figure.add_trace(
                    go.Scatter(
                        x=
                            comparison[
                                "Date"
                            ],

                        y=
                            comparison[
                                "Predicted"
                            ],

                        mode=
                            "lines",

                        name=
                            "Predicted Sales",

                        line=dict(
                            color=
                                COPPER,

                            width=
                                2.7
                        )
                    )
                )


                figure.update_layout(
                    title=
                        "Validation Actual vs Predicted Sales"
                )


                st.plotly_chart(
                    style_chart(
                        figure,
                        425,
                        "x unified"
                    ),
                    use_container_width=True,
                    config={
                        "displaylogo":
                            False
                    }
                )


                callout(
                    "Validation reading",

                    (
                        f"MAE <b>{fmt_number(MAE)}</b> · "
                        f"RMSE <b>{fmt_number(RMSE)}</b> · "
                        f"WAPE <b>{fmt_pct(WAPE)}</b> · "
                        f"R² <b>{f'{R2:.4f}' if np.isfinite(R2) else '—'}</b> · "
                        f"Bias <b>{fmt_pct(BIAS)}</b>."
                    )
                )


    with contract_tab:

        features = schema.get(
            "ordered_features",
            schema.get(
                "features",
                []
            )
        )


        if features:

            st.dataframe(
                pd.DataFrame(
                    {
                        "Position":
                            range(
                                1,
                                len(
                                    features
                                )
                                +
                                1
                            ),

                        "Feature":
                            features
                    }
                ),
                use_container_width=True,
                hide_index=True
            )


        else:

            st.info(
                "The serialized feature contract was not detected."
            )


    with importance_tab:

        if (
            feature_importance is not None
            and
            not feature_importance.empty
        ):

            numeric_columns = (
                feature_importance
                .select_dtypes(
                    include=
                        np.number
                )
                .columns
                .tolist()
            )


            text_columns = [
                column
                for column
                in feature_importance.columns
                if column
                not in numeric_columns
            ]


            if (
                numeric_columns
                and
                text_columns
            ):

                visible = (
                    feature_importance
                    .sort_values(
                        numeric_columns[0],
                        ascending=False
                    )
                    .head(20)
                )


                figure = go.Figure(
                    go.Bar(
                        x=
                            visible[
                                numeric_columns[0]
                            ],

                        y=
                            visible[
                                text_columns[0]
                            ],

                        orientation=
                            "h",

                        marker_color=
                            COPPER
                    )
                )


                figure.update_yaxes(
                    autorange=
                        "reversed"
                )


                figure.update_layout(
                    title=
                        "Leading Forecast Features"
                )


                st.plotly_chart(
                    style_chart(
                        figure,
                        500
                    ),
                    use_container_width=True,
                    config={
                        "displaylogo":
                            False
                    }
                )


            st.dataframe(
                feature_importance,
                use_container_width=True,
                hide_index=True
            )


        else:

            st.info(
                "Feature-importance evidence was not detected."
            )


        if (
            group_importance is not None
            and
            not group_importance.empty
        ):

            section(
                "Feature families",
                "Grouped feature intelligence"
            )


            st.dataframe(
                group_importance,
                use_container_width=True,
                hide_index=True
            )


    with methodology_tab:

        if METHOD:

            try:

                st.text_area(
                    "Forecast methodology",

                    read_text(
                        str(
                            METHOD
                        )
                    ),

                    height=
                        330,

                    disabled=
                        True
                )


            except Exception:

                st.info(
                    "The methodology file could not be read."
                )


        else:

            callout(
                "Production method",

                (
                    "The production workflow uses a two-layer LSTM, "
                    "a 42-day historical lookback, chronological validation, "
                    "Store-safe sequences and recursive six-week forecasting."
                )
            )


# =========================================================
# FORECAST SERVICE
# =========================================================

elif page == "Forecast Service":

    hero(
        "Forecast Service",

        (
            "Retrieve approved Store/date forecasts interactively or "
            "submit a batch request for multiple Store/date combinations."
        ),

        [
            "Interactive Lookup",
            "Batch Retrieval",
            "CSV Export",
            "Approved Horizon"
        ]
    )


    if not FORECAST_READY:

        st.error(
            "Forecast output is unavailable."
        )

        st.stop()


    lookup_tab, batch_tab = (
        st.tabs(
            [
                "Interactive Lookup",
                "Batch Forecast Retrieval"
            ]
        )
    )


    with lookup_tab:

        stores = sorted(
            fc[
                "Store"
            ]
            .dropna()
            .astype(int)
            .unique()
        )


        left, right = (
            st.columns(2)
        )


        selected_store = (
            left.selectbox(
                "Store",
                stores
            )
        )


        dates = (
            fc.loc[
                fc[
                    "Store"
                ]
                .eq(
                    selected_store
                ),

                "Date"
            ]
            .dropna()
            .sort_values()
            .dt.date
            .tolist()
        )


        selected_date = (
            right.selectbox(
                "Forecast date",
                dates
            )
        )


        row = (
            fc[
                fc[
                    "Store"
                ]
                .eq(
                    selected_store
                )
                &
                fc[
                    "Date"
                ]
                .dt.date
                .eq(
                    selected_date
                )
            ]
            .head(1)
        )


        if not row.empty:

            record = (
                row.iloc[0]
            )


            m1, m2, m3, m4, m5 = (
                st.columns(5)
            )


            m1.metric(
                "Predicted Sales",
                fmt_number(
                    record[
                        "PredictedSales"
                    ]
                )
            )


            m2.metric(
                "Lower 90%",
                (
                    fmt_number(
                        record[
                            "Lower90"
                        ]
                    )
                    if "Lower90"
                    in row.columns
                    else "—"
                )
            )


            m3.metric(
                "Upper 90%",
                (
                    fmt_number(
                        record[
                            "Upper90"
                        ]
                    )
                    if "Upper90"
                    in row.columns
                    else "—"
                )
            )


            m4.metric(
                "Open",
                (
                    str(
                        int(
                            record[
                                "Open"
                            ]
                        )
                    )
                    if (
                        "Open"
                        in row.columns
                        and
                        pd.notna(
                            record[
                                "Open"
                            ]
                        )
                    )
                    else "—"
                )
            )


            m5.metric(
                "Promotion",
                (
                    str(
                        int(
                            record[
                                "Promo"
                            ]
                        )
                    )
                    if (
                        "Promo"
                        in row.columns
                        and
                        pd.notna(
                            record[
                                "Promo"
                            ]
                        )
                    )
                    else "—"
                )
            )


            callout(
                "Forecast interpretation",

                (
                    f"Store <b>{selected_store}</b> has a central forecast "
                    f"of <b>{record['PredictedSales']:,.0f}</b> Sales on "
                    f"<b>{pd.Timestamp(selected_date):%d %B %Y}</b>. "
                    f"The point forecast is the planning baseline; "
                    f"interval bounds communicate uncertainty."
                )
            )


    with batch_tab:

        template = (
            fc[
                [
                    "Store",
                    "Date"
                ]
            ]
            .head(12)
            .copy()
        )


        template[
            "Date"
        ] = (
            template[
                "Date"
            ]
            .dt.strftime(
                "%Y-%m-%d"
            )
        )


        st.download_button(
            "Download Request Template",

            data=
                template
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8"
                ),

            file_name=
                "rossmann_forecast_request.csv",

            mime=
                "text/csv"
        )


        uploaded = (
            st.file_uploader(
                "Upload Store/Date request CSV",
                type=[
                    "csv"
                ]
            )
        )


        if uploaded is not None:

            try:

                request = pd.read_csv(
                    uploaded
                )


                if not {
                    "Store",
                    "Date"
                }.issubset(
                    request.columns
                ):

                    st.error(
                        "CSV must contain Store and Date columns."
                    )


                else:

                    request[
                        "Store"
                    ] = (
                        pd.to_numeric(
                            request[
                                "Store"
                            ],
                            errors="coerce"
                        )
                        .astype(
                            "Int64"
                        )
                    )


                    request[
                        "Date"
                    ] = pd.to_datetime(
                        request[
                            "Date"
                        ],
                        errors="coerce"
                    )


                    columns = [
                        column
                        for column
                        in [
                            "Store",
                            "Date",
                            "ForecastWeek",
                            "Open",
                            "Promo",
                            "PredictedSales",
                            "Lower90",
                            "Upper90",
                            "RelativeWidth"
                        ]
                        if column
                        in fc.columns
                    ]


                    result = (
                        request.merge(
                            fc[
                                columns
                            ],
                            on=[
                                "Store",
                                "Date"
                            ],
                            how="left"
                        )
                    )


                    result[
                        "Status"
                    ] = np.where(
                        result[
                            "PredictedSales"
                        ]
                        .notna(),

                        "Matched",

                        "Outside Available Forecast"
                    )


                    matched = int(
                        result[
                            "Status"
                        ]
                        .eq(
                            "Matched"
                        )
                        .sum()
                    )


                    a, b, c = (
                        st.columns(3)
                    )


                    a.metric(
                        "Requests",
                        len(
                            result
                        )
                    )


                    b.metric(
                        "Matched",
                        matched
                    )


                    c.metric(
                        "Match Rate",
                        fmt_pct(
                            matched
                            /
                            len(
                                result
                            )
                            *
                            100
                            if len(
                                result
                            )
                            else np.nan
                        )
                    )


                    st.dataframe(
                        result,
                        use_container_width=True,
                        hide_index=True
                    )


                    st.download_button(
                        "Download Forecast Results",

                        data=
                            result
                            .to_csv(
                                index=False
                            )
                            .encode(
                                "utf-8"
                            ),

                        file_name=
                            "rossmann_forecast_results.csv",

                        mime=
                            "text/csv",

                        use_container_width=True
                    )


            except Exception as exc:

                st.error(
                    f"Unable to process the request file: {exc}"
                )


# =========================================================
# APPLICATION GOVERNANCE
# =========================================================

elif page == "Application Governance":

    hero(
        "Application Governance",

        (
            "Verify analytical data, forecast outputs, production model "
            "artifacts and runtime dependencies used by the deployed application."
        ),

        [
            "Asset Readiness",
            "Runtime Health",
            "Deployment Evidence",
            "Auditability"
        ]
    )


    assets = {
        "Historical EDA Data":
            EDA_PARQUET
            or
            TRAIN,

        "Store Information":
            STORE,

        "Forecast Output":
            FORECAST,

        "Production Model":
            MODEL,

        "Feature Scaler":
            FSCALER,

        "Target Scaler":
            TSCALER,

        "Feature Contract":
            SCHEMA,

        "Validation Evidence":
            VALIDATION,

        "Evaluation Metrics":
            METRICS,

        "Feature Importance":
            FIMPORT
    }


    asset_register = pd.DataFrame(
        [
            {
                "Asset":
                    name,

                "Status":
                    (
                        "Available"
                        if path
                        else "Missing"
                    ),

                "Location":
                    (
                        str(
                            path.relative_to(
                                ROOT
                            )
                        )
                        if (
                            path
                            and
                            path.is_relative_to(
                                ROOT
                            )
                        )
                        else
                        str(
                            path
                        )
                        if path
                        else "—"
                    )
            }

            for name, path
            in assets.items()
        ]
    )


    dependencies = {
        "Streamlit":
            "streamlit",

        "Pandas":
            "pandas",

        "NumPy":
            "numpy",

        "Plotly":
            "plotly",

        "Joblib":
            "joblib",

        "TensorFlow":
            "tensorflow"
    }


    dependency_register = pd.DataFrame(
        [
            {
                "Dependency":
                    name,

                "Status":
                    (
                        "Available"
                        if importlib.util.find_spec(
                            module
                        )
                        is not None
                        else "Missing"
                    )
            }

            for name, module
            in dependencies.items()
        ]
    )


    a, b, c, d = (
        st.columns(4)
    )


    a.metric(
        "Historical Intelligence",
        (
            "Ready"
            if EDA_READY
            else "Review"
        )
    )


    b.metric(
        "Forecast Intelligence",
        (
            "Ready"
            if FORECAST_READY
            else "Review"
        )
    )


    c.metric(
        "Model Package",
        (
            "Ready"
            if MODEL_READY
            else "Partial"
        )
    )


    d.metric(
        "Dependencies",
        (
            f"{dependency_register['Status'].eq('Available').sum()}"
            f"/"
            f"{len(dependency_register)}"
        )
    )


    (
        assets_tab,
        dependencies_tab,
        runtime_tab
    ) = st.tabs(
        [
            "Application Assets",
            "Dependencies",
            "Runtime"
        ]
    )


    with assets_tab:

        st.dataframe(
            asset_register,
            use_container_width=True,
            hide_index=True
        )


    with dependencies_tab:

        st.dataframe(
            dependency_register,
            use_container_width=True,
            hide_index=True
        )


    with runtime_tab:

        runtime = pd.DataFrame(
            [
                [
                    "Python",
                    sys.version.split()[0]
                ],

                [
                    "Application Directory",
                    str(
                        ROOT
                    )
                ],

                [
                    "Session",
                    datetime.now()
                    .strftime(
                        "%Y-%m-%d %H:%M"
                    )
                ]
            ],

            columns=[
                "Setting",
                "Value"
            ]
        )


        st.dataframe(
            runtime,
            use_container_width=True,
            hide_index=True
        )


    st.download_button(
        "Download System Readiness Report",

        data=
            asset_register
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            ),

        file_name=
            "rossmann_system_readiness.csv",

        mime=
            "text/csv",

        use_container_width=True
    )