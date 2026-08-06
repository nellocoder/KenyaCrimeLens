"""Offence Analysis: categories, specific offences, weapons and motives."""

import streamlit as st

st.set_page_config(page_title="Offence Analysis · Kenya CrimeLens", page_icon="📂",
                   layout="wide")

from utils import charts
from utils import config as C
from utils.analytics import top_n
from utils.filters import active_filters, get_filtered, render_sidebar
from utils.loader import load_data
from utils.theme import (apply_theme, chart_card, filter_chips, info_banner,
                         kpi_cards, page_header)

apply_theme()
df = load_data()
if df.empty:
    st.stop()
render_sidebar(df)

page_header("📂", "Offence Analysis",
            "What kinds of crimes dominate, and the weapons and motives behind them")

res = get_filtered(df)
if res is None:
    info_banner()
    st.stop()
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

filter_chips(active_filters())

top_cat = res[C.COL_CATEGORY].value_counts().head(1)
top_off = top_n(res[C.COL_OFFENCE], 1)
top_weapon = top_n(res[C.COL_WEAPON], 1)
top_motive = top_n(res[C.COL_MOTIVE], 1)

kpi_cards([
    {"icon": "📂", "label": "Offence categories",
     "value": f"{res[C.COL_CATEGORY].nunique()}",
     "sub": f"{res[C.COL_OFFENCE].nunique()} distinct offences"},
    {"icon": "🥇", "label": "Top category",
     "value": top_cat.index[0] if len(top_cat) else "—",
     "sub": (f"{top_cat.iloc[0]} incidents · "
             f"{top_cat.iloc[0] / len(res) * 100:.0f}% of query") if len(top_cat) else ""},
    {"icon": "🔪", "label": "Most common weapon",
     "value": top_weapon.index[0] if len(top_weapon) else "—",
     "sub": f"{top_weapon.iloc[0]} cases" if len(top_weapon) else "not recorded"},
    {"icon": "🎯", "label": "Leading motive",
     "value": top_motive.index[0] if len(top_motive) else "—",
     "sub": f"{top_motive.iloc[0]} cases" if len(top_motive) else "not recorded"},
])

c1, c2 = st.columns(2)
with c1:
    chart_card("Incidents by offence category", charts.category_bar(res), height=460)
with c2:
    offences = res[res[C.COL_OFFENCE] != C.UNKNOWN][C.COL_OFFENCE].value_counts().head(15)
    chart_card("Top 15 specific offences",
               charts.generic_barh(offences.sort_values(), color="#4f46e5",
                                   unit="incidents"), height=460)

chart_card("Offence category structure (category → offence)",
           charts.treemap(res, [C.COL_CATEGORY, C.COL_OFFENCE]), height=520)

c3, c4 = st.columns(2)
with c3:
    weapons = res[res[C.COL_WEAPON] != C.UNKNOWN][C.COL_WEAPON].value_counts().head(12)
    chart_card("Weapons used (where recorded)",
               charts.generic_barh(weapons.sort_values(), color="#ea580c",
                                   unit="cases"), height=420)
with c4:
    motives = res[res[C.COL_MOTIVE] != C.UNKNOWN][C.COL_MOTIVE].value_counts().head(12)
    chart_card("Recorded motives",
               charts.generic_barh(motives.sort_values(), color="#0d9488",
                                   unit="cases"), height=420)

chart_card("Monthly trend for this selection", charts.monthly_trend_with_ma(res),
           height=300, caption="Dotted line: 3-month moving average")

st.subheader("Category detail")
detail = (res.groupby(C.COL_CATEGORY)
          .agg(Incidents=(C.COL_CATEGORY, "size"),
               Victims=(C.COL_VICTIMS, "sum"),
               **{"Victims / incident": (C.COL_VICTIMS, "mean")},
               **{"Top offence": (C.COL_OFFENCE,
                                  lambda s: s.value_counts().index[0])})
          .sort_values("Incidents", ascending=False).reset_index())
detail["Victims / incident"] = detail["Victims / incident"].round(2)
st.dataframe(detail, use_container_width=True, hide_index=True)
