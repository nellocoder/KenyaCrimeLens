"""Kenya CrimeLens - landing page (national overview).

Run:  streamlit run Home.py
"""

import os

import streamlit as st

try:
    from PIL import Image
    _icon = Image.open(os.path.join("assets", "logo_ncrc.png"))
except Exception:  # noqa: BLE001 - fall back to emoji if logo/PIL unavailable
    _icon = "🔍"

st.set_page_config(
    page_title="Kenya CrimeLens · NCRC",
    page_icon=_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils import charts
from utils import config as C
from utils.filters import render_sidebar
from utils.loader import load_data, load_logo_b64
from utils.theme import (apply_theme, chart_card, kpi_cards, org_banner,
                         page_header)

apply_theme()
df = load_data()
if df.empty:
    st.stop()

render_sidebar(df)

org_banner(load_logo_b64())

page_header(
    "🔍", "Kenya CrimeLens",
    "Interactive analysis of media-mined crime incidents across Kenya · "
    "Cumulative dataset 2025–2026",
)

st.info(
    "Every page loads with the full national overview by default. To narrow it, "
    "use the **sidebar query panel** to filter by year, county, offence category, "
    "victim gender, weapon or motive, then click **Analyze**. Navigate between "
    "analytical modules using the menu.",
    icon="💡",
)

# ---------------------------------------------------------------------------
# National overview (always unfiltered)
# ---------------------------------------------------------------------------
victims = int(df[C.COL_VICTIMS].sum())
perps = int(df[C.COL_PERPS].sum(skipna=True) or 0)
top_county = df[df[C.COL_COUNTY] != C.UNKNOWN][C.COL_COUNTY].value_counts().head(1)
top_cat = df[C.COL_CATEGORY].value_counts().head(1)

kpi_cards([
    {"icon": "📈", "label": "Incidents", "value": f"{len(df):,}",
     "sub": f"{df[C.COL_COUNTY].nunique()} counties affected"},
    {"icon": "👥", "label": "Victims", "value": f"{victims:,}",
     "sub": f"{perps:,} recorded perpetrators"},
    {"icon": "📍", "label": "Top County", "value": top_county.index[0],
     "sub": f"{top_county.iloc[0]} incidents"},
    {"icon": "📂", "label": "Top Category", "value": top_cat.index[0],
     "sub": f"{top_cat.iloc[0]} incidents"},
])

chart_card("Monthly incident trend (full dataset)",
           charts.monthly_trend_with_ma(df), height=320,
           caption="Dotted line: 3-month moving average")

c1, c2 = st.columns(2)
with c1:
    chart_card("Incidents by offence category", charts.category_bar(df), height=480)
with c2:
    chart_card("Top counties by incidents", charts.top_counties_bar(df), height=480)

choropleth = charts.county_choropleth(df)
if choropleth is not None:
    chart_card("National incident density by county", choropleth, height=520,
               caption="Hover a county for incidents, victims, rank and top category")

st.divider()
st.caption(
    "Built from the Cumulative Media Mining Dataset 2025–2026. Media-reported "
    "incidents only; figures are indicative and not official crime statistics."
)
