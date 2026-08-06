"""Spatial Analysis: choropleth and bubble views of incidents across Kenya."""

import streamlit as st

st.set_page_config(page_title="Spatial Analysis · Kenya CrimeLens", page_icon="🗺️",
                   layout="wide")

from utils import charts
from utils import config as C
from utils.filters import active_filters, get_filtered, render_sidebar
from utils.loader import load_data, load_geojson
from utils.theme import (apply_theme, chart_card, filter_chips, info_banner,
                         kpi_cards, page_header)

apply_theme()
df = load_data()
if df.empty:
    st.stop()
render_sidebar(df)

page_header("🗺️", "Spatial Analysis",
            "County-level geography of incidents: choropleth density and bubble volume")

res = get_filtered(df)
if res is None:
    info_banner()
    st.stop()
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

filter_chips(active_filters())

mapped = res[res[C.COL_COUNTY].isin(charts.COUNTY_COORDS)]
coverage = len(mapped) / len(res) * 100 if len(res) else 0
total_victims_national = df[C.COL_VICTIMS].sum()
mapped_victims = mapped[C.COL_VICTIMS].sum()
national_share = (mapped_victims / total_victims_national * 100
                  if total_victims_national else 0)

kpi_cards([
    {"icon": "🗺️", "label": "Mapped incidents", "value": f"{len(mapped):,}",
     "sub": f"{coverage:.0f}% of the current query"},
    {"icon": "📍", "label": "Counties mapped",
     "value": f"{mapped[C.COL_COUNTY].nunique()}", "sub": "of Kenya's 47 counties"},
    {"icon": "👥", "label": "Mapped victims", "value": f"{int(mapped_victims):,}",
     "sub": f"{national_share:.1f}% of all victims"},
    {"icon": "🧭", "label": "Unmapped records", "value": f"{len(res) - len(mapped):,}",
     "sub": "Unknown / multiple / outside Kenya"},
])

# ---- Map controls ----
col1, col2 = st.columns([2, 1])
with col1:
    metric_label = st.radio(
        "Map metric",
        ["Incidents", "Victims", "Severity (avg victims per incident)"],
        horizontal=True, index=0, key="map_metric",
    )
with col2:
    map_type = st.selectbox("Map style", ["Choropleth", "Bubbles"], index=0,
                            key="map_type")

metric = {"Incidents": "incidents", "Victims": "victims"}.get(metric_label,
                                                              "severity")

with st.spinner("Rendering map..."):
    if map_type == "Choropleth":
        fig_map = charts.county_choropleth(res, metric=metric)
        if fig_map is None:
            st.warning("County GeoJSON not found in `assets/`; showing bubble map.")
            fig_map = charts.county_map(res, metric=metric)
    else:
        fig_map = charts.county_map(res, metric=metric)

chart_card("Incident map of Kenya", fig_map, height=560,
           caption="Hover a county for incidents, victims, rank and its top offence category")

# ---- County ranking ----
with st.expander("County ranking for the selected metric", expanded=False):
    rank = (mapped.groupby(C.COL_COUNTY)
            .agg(Incidents=(C.COL_COUNTY, "size"),
                 Victims=(C.COL_VICTIMS, "sum"))
            .reset_index())
    rank["Avg victims / incident"] = (rank["Victims"] / rank["Incidents"]).round(2)
    sort_col = {"incidents": "Incidents", "victims": "Victims",
                "severity": "Avg victims / incident"}[metric]
    rank = rank.sort_values(sort_col, ascending=False).reset_index(drop=True)
    rank.insert(0, "Rank", rank.index + 1)
    st.dataframe(rank, use_container_width=True, hide_index=True)

# ---- Bottom charts ----
c1, c2 = st.columns(2)
with c1:
    top_incidents = mapped[C.COL_COUNTY].value_counts().head(15)
    chart_card("Top counties by incidents (mapped)",
               charts.generic_bar(top_incidents, color="#2563eb",
                                  unit="incidents"), height=400)
with c2:
    victims_series = (mapped.groupby(C.COL_COUNTY)[C.COL_VICTIMS].sum()
                      .sort_values(ascending=False).head(15))
    chart_card("Top counties by victim toll",
               charts.generic_barh(victims_series.sort_values(), color="#0d9488",
                                   unit="victims"), height=400)

c3, c4 = st.columns(2)
with c3:
    chart_card("Avg victims per incident · by county (mapped)",
               charts.avg_victims_per_incident(mapped, group_col=C.COL_COUNTY,
                                               top_n=10), height=400)
with c4:
    chart_card("Avg victims per incident · by offence category",
               charts.avg_victims_per_incident(res, group_col=C.COL_CATEGORY,
                                               top_n=10), height=400)

st.caption(
    "Counties with 'Unknown', 'Multiple Counties', 'Nationwide' or 'Outside Kenya' "
    "cannot be placed on the map. Severity is only computed for counties with at "
    f"least {C.MIN_INCIDENTS_FOR_RATIO} incidents."
)
