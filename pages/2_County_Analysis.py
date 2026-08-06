"""County Analysis: geographic distribution and county x category structure."""

import streamlit as st

st.set_page_config(page_title="County Analysis · Kenya CrimeLens", page_icon="📍",
                   layout="wide")

from utils import charts
from utils import config as C
from utils.analytics import county_scoreboard
from utils.filters import active_filters, get_filtered, render_sidebar
from utils.loader import load_data
from utils.theme import (apply_theme, chart_card, filter_chips, info_banner,
                         kpi_cards, page_header, styled_table)

apply_theme()
df = load_data()
if df.empty:
    st.stop()
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

filter_chips(active_filters())

known = res[res[C.COL_COUNTY] != C.UNKNOWN]
top = known[C.COL_COUNTY].value_counts().head(1)
kpi_cards([
    {"icon": "🗺️", "label": "Counties affected", "value": f"{known[C.COL_COUNTY].nunique()}",
     "sub": f"{len(res) - len(known)} records with unknown county"},
    {"icon": "📍", "label": "Leading county",
     "value": top.index[0] if len(top) else "—",
     "sub": f"{top.iloc[0]} incidents" if len(top) else ""},
    {"icon": "👥", "label": "Victims in leading county",
     "value": (f"{int(known[known[C.COL_COUNTY] == top.index[0]][C.COL_VICTIMS].sum()):,}"
               if len(top) else "—"),
     "sub": "media-reported"},
    {"icon": "📂", "label": "Leading category there",
     "value": (known[known[C.COL_COUNTY] == top.index[0]][C.COL_CATEGORY]
               .value_counts().index[0] if len(top) else "—"),
     "sub": "most frequent offence group"},
])

c1, c2 = st.columns(2)
with c1:
    chart_card("Top 15 counties by incidents", charts.top_counties_bar(res, n=15),
               height=430)
with c2:
    chart_card("Top 10 counties by offence category",
               charts.stacked_county_category(res, n_counties=10), height=430)

chart_card("Top 10 counties · offence category mix",
           charts.county_category_heatmap(res, n_counties=10, n_categories=8),
           height=520,
           caption="Each cell shows a category's share of that county's incidents — "
                   "darker means a larger share")

chart_card("County vs offence category breakdown",
           charts.treemap(known, [C.COL_COUNTY, C.COL_CATEGORY]), height=520)

c3, c4 = st.columns(2)
with c3:
    chart_card("Avg victims per incident · by county",
               charts.avg_victims_per_incident(res, group_col=C.COL_COUNTY, top_n=10),
               height=400,
               caption=f"Counties with at least {C.MIN_INCIDENTS_FOR_RATIO} incidents")
with c4:
    chart_card("Avg victims per incident · by offence category",
               charts.avg_victims_per_incident(res, group_col=C.COL_CATEGORY, top_n=10),
               height=400,
               caption=f"Categories with at least {C.MIN_INCIDENTS_FOR_RATIO} incidents")

st.subheader("County scoreboard")
tbl = county_scoreboard(res)
cat_colors = charts.category_colors(res[C.COL_CATEGORY].unique())
styled_table(
    tbl,
    pill_columns={"Top Category": cat_colors},
    strong_columns=("County",),
    numeric_columns=("Incidents", "Victims", "Perpetrators", "% of incidents",
                     "% of victims", "Victims / incident"),
)
