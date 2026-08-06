"""Dashboard: executive overview of the current query with auto narrative."""

import streamlit as st

st.set_page_config(page_title="Dashboard · Kenya CrimeLens", page_icon="📊",
                   layout="wide")

from utils import charts, export
from utils.analytics import build_summary, county_scoreboard, kpis
from utils.filters import active_filters, get_filtered, render_sidebar
from utils.loader import load_data
from utils.theme import (apply_theme, chart_card, filter_chips, info_banner,
                         kpi_cards, page_header, summary_box)

apply_theme()
df = load_data()
if df.empty:
    st.stop()
render_sidebar(df)

page_header("📊", "Dashboard",
            "Executive overview of the current query with an automatic analyst briefing")

res = get_filtered(df)
if res is None:
    info_banner()
    st.stop()
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

f = active_filters() or {}
filter_chips(f)

cards = kpis(res)
kpi_cards(cards)

summary_html = build_summary(res, f)
summary_box(summary_html)

chart_card("Monthly incident trend", charts.monthly_trend_with_ma(res),
           height=320, caption="Dotted line: 3-month moving average")

c1, c2 = st.columns(2)
with c1:
    chart_card("Incidents by offence category", charts.category_bar(res), height=440)
with c2:
    chart_card("Top counties by incidents", charts.top_counties_bar(res, n=12),
               height=440)

c3, c4 = st.columns(2)
with c3:
    chart_card("Victim toll by offence category", charts.victims_by_category(res),
               height=420)
with c4:
    chart_card("Monthly victim toll", charts.monthly_trend(res, value="victims"),
               height=420)

# ---------------------------------------------------------------------------
# One-click PDF briefing
# ---------------------------------------------------------------------------
st.subheader("Export briefing")
scoreboard = county_scoreboard(res)
pdf = export.to_pdf_bytes("Query briefing", summary_html, cards, scoreboard)
if pdf is not None:
    st.download_button("⬇ Download PDF briefing", data=pdf,
                       file_name="kenya_crimelens_briefing.pdf",
                       mime="application/pdf")
else:
    st.caption("Install `reportlab` to enable the PDF briefing export.")
