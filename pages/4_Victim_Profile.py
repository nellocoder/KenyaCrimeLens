"""Victim Profile: gender distribution, victim toll by category and over time."""

import streamlit as st

st.set_page_config(page_title="Victim Profile · Kenya CrimeLens", page_icon="👥", layout="wide")

from utils.loader import load_data
from utils.theme import apply_theme, page_header, kpi_cards, chart_card, info_banner
from utils.filters import render_sidebar, get_filtered
from utils import charts

apply_theme()
df = load_data()
render_sidebar(df)

page_header("👥", "Victim Profile Analysis",
            "Who the victims are and which crimes carry the heaviest human toll")

res = get_filtered(df)
if res is None:
    info_banner()
    st.stop()
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

victims = int(res["Victim Tally"].sum())
gender = res["Victim Gender"].value_counts()
worst = res.nlargest(1, "Victim Tally").iloc[0]

kpi_cards([
    {"icon": "👥", "label": "Total victims", "value": f"{victims:,}",
     "sub": f"avg {victims / len(res):.1f} per incident"},
    {"icon": "🚻", "label": "Largest group", "value": gender.index[0],
     "sub": f"{gender.iloc[0]} incidents"},
    {"icon": "⚠️", "label": "Deadliest single incident",
     "value": f"{int(worst['Victim Tally']):,} victims",
     "sub": f"{worst['Offence']} · {worst['County']} · {worst['Date']:%Y-%m-%d}"},
    {"icon": "📈", "label": "Incidents analysed", "value": f"{len(res):,}",
     "sub": "current query"},
])

c1, c2 = st.columns(2)
with c1:
    chart_card("Victim gender distribution (incidents)",
               charts.donut(gender), height=400)
with c2:
    gv = res.groupby("Victim Gender")["Victim Tally"].sum().sort_values(ascending=False)
    chart_card("Victim gender distribution (victim toll)",
               charts.donut(gv, colors=["#2563eb", "#db2777", "#7c3aed", "#d97706", "#64748b"]),
               height=400)

chart_card("Victim toll by offence category", charts.victims_by_category(res), height=480)
chart_card("Monthly victim toll", charts.monthly_trend(res, value="victims"), height=300)

st.subheader("Incidents with the highest victim counts")
cols = ["Date", "County", "Offence Category", "Offence", "Victim Tally", "Motive", "Case Summary"]
st.dataframe(res.nlargest(20, "Victim Tally")[cols],
             use_container_width=True, hide_index=True)
