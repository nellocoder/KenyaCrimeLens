"""Data loading, validation and caching for Kenya CrimeLens."""

from __future__ import annotations

import json
import os

import pandas as pd
import streamlit as st

from utils import config as C

REQUIRED_COLS = [C.COL_DATE, C.COL_COUNTY, C.COL_CATEGORY, C.COL_OFFENCE, C.COL_VICTIMS]


@st.cache_data(show_spinner="Loading dataset...")
def load_data() -> pd.DataFrame:
    """Load and prepare the cleaned media-mining dataset.

    Returns an empty DataFrame (with an on-screen error) when the file is
    missing or malformed, so every page can simply ``st.stop()``.
    """
    if not os.path.exists(C.DATA_PATH):
        st.error(
            f"Dataset not found at `{C.DATA_PATH}`. Run `python data_cleaning.py` "
            "first, or place `cleaned_crime_data.csv` in the `data/` folder."
        )
        return pd.DataFrame()

    try:
        df = pd.read_csv(C.DATA_PATH, parse_dates=[C.COL_DATE])
    except (ValueError, pd.errors.ParserError) as exc:
        st.error(f"Could not parse the dataset: {exc}")
        return pd.DataFrame()

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        st.error(f"Dataset is missing required columns: {', '.join(missing)}")
        return pd.DataFrame()

    df = df.dropna(subset=[C.COL_DATE])
    df[C.COL_YEAR] = df[C.COL_DATE].dt.year
    df[C.COL_MONTH] = df[C.COL_DATE].dt.to_period("M").astype(str)

    for col in C.CATEGORICAL_COLS:
        if col in df.columns:
            df[col] = df[col].fillna(C.UNKNOWN).astype(str).str.strip()

    df[C.COL_VICTIMS] = (
        pd.to_numeric(df[C.COL_VICTIMS], errors="coerce").fillna(1).astype(int)
    )
    if C.COL_PERPS in df.columns:
        df[C.COL_PERPS] = pd.to_numeric(df[C.COL_PERPS], errors="coerce")
    else:
        df[C.COL_PERPS] = pd.NA

    return df.sort_values(C.COL_DATE).reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_geojson() -> dict | None:
    """Load the Kenya county boundaries GeoJSON (or None if unavailable)."""
    if not os.path.exists(C.GEOJSON_PATH):
        return None
    try:
        with open(C.GEOJSON_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None


@st.cache_data(show_spinner=False)
def load_logo_b64() -> str | None:
    """Return the NCRC logo as a base64 data URI, or None if unavailable."""
    import base64

    if not os.path.exists(C.LOGO_PATH):
        return None
    try:
        with open(C.LOGO_PATH, "rb") as fh:
            encoded = base64.b64encode(fh.read()).decode("ascii")
        return f"data:image/png;base64,{encoded}"
    except OSError:
        return None
