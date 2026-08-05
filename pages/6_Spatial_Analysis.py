"""Spatial Analysis: incident and victim bubbles over the map of Kenya."""

import streamlit as st

st.set_page_config(page_title="Spatial Analysis · Kenya CrimeLens", page_icon="🗺️", layout="wide")

from utils.loader import load_data
from utils.theme import apply_theme, page_header, kpi_cards, chart_card, info_banner
from utils.filters import render_sidebar, get_filtered
from utils import charts

apply_theme()
df = load_data()
render_sidebar(df)

page_header("🗺️", "Spatial Analysis",
            "Bubble size shows incidents per county; colour intensity shows the selected metric")

res = get_filtered(df)
if res is None:
    info_banner()
    st.stop()
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

mapped = res[res["County"].isin(charts.COUNTY_COORDS)]
coverage = len(mapped) / len(res) * 100 if len(res) else 0

# National total victims (unfiltered) for baseline share
total_victims_national = df["Victim Tally"].sum()
mapped_victims = mapped["Victim Tally"].sum()
national_share = (mapped_victims / total_victims_national * 100) if total_victims_national else 0

# ---- KPI cards ----
kpi_cards([
    {"icon": "🗺️", "label": "Mapped incidents", "value": f"{len(mapped):,}",
     "sub": f"{coverage:.0f}% of the current query"},
    {"icon": "📍", "label": "Counties mapped", "value": f"{mapped['County'].nunique()}",
     "sub": "of Kenya's 47 counties"},
    {"icon": "👥", "label": "Mapped victims", "value": f"{int(mapped_victims):,}",
     "sub": f"{national_share:.1f}% of all victims"},
    {"icon": "🧭", "label": "Unmapped records", "value": f"{len(res) - len(mapped):,}",
     "sub": "Unknown / multiple / outside Kenya"},
])

# ---- Map controls ----
col1, col2 = st.columns([2, 1])
with col1:
    map_metric = st.radio(
        "Map colour & size metric:",
        ["incidents", "victims", "severity (avg victims per incident)"],
        horizontal=True,
        index=0,
        key="map_metric"
    )
with col2:
    map_type = st.selectbox(
        "Map style",
        ["Bubbles", "Choropleth (coming soon)"],
        index=0,
        key="map_type"
    )

# ---- Map ----
with st.container():
    if map_type == "Bubbles":
        if map_metric == "severity (avg victims per incident)":
            fig_map = charts.county_map(res, metric="severity")
        else:
            fig_map = charts.county_map(res, metric=map_metric)
        chart_card("Incident map of Kenya", fig_map, height=560)
    else:
        st.warning("Choropleth requires county GeoJSON. Using bubble map instead.")
        fig_map = charts.county_map(res, metric=map_metric.split(" ")[0] if "severity" not in map_metric else "severity")
        chart_card("Incident map of Kenya (bubble fallback)", fig_map, height=560)

# ---- Bottom charts ----
c1, c2 = st.columns(2)
with c1:
    top_incidents = mapped["County"].value_counts().head(15)
    chart_card("Top counties by incidents (mapped)",
               charts.generic_bar(top_incidents, color="#2563eb", unit="incidents"), height=400)
with c2:
    victims_series = mapped.groupby("County")["Victim Tally"].sum().sort_values(ascending=False).head(15)
    chart_card("Top counties by victim toll",
               charts.generic_barh(victims_series, color="#0d9488", unit="victims"), height=400)

# ----- Victim‑per‑incident ratio charts -----
c3, c4 = st.columns(2)
with c3:
    chart_card("Avg victims per incident – by county (mapped)",
               charts.avg_victims_per_incident(mapped, group_col="County", top_n=10),
               height=400)
with c4:
    chart_card("Avg victims per incident – by offence category",
               charts.avg_victims_per_incident(res, group_col="Offence Category", top_n=10),
               height=400)

st.caption(
    "Counties with 'Unknown', 'Multiple Counties', 'Nationwide' or 'Outside Kenya' "
    "cannot be placed on the map. County centroids are approximate. "
    "Bubble size always reflects incident count; colour follows the selected metric."
)
