from pathlib import Path
from datetime import datetime
import importlib.util
import json
import os
import sys

import streamlit as st


# =========================================================
# SAFE DEPENDENCY LOADING
# =========================================================

try:
    import pandas as pd
    import numpy as np

except ModuleNotFoundError as exc:

    st.set_page_config(
        page_title="Rossmann Retail Intelligence",
        page_icon="📈",
        layout="wide"
    )

    st.error(
        f"Missing package: {exc.name}. "
        "Add streamlit, pandas and numpy to requirements.txt, "
        "commit the file to GitHub, then reboot the app."
    )

    st.stop()


# =========================================================
# APP CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Rossmann Retail Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


ROOT = (
    Path(__file__)
    .resolve()
    .parent
)


BURGUNDY = "#4A2630"
DARK = "#241418"
COPPER = "#B87A49"
IVORY = "#F7F4F0"
TEXT = "#2F2928"


EXCLUDED = {
    ".venv",
    "venv",
    ".git",
    "__pycache__",
    "site-packages",
    "node_modules",
    ".ipynb_checkpoints"
}


# =========================================================
# PROFESSIONAL VISUAL THEME
# =========================================================

st.markdown(
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
        background: rgba(247,244,240,.95);
        border-bottom: 1px solid rgba(70,50,45,.07);
    }}

    [data-testid="stSidebar"] {{
        background:
            radial-gradient(
                circle at 15% 8%,
                rgba(184,122,73,.16),
                transparent 28%
            ),
            linear-gradient(
                180deg,
                #201216 0%,
                #351D24 55%,
                #4A2630 100%
            );

        border-right:
            1px solid
            rgba(255,255,255,.06);
    }}

    [data-testid="stSidebar"] * {{
        color: #F5EEEA;
    }}

    [data-testid="stSidebar"] h1 {{
        font-family:
            Georgia,
            "Times New Roman",
            serif;

        color:
            #FFFFFF !important;
    }}

    [data-testid="stSidebar"]
    div[role="radiogroup"] label {{

        background:
            rgba(255,255,255,.035);

        border:
            1px solid
            rgba(255,255,255,.05);

        border-radius:
            9px;

        padding:
            .5rem .62rem;

        margin-bottom:
            .25rem;
    }}

    [data-testid="stSidebar"]
    div[role="radiogroup"] label:hover {{

        background:
            rgba(255,255,255,.08);

        border-color:
            rgba(230,196,161,.22);
    }}

    h1,
    h2,
    h3 {{
        font-family:
            Georgia,
            "Times New Roman",
            serif;

        color:
            {DARK};

        letter-spacing:
            -.015em;
    }}

    div[data-testid="stMetric"] {{
        min-height:
            108px;

        background:
            #FFFFFF;

        border:
            1px solid #DED6CF;

        border-radius:
            12px;

        padding:
            .85rem 1rem;

        box-shadow:
            0 7px 18px
            rgba(61,45,38,.04);
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
            8px;

        background:
            {COPPER};

        margin-bottom:
            .45rem;
    }}

    div[data-testid="stMetricValue"] {{
        color:
            {DARK};

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            1.4rem;
    }}

    div[data-testid="stMetricLabel"] {{
        color:
            #81563B;

        font-size:
            .72rem;
    }}

    div[data-testid="stExpander"] {{
        border:
            1px solid #DED6CF;

        border-radius:
            11px;

        background:
            #FFFFFF;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap:
            .3rem;

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
            0 .9rem;

        color:
            #665B57;
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
            #6B3A44;

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

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FILE DISCOVERY
# =========================================================

@st.cache_data(
    show_spinner=False
)
def scan_files(
    root
):

    found = []


    for current, dirs, names in os.walk(
        root
    ):

        dirs[:] = [
            directory
            for directory
            in dirs
            if directory
            not in EXCLUDED
        ]


        for name in names:

            found.append(
                str(
                    Path(current)
                    /
                    name
                )
            )


    return found


def files(
    suffixes=None
):

    values = [
        Path(path)
        for path
        in scan_files(
            str(ROOT)
        )
    ]


    if suffixes is None:

        return values


    return [
        path
        for path
        in values
        if path.suffix.lower()
        in suffixes
    ]


def newest(
    *names
):

    wanted = {
        name.lower()
        for name
        in names
    }


    found = [
        path
        for path
        in files()
        if path.name.lower()
        in wanted
    ]


    if not found:

        return None


    return max(
        found,
        key=lambda path:
            path.stat().st_mtime
    )


def csv_with(
    required,
    preferred=()
):

    required = set(
        required
    )


    preferred = {
        name.lower()
        for name
        in preferred
    }


    candidates = files(
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


def parquet_with(
    required
):

    required = set(
        required
    )


    candidates = sorted(
        files(
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


# =========================================================
# FIND PROJECT ASSETS
# =========================================================

EDA_PARQUET = parquet_with(
    {
        "Store",
        "Date",
        "Sales",
        "Customers"
    }
)


TRAIN = csv_with(
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


STORE = csv_with(
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


FORECAST = newest(
    "rossmann_42_day_forecast_with_intervals.csv",
    "rossmann_42_day_forecast.csv",
    "future_forecast.csv"
)


VALIDATION = newest(
    "validation_predictions.csv"
)


MODEL = newest(
    "rossmann_lstm_model.h5",
    "rossmann_lstm.keras"
)


FSCALER = newest(
    "feature_scaler.pkl",
    "feature_scaler.joblib"
)


TSCALER = newest(
    "target_scaler.pkl",
    "target_scaler.joblib"
)


SCHEMA = newest(
    "feature_schema.json",
    "forecast_contract.json"
)


METADATA = newest(
    "metadata.json"
)


METRICS = newest(
    "evaluation_metrics.json"
)


FIMPORT = newest(
    "feature_importance.csv"
)


GIMPORT = newest(
    "feature_group_importance.csv"
)


METHOD = newest(
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

        if path:

            return read_csv(
                str(path)
            )


    except Exception:

        pass


    return None


def safe_json(
    path
):

    try:

        if path:

            return read_json(
                str(path)
            )


    except Exception:

        pass


    return {}


# =========================================================
# PREPARE EDA DATA
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
            and
            "Store"
            in data.columns
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


# =========================================================
# PREPARE FORECAST DATA
# =========================================================

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
# FORMATTING HELPERS
# =========================================================

def fmt_number(
    value,
    decimals=0
):

    try:

        value = float(
            value
        )


        if np.isfinite(
            value
        ):

            return (
                f"{value:,.{decimals}f}"
            )


    except Exception:

        pass


    return "—"


def fmt_pct(
    value,
    decimals=1
):

    try:

        value = float(
            value
        )


        if np.isfinite(
            value
        ):

            return (
                f"{value:,.{decimals}f}%"
            )


    except Exception:

        pass


    return "—"


def page_intro(
    title,
    subtitle,
    eyebrow
):

    st.caption(
        eyebrow.upper()
    )


    st.title(
        title
    )


    st.write(
        subtitle
    )


    st.divider()


def context_panel(
    purpose,
    questions,
    decision
):

    with st.container(
        border=True
    ):

        column_1, column_2, column_3 = (
            st.columns(
                [
                    1,
                    1.35,
                    1
                ]
            )
        )


        with column_1:

            st.markdown(
                "**Purpose**"
            )

            st.write(
                purpose
            )


        with column_2:

            st.markdown(
                "**Questions answered**"
            )


            for question in questions:

                st.markdown(
                    f"- {question}"
                )


        with column_3:

            st.markdown(
                "**Decision use**"
            )

            st.write(
                decision
            )


def explain(
    what,
    reading,
    why,
    decision
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
                decision
            )


def top_share(
    frame,
    fraction
):

    number_of_stores = max(
        1,
        int(
            np.ceil(
                len(
                    frame
                )
                *
                fraction
            )
        )
    )


    total = (
        frame[
            "PredictedSales"
        ]
        .sum()
    )


    if total == 0:

        return np.nan


    return (
        frame
        .head(
            number_of_stores
        )[
            "PredictedSales"
        ]
        .sum()
        /
        total
        *
        100
    )


def line_chart(
    data,
    x,
    y,
    height=400
):

    st.line_chart(
        data=
            data,

        x=
            x,

        y=
            y,

        height=
            height,

        use_container_width=
            True
    )


def bar_chart(
    data,
    x,
    y,
    height=360
):

    st.bar_chart(
        data=
            data,

        x=
            x,

        y=
            y,

        height=
            height,

        use_container_width=
            True
    )


# =========================================================
# VALIDATION METRICS
# =========================================================

def compute_validation_metrics():

    if validation is None:

        return {}


    actual_column = next(
        (
            column
            for column
            in [
                "ActualSales",
                "Actual",
                "Sales"
            ]
            if column
            in validation.columns
        ),
        None
    )


    predicted_column = next(
        (
            column
            for column
            in [
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
        actual_column is None
        or
        predicted_column is None
    ):

        return {}


    actual = pd.to_numeric(
        validation[
            actual_column
        ],
        errors="coerce"
    )


    predicted = pd.to_numeric(
        validation[
            predicted_column
        ],
        errors="coerce"
    )


    valid = (
        actual.notna()
        &
        predicted.notna()
    )


    actual = (
        actual[
            valid
        ]
        .to_numpy(
            dtype=float
        )
    )


    predicted = (
        predicted[
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
        predicted
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
                        predicted
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
        "Sales Forecasting · Retail Analytics · Decision Support"
    )


    st.divider()


    page = st.radio(
        "Workspace",

        [
            "Executive Overview",
            "Retail Intelligence",
            "Forecast Intelligence",
            "Store Portfolio",
            "Model Governance",
            "Forecast Service",
            "Application Governance"
        ]
    )


    st.divider()


    st.caption(
        "SYSTEM STATUS"
    )


    left, right = (
        st.columns(2)
    )


    left.metric(
        "History",
        (
            "Ready"
            if EDA_READY
            else "Review"
        )
    )


    right.metric(
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

    page_intro(
        "Rossmann Retail Intelligence & Sales Forecasting",

        (
            "Historical demand evidence, six-week forecasting, "
            "Store prioritisation and model governance "
            "in one management-facing application."
        ),

        "Retail decision intelligence platform"
    )


    context_panel(
        (
            "Connect observed retail behaviour "
            "with forward demand."
        ),

        [
            "What shaped historical demand?",
            "When will demand peak?",
            "Which Stores matter most?",
            "Where is forecast risk higher?"
        ],

        (
            "Demand readiness, Store prioritisation "
            "and forecast governance."
        )
    )


    historical = (
        eda.copy()
        if EDA_READY
        else None
    )


    if (
        historical is not None
        and
        "Open"
        in historical.columns
    ):

        historical = (
            historical[
                historical[
                    "Open"
                ]
                .fillna(0)
                .eq(1)
            ]
        )


    metric_1, metric_2, metric_3, metric_4, metric_5 = (
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


        metric_1.metric(
            "Stores Analysed",
            f"{historical['Store'].nunique():,}"
        )


        metric_2.metric(
            "Historical Sales",
            fmt_number(
                historical_sales
            )
        )


        metric_3.metric(
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

        metric_1.metric(
            "Stores Analysed",
            "—"
        )

        metric_2.metric(
            "Historical Sales",
            "—"
        )

        metric_3.metric(
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


        peak = (
            daily.loc[
                daily[
                    "PredictedSales"
                ]
                .idxmax()
            ]
        )


        metric_4.metric(
            "Six-Week Forecast",
            fmt_number(
                fc[
                    "PredictedSales"
                ]
                .sum()
            )
        )


        metric_5.metric(
            "Peak Demand Date",
            f"{peak['Date']:%d %b %Y}",
            f"{peak['PredictedSales']:,.0f} Sales"
        )


    else:

        metric_4.metric(
            "Six-Week Forecast",
            "—"
        )

        metric_5.metric(
            "Peak Demand Date",
            "—"
        )


    left, right = (
        st.columns(2)
    )


    with left:

        st.subheader(
            "Historical Network Demand"
        )


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


            line_chart(
                historical_daily,
                "Date",
                "Sales",
                330
            )


        else:

            st.info(
                "Historical trend unavailable."
            )


    with right:

        st.subheader(
            "Forward Network Demand"
        )


        if FORECAST_READY:

            line_chart(
                daily,
                "Date",
                "PredictedSales",
                330
            )


        else:

            st.info(
                "Forecast trend unavailable."
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


        st.subheader(
            "Executive Management Brief"
        )


        brief_1, brief_2, brief_3 = (
            st.columns(3)
        )


        brief_1.info(
            f"**Demand timing**\n\n"
            f"Peak network demand: "
            f"**{peak['Date']:%d %B %Y}** · "
            f"**{peak['PredictedSales']:,.0f} Sales**."
        )


        brief_2.info(
            f"**Demand concentration**\n\n"
            f"Top 10% of Stores contribute "
            f"**{top_share(stores, .10):.1f}%** "
            f"of forecast Sales."
        )


        brief_3.info(
            "**Forecast precision**\n\n"
            +
            (
                f"Median relative uncertainty: "
                f"**{fmt_pct(uncertainty)}**."
                if np.isfinite(
                    uncertainty
                )
                else
                "Prediction interval information is unavailable."
            )
        )


# =========================================================
# RETAIL INTELLIGENCE
# =========================================================

elif page == "Retail Intelligence":

    page_intro(
        "Historical Retail Intelligence",

        (
            "Interactive analysis of demand, customers, promotions, "
            "holidays, Store structure and competition."
        ),

        "Historical performance intelligence"
    )


    if not EDA_READY:

        st.error(
            "Historical Rossmann data was not detected "
            "in the deployed repository."
        )

        st.stop()


    data = eda.copy()


    with st.expander(
        "Analysis Controls",
        expanded=True
    ):

        filter_1, filter_2, filter_3, filter_4 = (
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
                filter_1.date_input(
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
                filter_2.multiselect(
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
                filter_3.multiselect(
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
            filter_4.toggle(
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


    metric_1, metric_2, metric_3, metric_4, metric_5 = (
        st.columns(5)
    )


    metric_1.metric(
        "Sales",
        fmt_number(
            total_sales
        )
    )


    metric_2.metric(
        "Average Sales",
        fmt_number(
            data[
                "Sales"
            ]
            .mean()
        )
    )


    metric_3.metric(
        "Customers",
        fmt_number(
            total_customers
        )
    )


    metric_4.metric(
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


    metric_5.metric(
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
        promotion_tab,
        store_tab
    ) = st.tabs(
        [
            "Demand & Seasonality",
            "Customer Behaviour",
            "Promotion & Holidays",
            "Store & Competition"
        ]
    )


    # -----------------------------------------------------
    # DEMAND & SEASONALITY
    # -----------------------------------------------------

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


            st.subheader(
                f"{resolution} Historical Sales Trend"
            )


            line_chart(
                trend,
                "Date",
                "Sales",
                390
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
                        f"Strongest period: "
                        f"{highest['Date']:%d %b %Y} "
                        f"({highest['Sales']:,.0f}); "
                        f"weakest: "
                        f"{lowest['Date']:%d %b %Y} "
                        f"({lowest['Sales']:,.0f})."
                    ),

                    (
                        "Repeated peaks and troughs reveal "
                        "calendar and seasonal structure."
                    ),

                    (
                        "Use recurring strong periods for demand-readiness "
                        "planning and investigate unusual deviations separately."
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


            st.subheader(
                "Average Sales by Weekday"
            )


            bar_chart(
                weekday,
                "DayName",
                "Sales",
                350
            )


    # -----------------------------------------------------
    # CUSTOMER BEHAVIOUR
    # -----------------------------------------------------

    with customer_tab:

        if "Customers" not in data.columns:

            st.info(
                "Customer information is unavailable."
            )


        else:

            valid = (
                data[
                    data[
                        "Customers"
                    ]
                    .gt(0)
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


            metric_1, metric_2, metric_3 = (
                st.columns(3)
            )


            metric_1.metric(
                "Sales–Customer Correlation",
                f"{correlation:.3f}"
            )


            metric_2.metric(
                "Average Customers",
                fmt_number(
                    valid[
                        "Customers"
                    ]
                    .mean()
                )
            )


            metric_3.metric(
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
                        15000,
                        len(
                            valid
                        )
                    ),
                    random_state=42
                )
                if len(
                    valid
                ) > 15000
                else valid
            )


            st.subheader(
                "Sales vs Customer Traffic"
            )


            st.scatter_chart(
                sample,

                x=
                    "Customers",

                y=
                    "Sales",

                height=
                    410,

                use_container_width=
                    True
            )


            explain(
                (
                    "Each point represents a Store-day with "
                    "customer traffic and realised Sales."
                ),

                (
                    f"Current Sales–Customer correlation: "
                    f"{correlation:.3f}."
                ),

                (
                    "This helps distinguish traffic-driven Sales "
                    "from changes in value per customer."
                ),

                (
                    "Use the relationship descriptively; "
                    "correlation does not prove causation."
                )
            )


    # -----------------------------------------------------
    # PROMOTION & HOLIDAYS
    # -----------------------------------------------------

    with promotion_tab:

        if "Promo" in data.columns:

            promotion = (
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

                    Observations=(
                        "Sales",
                        "size"
                    )
                )
            )


            promotion[
                "Condition"
            ] = (
                promotion[
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


            st.subheader(
                "Average Sales by Promotion Status"
            )


            bar_chart(
                promotion,
                "Condition",
                "AverageSales",
                350
            )


            baseline = (
                promotion.loc[
                    promotion[
                        "Promo"
                    ]
                    .eq(0),

                    "AverageSales"
                ]
            )


            promoted = (
                promotion.loc[
                    promotion[
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
                    baseline.iloc[0]
                    -
                    1
                )
                *
                100
                if (
                    len(
                        baseline
                    )
                    and
                    len(
                        promoted
                    )
                    and
                    baseline.iloc[0]
                )
                else np.nan
            )


            st.info(
                f"Observed promotion-labelled Sales difference: "
                f"**{difference:+.1f}%**. "
                f"This is descriptive effectiveness, not causal ROI."
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


                st.subheader(
                    "State Holiday Demand"
                )


                bar_chart(
                    holiday,
                    "HolidayType",
                    "Sales",
                    330
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


                st.subheader(
                    "School Holiday Demand"
                )


                bar_chart(
                    school,
                    "Condition",
                    "Sales",
                    330
                )


    # -----------------------------------------------------
    # STORE & COMPETITION
    # -----------------------------------------------------

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
                )


                st.subheader(
                    "Average Sales by Store Type"
                )


                bar_chart(
                    store_type,
                    "StoreType",
                    "AverageSales",
                    340
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
                )


                st.subheader(
                    "Average Sales by Assortment"
                )


                bar_chart(
                    assortment,
                    "Assortment",
                    "AverageSales",
                    340
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


                st.subheader(
                    "Average Sales by Competitive Proximity"
                )


                bar_chart(
                    competition_view,
                    "CompetitionBand",
                    "Sales",
                    350
                )


                competition_correlation = (
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


                st.info(
                    f"Sales–CompetitionDistance correlation: "
                    f"**{competition_correlation:.3f}**. "
                    f"Treat competition distance as a contextual signal, "
                    f"not a stand-alone explanation."
                )


# =========================================================
# FORECAST INTELLIGENCE
# =========================================================

elif page == "Forecast Intelligence":

    page_intro(
        "Forecast & Risk Intelligence",

        (
            "Six-week network outlook, demand concentration, "
            "prediction uncertainty and management priorities."
        ),

        "Forward demand intelligence"
    )


    if not FORECAST_READY:

        st.error(
            "The approved forecast output was not detected "
            "in the repository."
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


    metric_1, metric_2, metric_3, metric_4 = (
        st.columns(4)
    )


    metric_1.metric(
        "Forecast Sales",
        fmt_number(
            fc[
                "PredictedSales"
            ]
            .sum()
        )
    )


    metric_2.metric(
        "Stores Covered",
        f"{fc['Store'].nunique():,}"
    )


    metric_3.metric(
        "Forecast Horizon",
        f"{fc['Date'].nunique()} Days"
    )


    metric_4.metric(
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


    # -----------------------------------------------------
    # NETWORK OUTLOOK
    # -----------------------------------------------------

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


        st.subheader(
            "Network-Level Six-Week Forecast"
        )


        line_chart(
            network,
            "Date",
            (
                [
                    "PredictedSales",
                    "Lower90",
                    "Upper90"
                ]
                if INTERVAL_READY
                else
                "PredictedSales"
            ),
            420
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
                "Total predicted network Sales by future date. "
                "Interval lines show forecast uncertainty when available."
            ),

            (
                f"Average expected demand: "
                f"{network['PredictedSales'].mean():,.0f} Sales/day. "
                f"Highest: {highest['PredictedSales']:,.0f} on "
                f"{highest['Date']:%d %b %Y}; "
                f"lowest: {lowest['PredictedSales']:,.0f} on "
                f"{lowest['Date']:%d %b %Y}."
            ),

            (
                "This identifies periods with comparatively "
                "greater or lower operating demand."
            ),

            (
                "Use peak dates for readiness planning and wider "
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


        st.subheader(
            "Weekly Forecast Profile"
        )


        bar_chart(
            weekly,
            "ForecastWeek",
            "PredictedSales",
            330
        )


    # -----------------------------------------------------
    # DEMAND CONCENTRATION
    # -----------------------------------------------------

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


        shares = [
            top_share(
                store_forecast,
                percentage
            )

            for percentage
            in [
                .01,
                .05,
                .10,
                .20
            ]
        ]


        columns = (
            st.columns(4)
        )


        for column, label, value in zip(
            columns,
            [
                "Top 1%",
                "Top 5%",
                "Top 10%",
                "Top 20%"
            ],
            shares
        ):

            column.metric(
                f"{label} Contribution",
                fmt_pct(
                    value
                )
            )


        maximum = min(
            40,
            len(
                store_forecast
            )
        )


        if maximum >= 5:

            displayed = (
                st.slider(
                    "Stores displayed",

                    min_value=5,

                    max_value=
                        maximum,

                    value=min(
                        15,
                        maximum
                    )
                )
            )


        else:

            displayed = maximum


        visible = (
            store_forecast
            .head(
                displayed
            )
            .copy()
        )


        visible[
            "StoreLabel"
        ] = (
            visible[
                "Store"
            ]
            .apply(
                lambda value:
                    f"Store {int(value)}"
            )
        )


        st.subheader(
            "Highest Forecast-Contribution Stores"
        )


        bar_chart(
            visible,
            "StoreLabel",
            "PredictedSales",
            max(
                340,
                displayed
                *
                20
            )
        )


        explain(
            (
                "Stores ranked by total forecast Sales "
                "over the full horizon."
            ),

            (
                f"Top 10% of Stores contribute "
                f"{shares[2]:.1f}% "
                f"of network forecast Sales."
            ),

            (
                "Higher concentration means a smaller group of Stores "
                "carries a larger share of future demand."
            ),

            (
                "Prioritise demand readiness at high-contribution Stores "
                "without interpreting contribution as profitability."
            )
        )


    # -----------------------------------------------------
    # FORECAST RISK
    # -----------------------------------------------------

    with risk_tab:

        if not INTERVAL_READY:

            st.info(
                "Prediction intervals are not available "
                "in the detected forecast file."
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


            st.subheader(
                "Demand Exposure vs Forecast Uncertainty"
            )


            st.scatter_chart(
                risk,

                x=
                    "ForecastSales",

                y=
                    "RelativeUncertainty",

                color=
                    "Priority",

                size=
                    "ForecastSales",

                height=
                    420,

                use_container_width=
                    True
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


            highest_uncertainty = (
                risk.sort_values(
                    "RelativeUncertainty",
                    ascending=False
                )
                .iloc[0]
            )


            explain(
                (
                    "Each point is a Store; demand is on the horizontal "
                    "axis and relative uncertainty on the vertical axis."
                ),

                (
                    f"{critical} Stores are Demand-Critical. "
                    f"Store {int(highest_uncertainty['Store'])} has "
                    f"the highest relative uncertainty at "
                    f"{highest_uncertainty['RelativeUncertainty']:.1f}%."
                ),

                (
                    "High-demand/high-uncertainty Stores combine "
                    "larger commercial exposure with lower forecast precision."
                ),

                (
                    "Review Demand-Critical Stores first and retain "
                    "more flexibility around their central forecast."
                )
            )


    # -----------------------------------------------------
    # MANAGEMENT PRIORITIES
    # -----------------------------------------------------

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


        counts = (
            priority[
                "ManagementPriority"
            ]
            .value_counts()
        )


        metric_1, metric_2, metric_3 = (
            st.columns(3)
        )


        metric_1.metric(
            "Demand-Critical",
            int(
                counts.get(
                    "Demand-Critical",
                    0
                )
            )
        )


        metric_2.metric(
            "High Demand",
            int(
                counts.get(
                    "High Demand",
                    0
                )
            )
        )


        metric_3.metric(
            "Elevated Uncertainty",
            int(
                counts.get(
                    "Elevated Uncertainty",
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

    page_intro(
        "Store Portfolio Intelligence",

        (
            "Review one Store across historical performance, "
            "structural attributes, forecast trajectory, "
            "ranking and uncertainty."
        ),

        "Store-level decision support"
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


    metric_columns = (
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


        metric_columns[
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


        metric_columns[
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


        metric_columns[
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

        metric_columns[
            0
        ].metric(
            "Historical Sales",
            "—"
        )

        metric_columns[
            1
        ].metric(
            "Average Sales",
            "—"
        )

        metric_columns[
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


        metric_columns[
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


        metric_columns[
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


        metric_columns[
            5
        ].metric(
            "Forecast Peak",
            f"{peak_store['Date']:%d %b}",
            f"{peak_store['PredictedSales']:,.0f} Sales"
        )


    else:

        metric_columns[
            3
        ].metric(
            "Forecast Sales",
            "—"
        )

        metric_columns[
            4
        ].metric(
            "Forecast Rank",
            "—"
        )

        metric_columns[
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


            st.subheader(
                f"Store {selected_store} Historical Sales"
            )


            line_chart(
                trend,
                "Date",
                "Sales",
                380
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

            columns = [
                "PredictedSales"
            ]


            if {
                "Lower90",
                "Upper90"
            }.issubset(
                future_store.columns
            ):

                columns.extend(
                    [
                        "Lower90",
                        "Upper90"
                    ]
                )


            st.subheader(
                f"Store {selected_store} Six-Week Outlook"
            )


            line_chart(
                future_store,
                "Date",
                columns,
                390
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


            explain(
                (
                    f"Daily Sales forecast for Store "
                    f"{selected_store}."
                ),

                (
                    f"Total expected Sales: "
                    f"{future_store['PredictedSales'].sum():,.0f}; "
                    f"peak: {peak_store['PredictedSales']:,.0f} on "
                    f"{peak_store['Date']:%d %B %Y}; "
                    f"median relative uncertainty: "
                    f"{fmt_pct(uncertainty)}."
                ),

                (
                    "Store-level demand and forecast precision "
                    "can differ materially from network averages."
                ),

                (
                    "Use the central forecast as the baseline "
                    "and interval width to judge how much "
                    "flexibility is appropriate."
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

            columns = [
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


            if columns:

                profile = (
                    historical_store[
                        columns
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


        scorecard = pd.DataFrame(
            {
                "Indicator":
                    [
                        "Historical Network Rank",
                        "Forecast Network Rank"
                    ],

                "Value":
                    [
                        (
                            f"#{historical_rank}"
                            if np.isfinite(
                                historical_rank
                            )
                            else "—"
                        ),

                        (
                            f"#{forecast_rank}"
                            if np.isfinite(
                                forecast_rank
                            )
                            else "—"
                        )
                    ]
            }
        )


        st.dataframe(
            scorecard,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# MODEL GOVERNANCE
# =========================================================

elif page == "Model Governance":

    page_intro(
        "Model Governance",

        (
            "Validation performance, production configuration, "
            "feature contract and model evidence."
        ),

        "Forecast reliability and governance"
    )


    metric_1, metric_2, metric_3, metric_4, metric_5 = (
        st.columns(5)
    )


    metric_1.metric(
        "Model",
        metadata.get(
            "model_type",
            "Two-Layer LSTM"
        )
    )


    metric_2.metric(
        "Lookback",
        f"{metadata.get('lookback_days', 42)} Days"
    )


    metric_3.metric(
        "Forecast Horizon",
        f"{metadata.get('forecast_horizon_days', 42)} Days"
    )


    metric_4.metric(
        "Feature Count",
        metadata.get(
            "feature_count",
            schema.get(
                "feature_count",
                "—"
            )
        )
    )


    metric_5.metric(
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

        columns = (
            st.columns(5)
        )


        labels = [
            "MAE",
            "RMSE",
            "WAPE",
            "R²",
            "Bias"
        ]


        values = [
            fmt_number(
                MAE
            ),

            fmt_number(
                RMSE
            ),

            fmt_pct(
                WAPE
            ),

            (
                f"{R2:.4f}"
                if np.isfinite(
                    R2
                )
                else "—"
            ),

            fmt_pct(
                BIAS
            )
        ]


        for column, label, value in zip(
            columns,
            labels,
            values
        ):

            column.metric(
                label,
                value
            )


        with st.expander(
            "How to read these metrics"
        ):

            st.markdown(
                """
                **MAE** — average absolute forecast error. Lower is better.

                **RMSE** — penalises larger misses more strongly. Lower is better.

                **WAPE** — total absolute error relative to actual Sales. Lower is better.

                **R²** — how much observed Sales variation is captured. Higher is generally better.

                **Bias** — aggregate directional error. Values closer to zero are preferable.
                """
            )


        if validation is not None:

            actual_column = next(
                (
                    column
                    for column
                    in [
                        "ActualSales",
                        "Actual",
                        "Sales"
                    ]
                    if column
                    in validation.columns
                ),
                None
            )


            predicted_column = next(
                (
                    column
                    for column
                    in [
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
                actual_column
                and
                predicted_column
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
                            actual_column,
                            "sum"
                        ),

                        Predicted=(
                            predicted_column,
                            "sum"
                        )
                    )
                )


                st.subheader(
                    "Validation: Actual vs Predicted"
                )


                line_chart(
                    comparison,
                    "Date",
                    [
                        "Actual",
                        "Predicted"
                    ],
                    390
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
                "Serialized feature contract was not detected."
            )


    with importance_tab:

        if (
            feature_importance is not None
            and
            not feature_importance.empty
        ):

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

            st.subheader(
                "Feature Family Intelligence"
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

                    height=300,

                    disabled=True
                )


            except Exception:

                st.info(
                    "The methodology file could not be read."
                )


        else:

            st.info(
                "The production workflow uses a two-layer LSTM, "
                "42-day lookback, chronological validation, "
                "Store-safe sequences and recursive six-week forecasting."
            )


# =========================================================
# FORECAST SERVICE
# =========================================================

elif page == "Forecast Service":

    page_intro(
        "Forecast Service",

        (
            "Retrieve approved Store/date forecasts interactively "
            "or through a batch request."
        ),

        "Prediction serving"
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


            columns = (
                st.columns(5)
            )


            columns[
                0
            ].metric(
                "Predicted Sales",
                fmt_number(
                    record[
                        "PredictedSales"
                    ]
                )
            )


            columns[
                1
            ].metric(
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


            columns[
                2
            ].metric(
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


            columns[
                3
            ].metric(
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


            columns[
                4
            ].metric(
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


            st.info(
                f"Store **{selected_store}** has a central forecast "
                f"of **{record['PredictedSales']:,.0f} Sales** on "
                f"**{pd.Timestamp(selected_date):%d %B %Y}**."
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


                    metric_1, metric_2, metric_3 = (
                        st.columns(3)
                    )


                    metric_1.metric(
                        "Requests",
                        len(
                            result
                        )
                    )


                    metric_2.metric(
                        "Matched",
                        matched
                    )


                    metric_3.metric(
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
                    f"Unable to process request file: {exc}"
                )


# =========================================================
# APPLICATION GOVERNANCE
# =========================================================

elif page == "Application Governance":

    page_intro(
        "Application Governance",

        (
            "Verify data assets, forecast outputs, model files "
            "and runtime dependencies used by the deployed application."
        ),

        "Deployment readiness and auditability"
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
            "numpy"
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


    metric_1, metric_2, metric_3, metric_4 = (
        st.columns(4)
    )


    metric_1.metric(
        "Historical Intelligence",
        (
            "Ready"
            if EDA_READY
            else "Review"
        )
    )


    metric_2.metric(
        "Forecast Intelligence",
        (
            "Ready"
            if FORECAST_READY
            else "Review"
        )
    )


    metric_3.metric(
        "Model Package",
        (
            "Ready"
            if MODEL_READY
            else "Partial"
        )
    )


    metric_4.metric(
        "Core Dependencies",
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


        missing = (
            asset_register.loc[
                asset_register[
                    "Status"
                ]
                .eq(
                    "Missing"
                ),

                "Asset"
            ]
            .tolist()
        )


        if missing:

            st.warning(
                "Missing or undetected assets: "
                +
                ", ".join(
                    missing
                )
            )


        else:

            st.success(
                "All registered application assets were detected."
            )


    with dependencies_tab:

        st.dataframe(
            dependency_register,
            use_container_width=True,
            hide_index=True
        )


        st.success(
            "This deployment-safe version uses native Streamlit charts. "
            "Plotly is not required, so the previous Plotly "
            "ModuleNotFoundError cannot block application startup."
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
                    "Session Time",
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
