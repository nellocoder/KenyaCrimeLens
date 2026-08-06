"""
Kenya CrimeLens - landing page (national overview).
Run:  streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Kenya CrimeLens",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.loader import load_data
from utils.theme import apply_theme, page_header, kpi_cards, chart_card
from utils.filters import render_sidebar
from utils import charts

apply_theme()
df = load_data()
if df.empty:
    st.stop()

render_sidebar(df)

page_header(
    "🔍", "Kenya CrimeLens",
    "Interactive analysis of media-mined crime incidents across Kenya · "
    "Cumulative dataset 2025–2026",
)

st.info(
    "👈 Use the **sidebar query panel** to filter by year, county, offence "
    "category, victim gender, weapon or motive, then click **Analyze**. "
    "Navigate between analytical modules using the page menu above the filters. "
    "The overview below covers the full dataset.",
    icon="💡",
)

# ---------------------------------------------------------------------------
# National overview (always unfiltered)
# ---------------------------------------------------------------------------
victims = int(df["Victim Tally"].sum())
perps = int(df["Perpetrator Tally"].sum())
top_county = df[df["County"] != "Unknown"]["County"].value_counts().head(1)
top_cat = df["Offence Category"].value_counts().head(1)

kpi_cards([
    {"icon": "📈", "label": "Incidents", "value": f"{len(df):,}",
     "sub": f"{df['County'].nunique()} counties affected"},
    {"icon": "👥", "label": "Victims", "value": f"{victims:,}",
     "sub": f"{perps:,} recorded perpetrators"},
    {"icon": "📍", "label": "Top County", "value": top_county.index[0],
     "sub": f"{top_county.iloc[0]} incidents"},
    {"icon": "📂", "label": "Top Category", "value": top_cat.index[0],
     "sub": f"{top_cat.iloc[0]} incidents"},
])

chart_card("Monthly incident trend (full dataset)", charts.monthly_trend(df), height=300)

c1, c2 = st.columns(2)
with c1:
    chart_card("Incidents by offence category", charts.category_bar(df), height=480)
with c2:
    chart_card("Top counties by incidents", charts.top_counties_bar(df), height=480)

st.divider()
st.caption(
    "Built from the Cumulative Media Mining Dataset 2025–2026. Media-reported "
    "incidents only; figures are indicative and not official crime statistics."
)
