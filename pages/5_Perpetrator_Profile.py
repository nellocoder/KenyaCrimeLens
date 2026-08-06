"""Perpetrator Profile: gender, numbers and patterns of recorded perpetrators."""

import streamlit as st

st.set_page_config(page_title="Perpetrator Profile · Kenya CrimeLens",
                   page_icon="🕵️", layout="wide")

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

page_header("🕵️", "Perpetrator Profile Analysis",
            "Recorded perpetrator counts, gender and the offences they are linked to")

res = get_filtered(df)
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

filter_chips(active_filters(df))

recorded = res[res[C.COL_PERPS].notna()]
perps = int(res[C.COL_PERPS].sum(skipna=True) or 0)
pg = res[res[C.COL_PERP_GENDER] != C.UNKNOWN][C.COL_PERP_GENDER].value_counts()
has_counts = len(recorded) > 0
largest = recorded.nlargest(1, C.COL_PERPS).iloc[0] if has_counts else None

kpi_cards([
    {"icon": "🕵️", "label": "Recorded perpetrators", "value": f"{perps:,}",
     "sub": f"{len(recorded):,} incidents have a count"},
    {"icon": "📊", "label": "Avg per incident",
     "value": f"{recorded[C.COL_PERPS].mean():.1f}" if has_counts else "—",
     "sub": "where recorded"},
    {"icon": "🚻", "label": "Dominant gender",
     "value": pg.index[0] if len(pg) else "—",
     "sub": f"{pg.iloc[0]} incidents" if len(pg) else ""},
    {"icon": "👥", "label": "Largest group",
     "value": f"{int(largest[C.COL_PERPS]):,}" if has_counts else "—",
     "sub": (f"{largest[C.COL_OFFENCE]} · {largest[C.COL_COUNTY]}"
             if has_counts else "")},
])

st.caption(
    "Note: perpetrator details are only available where the media report named or "
    "counted suspects; many incidents have no perpetrator information recorded."
)

c1, c2 = st.columns(2)
with c1:
    chart_card("Perpetrator gender distribution",
               charts.donut(res[C.COL_PERP_GENDER].value_counts()), height=400)
with c2:
    if has_counts:
        dist = recorded[C.COL_PERPS].clip(upper=20).value_counts().sort_index()
        chart_card("Perpetrators per incident (capped at 20)",
                   charts.generic_bar(dist, color="#ea580c", unit="incidents"),
                   height=400)
    else:
        st.info("No incidents in this query carry a perpetrator count.")

gp = (res.groupby(C.COL_CATEGORY)[C.COL_PERPS].sum().dropna().sort_values())
chart_card("Recorded perpetrators by offence category",
           charts.generic_barh(gp, color="#dc2626", unit="perpetrators"), height=480)

st.subheader("Incidents with the most recorded perpetrators")
cols = [C.COL_DATE, C.COL_COUNTY, C.COL_CATEGORY, C.COL_OFFENCE, C.COL_PERPS,
        C.COL_PERP_GENDER, C.COL_SUMMARY]
cat_colors = charts.category_colors(res[C.COL_CATEGORY].unique())
styled_table(
    recorded.nlargest(20, C.COL_PERPS)[cols].rename(
        columns={C.COL_PERPS: "Perpetrators"}),
    pill_columns={C.COL_CATEGORY: cat_colors},
    strong_columns=(C.COL_OFFENCE,),
    numeric_columns=("Perpetrators",),
    muted_columns=(C.COL_PERP_GENDER, C.COL_SUMMARY),
    truncate_columns={C.COL_SUMMARY: 90},
    date_columns=(C.COL_DATE,),
)
