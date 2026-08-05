"""Dashboard: filtered overview with key metrics and trend."""

import streamlit as st

st.set_page_config(page_title="Dashboard · Kenya CrimeLens", page_icon="📊", layout="wide")

from utils.loader import load_data
from utils.theme import apply_theme, page_header, kpi_cards, chart_card, summary_box, info_banner
from utils.filters import render_sidebar, get_filtered, active_filters
from utils.analytics import kpis, build_summary
from utils import charts

apply_theme()
df = load_data()
render_sidebar(df)

page_header("📊", "Dashboard",
            "Key metrics and trend for your current query")

res = get_filtered(df)
if res is None:
    info_banner()
    st.stop()
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

# KPI cards
filters = active_filters() or {}
kpi_cards(kpis(res))

# Auto-generated summary
summary_box(build_summary(res, filters))

# Trend with moving average
chart_card("Monthly incident trend with 3‑month moving average",
           charts.monthly_trend_with_ma(res, value="incidents", window=3),
           height=320)

# Two key charts
c1, c2 = st.columns(2)
with c1:
    chart_card("Incidents by offence category", charts.category_bar(res), height=400)
with c2:
    chart_card("Top counties by incidents", charts.top_counties_bar(res), height=400)
