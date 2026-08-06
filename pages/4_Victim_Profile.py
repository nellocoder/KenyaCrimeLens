"""Victim Profile: gender distribution, victim toll by category and over time."""

import streamlit as st

st.set_page_config(page_title="Victim Profile · Kenya CrimeLens", page_icon="👥",
                   layout="wide")

from utils import charts
from utils import config as C
from utils.filters import active_filters, get_filtered, render_sidebar
from utils.loader import load_data
from utils.theme import (apply_theme, chart_card, filter_chips, info_banner,
                         kpi_cards, page_header, styled_table)

apply_theme()
df = load_data()
if df.empty:
    st.stop()
render_sidebar(df)

page_header("👥", "Victim Profile Analysis",
            "Who the victims are and which crimes carry the heaviest human toll")

res = get_filtered(df)
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

filter_chips(active_filters(df))

victims = int(res[C.COL_VICTIMS].sum())
gender = res[C.COL_VICTIM_GENDER].value_counts()
worst = res.nlargest(1, C.COL_VICTIMS).iloc[0]

kpi_cards([
    {"icon": "👥", "label": "Total victims", "value": f"{victims:,}",
     "sub": f"avg {victims / len(res):.1f} per incident"},
    {"icon": "🚻", "label": "Largest group", "value": gender.index[0],
     "sub": f"{gender.iloc[0]} incidents"},
    {"icon": "⚠️", "label": "Deadliest single incident",
     "value": f"{int(worst[C.COL_VICTIMS]):,} victims",
     "sub": f"{worst[C.COL_OFFENCE]} · {worst[C.COL_COUNTY]} · "
            f"{worst[C.COL_DATE]:%Y-%m-%d}"},
    {"icon": "📈", "label": "Incidents analysed", "value": f"{len(res):,}",
     "sub": "current query"},
])

c1, c2 = st.columns(2)
with c1:
    chart_card("Victim gender distribution (incidents)", charts.donut(gender),
               height=400)
with c2:
    gv = (res.groupby(C.COL_VICTIM_GENDER)[C.COL_VICTIMS].sum()
          .sort_values(ascending=False))
    chart_card("Victim gender distribution (victim toll)",
               charts.donut(gv, colors=["#2563eb", "#db2777", "#7c3aed",
                                        "#d97706", "#64748b"]),
               height=400)

chart_card("Victim toll by offence category", charts.victims_by_category(res),
           height=480)
chart_card("Monthly victim toll", charts.monthly_trend(res, value="victims"),
           height=300)

st.subheader("Incidents with the highest victim counts")
cols = [C.COL_DATE, C.COL_COUNTY, C.COL_CATEGORY, C.COL_OFFENCE, C.COL_VICTIMS,
        C.COL_MOTIVE, C.COL_SUMMARY]
cat_colors = charts.category_colors(res[C.COL_CATEGORY].unique())
styled_table(
    res.nlargest(20, C.COL_VICTIMS)[cols].rename(columns={C.COL_VICTIMS: "Victims"}),
    pill_columns={C.COL_CATEGORY: cat_colors},
    strong_columns=(C.COL_OFFENCE,),
    numeric_columns=("Victims",),
    muted_columns=(C.COL_MOTIVE, C.COL_SUMMARY),
    date_columns=(C.COL_DATE,),
)
