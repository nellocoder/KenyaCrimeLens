"""County Analysis: geographic distribution and county x category structure."""

import streamlit as st

st.set_page_config(page_title="County Analysis · Kenya CrimeLens", page_icon="📍", layout="wide")

from utils.loader import load_data
from utils.theme import apply_theme, page_header, kpi_cards, chart_card, info_banner
from utils.filters import render_sidebar, get_filtered
from utils.analytics import top_n
from utils import charts

apply_theme()
df = load_data()
render_sidebar(df)

page_header("📍", "County Analysis",
            "Where incidents are concentrated and how offence patterns differ by county")

res = get_filtered(df)
if res is None:
    info_banner()
    st.stop()
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

known = res[res["County"] != "Unknown"]
top = known["County"].value_counts().head(1)
kpi_cards([
    {"icon": "🗺️", "label": "Counties affected", "value": f"{known['County'].nunique()}",
     "sub": f"{len(res) - len(known)} records with unknown county"},
    {"icon": "📍", "label": "Leading county", "value": top.index[0] if len(top) else "—",
     "sub": f"{top.iloc[0]} incidents" if len(top) else ""},
    {"icon": "👥", "label": "Victims in leading county",
     "value": f"{int(known[known['County'] == top.index[0]]['Victim Tally'].sum()):,}" if len(top) else "—",
     "sub": "media-reported"},
    {"icon": "📂", "label": "Leading category there",
     "value": (known[known["County"] == top.index[0]]["Offence Category"].value_counts().index[0]
               if len(top) else "—"),
     "sub": "most frequent offence group"},
])

c1, c2 = st.columns(2)
with c1:
    chart_card("Top 15 counties by incidents", charts.top_counties_bar(res, n=15), height=430)
with c2:
    chart_card("Top 10 counties by offence category",
               charts.stacked_county_category(res, n_counties=10), height=430)

chart_card("County vs offence category breakdown",
           charts.treemap(res[res["County"] != "Unknown"], ["County", "Offence Category"]),
           height=520)

st.subheader("County scoreboard")
tbl = (known.groupby("County")
       .agg(Incidents=("County", "size"), Victims=("Victim Tally", "sum"),
            Perpetrators=("Perpetrator Tally", "sum"),
            **{"Top Category": ("Offence Category", lambda s: s.value_counts().index[0])})
       .sort_values("Incidents", ascending=False).reset_index())
st.dataframe(tbl, use_container_width=True, hide_index=True)
