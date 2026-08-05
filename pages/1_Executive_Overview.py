"""Executive Overview: filtered key metrics and findings."""

import streamlit as st

st.set_page_config(page_title="Executive Overview · Kenya CrimeLens", page_icon="📊", layout="wide")

from utils.loader import load_data
from utils.theme import apply_theme, page_header, kpi_cards, chart_card, summary_box, info_banner
from utils.filters import render_sidebar, get_filtered, active_filters
from utils.analytics import kpis, build_summary
from utils import charts

apply_theme()
df = load_data()
render_sidebar(df)

page_header("📊", "Executive Overview",
            "Key findings and critical metrics for your current query")

res = get_filtered(df)
if res is None:
    info_banner()
    st.stop()
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

filters = active_filters() or {}
kpi_cards(kpis(res))
summary_box(build_summary(res, filters))

# Trend with MA
chart_card("Monthly incident trend with 3‑month moving average",
           charts.monthly_trend_with_ma(res, value="incidents", window=3),
           height=320)

c1, c2 = st.columns(2)
with c1:
    chart_card("Crime composition", charts.category_bar(res), height=400)
with c2:
    chart_card("Top counties", charts.top_counties_bar(res), height=400)

# Area requiring attention: biggest change (if we had previous period)
st.caption("Note: quarter‑on‑quarter change will be available in a future update.")
