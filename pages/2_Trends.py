"""Crime Trends: incident patterns over time."""

import streamlit as st

st.set_page_config(page_title="Crime Trends · Kenya CrimeLens", page_icon="📈", layout="wide")

from utils.loader import load_data
from utils.theme import apply_theme, page_header, kpi_cards, chart_card, summary_box, info_banner
from utils.filters import render_sidebar, get_filtered
from utils import charts

apply_theme()
df = load_data()
render_sidebar(df)

page_header("📈", "Crime Trends",
            "How media‑reported incidents change over time")

res = get_filtered(df)
if res is None:
    info_banner()
    st.stop()
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

kpi_cards([
    {"icon": "📅", "label": "Time period",
     "value": f"{res['Date'].min():%Y-%m-%d} – {res['Date'].max():%Y-%m-%d}",
     "sub": f"{len(res)} incidents"},
    {"icon": "📊", "label": "Monthly average",
     "value": f"{len(res) / max(1, res['Month'].nunique()):.1f}",
     "sub": "incidents per month"},
    {"icon": "📈", "label": "Peak month",
     "value": res["Month"].value_counts().index[0],
     "sub": f"{res['Month'].value_counts().iloc[0]} incidents"},
    {"icon": "🔍", "label": "Victim count known",
     "value": f"{res['Victim Known'].sum()} of {len(res)}",
     "sub": "incidents with victim numbers"},
])

chart_card("Monthly incident trend with 3‑month moving average",
           charts.monthly_trend_with_ma(res, value="incidents", window=3), height=400)

c1, c2 = st.columns(2)
with c1:
    chart_card("Victim toll trend", charts.monthly_trend_with_ma(res, value="victims", window=3), height=350)
with c2:
    # Year-on-year (simplified: compare 2025 vs 2026, but data might be partial)
    y25 = len(res[res["Year"] == 2025])
    y26 = len(res[res["Year"] == 2026])
    if y25 > 0 and y26 > 0:
        change = (y26 - y25) / y25 * 100
        st.metric("2025 → 2026 incident count", y25, f"{y26} ({change:+.0f}%)")
    else:
        st.info("Year‑on‑year comparison not possible with current filter.")

st.caption("Moving average smooths monthly fluctuations to reveal underlying direction.")
