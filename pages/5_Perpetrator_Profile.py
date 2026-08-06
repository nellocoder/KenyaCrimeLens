"""Perpetrator Profile: gender, numbers and patterns of recorded perpetrators."""

import streamlit as st

st.set_page_config(page_title="Perpetrator Profile · Kenya CrimeLens", page_icon="🕵️", layout="wide")

from utils.loader import load_data
from utils.theme import apply_theme, page_header, kpi_cards, chart_card, info_banner
from utils.filters import render_sidebar, get_filtered
from utils import charts

apply_theme()
df = load_data()
render_sidebar(df)

page_header("🕵️", "Perpetrator Profile Analysis",
            "Recorded perpetrator counts, gender and the offences they are linked to")

res = get_filtered(df)
if res is None:
    info_banner()
    st.stop()
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

recorded = res[res["Perpetrator Tally"].notna()]
perps = int(res["Perpetrator Tally"].sum())
pg = res[res["Perpetrator Gender"] != "Unknown"]["Perpetrator Gender"].value_counts()
largest = res.nlargest(1, "Perpetrator Tally").iloc[0]

kpi_cards([
    {"icon": "🕵️", "label": "Recorded perpetrators", "value": f"{perps:,}",
     "sub": f"{len(recorded):,} incidents have a count"},
    {"icon": "📊", "label": "Avg per incident",
     "value": f"{recorded['Perpetrator Tally'].mean():.1f}" if len(recorded) else "—",
     "sub": "where recorded"},
    {"icon": "🚻", "label": "Dominant gender", "value": pg.index[0] if len(pg) else "—",
     "sub": f"{pg.iloc[0]} incidents" if len(pg) else ""},
    {"icon": "👥", "label": "Largest group",
     "value": f"{int(largest['Perpetrator Tally']):,}" if recorded.shape[0] else "—",
     "sub": f"{largest['Offence']} · {largest['County']}" if recorded.shape[0] else ""},
])

st.caption(
    "Note: perpetrator details are only available where the media report named or "
    "counted suspects; many incidents have no perpetrator information recorded."
)

c1, c2 = st.columns(2)
with c1:
    chart_card("Perpetrator gender distribution",
               charts.donut(res["Perpetrator Gender"].value_counts()), height=400)
with c2:
    if len(recorded):
        dist = recorded["Perpetrator Tally"].clip(upper=20).value_counts().sort_index()
        chart_card("Perpetrators per incident (capped at 20)",
                   charts.generic_bar(dist, color="#ea580c", unit="incidents"), height=400)

gp = (res.groupby("Offence Category")["Perpetrator Tally"].sum()
      .dropna().sort_values())
chart_card("Recorded perpetrators by offence category",
           charts.generic_barh(gp, color="#dc2626", unit="perpetrators"), height=480)

st.subheader("Incidents with the most recorded perpetrators")
cols = ["Date", "County", "Offence Category", "Offence", "Perpetrator Tally",
        "Perpetrator Gender", "Case Summary"]
st.dataframe(res.nlargest(20, "Perpetrator Tally")[cols],
             use_container_width=True, hide_index=True)
