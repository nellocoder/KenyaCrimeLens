"""Data loading and caching for Kenya CrimeLens."""

import os
import pandas as pd
import streamlit as st

DATA_PATH = os.path.join("data", "cleaned_crime_data.csv")


@st.cache_data(show_spinner="Loading dataset...")
def load_data() -> pd.DataFrame:
    """Load the cleaned, categorized media-mining dataset (cached)."""
    if not os.path.exists(DATA_PATH):
        st.error(
            f"Dataset not found at `{DATA_PATH}`. Run `python data_cleaning.py` "
            "first, or place cleaned_crime_data.csv in the data/ folder."
        )
        return pd.DataFrame()

    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    for col in ["County", "Offence Category", "Offence", "Victim Gender",
                "Perpetrator Gender", "Weapon", "Motive", "Source"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    df["Victim Tally"] = pd.to_numeric(df["Victim Tally"], errors="coerce").fillna(1).astype(int)
    df["Perpetrator Tally"] = pd.to_numeric(df["Perpetrator Tally"], errors="coerce")

    return df.sort_values("Date")
