"""Geography & Maps: county-level distribution and rates."""

import streamlit as st

st.set_page_config(page_title="Geography & Maps · Kenya CrimeLens", page_icon="🗺️", layout="wide")

from utils.loader import load_data
from utils.theme import apply_theme, page_header, kpi_cards, chart_card, info_banner
from utils.filters import render_sidebar, get_filtered
from utils import charts
from utils.population import COUNTY_POPULATION

apply_theme()
df = load_data()
render_sidebar(df)

page_header("🗺️", "Geography & Maps",
            "Where media‑reported incidents are concentrated")

res = get_filtered(df)
if res is None:
    info_banner()
    st.stop()
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

mapped = res[res["County"].isin(charts.COUNTY_COORDS)]
coverage = len(mapped) / len(res) * 100 if len(res) else 0

query_total_victims = res["Victim Tally"].sum()
mapped_victims = mapped["Victim Tally"].sum()
mapped_share = (mapped_victims / query_total_victims * 100) if query_total_victims else 0

kpi_cards([
    {"icon": "🗺️", "label": "Mapped incidents", "value": f"{len(mapped):,}",
     "sub": f"{coverage:.0f}% of selection"},
    {"icon": "📍", "label": "Counties mapped", "value": f"{mapped['County'].nunique()}",
     "sub": "of Kenya's 47 counties"},
    {"icon": "👥", "label": "Mapped victims", "value": f"{int(mapped_victims):,}",
     "sub": f"{mapped_share:.1f}% of victims in selection"},
    {"icon": "🧭", "label": "Unmapped records", "value": f"{len(res) - len(mapped):,}",
     "sub": "Unknown / multiple / outside Kenya"},
])

# Map controls
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    map_metric = st.radio("Map metric:",
                          ["Incidents", "Victims", "Avg victims per incident"],
                          horizontal=True, index=0)
with col2:
    show_rate = st.checkbox("Show rate (per 100k)", value=False) if map_metric == "Incidents" else False
with col3:
    # Placeholder for choropleth toggle (future)
    st.caption("Bubble map")

metric_key = {"Incidents": "incidents", "Victims": "victims", "Avg victims per incident": "avg_victims"}[map_metric]
fig_map = charts.county_map(res, metric=metric_key, rate=show_rate)
chart_card("Incident distribution across Kenya", fig_map, height=560)

# County ranking with rates
c1, c2 = st.columns(2)
with c1:
    top_inc = mapped["County"].value_counts().head(15)
    chart_card("Top counties by incident count",
               charts.generic_bar(top_inc, color="#2563eb", unit="incidents"), height=400)
with c2:
    # Rates
    if len(mapped) > 0:
        rate_data = []
        for county, count in mapped["County"].value_counts().items():
            rate = charts.crime_rate(count, county)  # need to import crime_rate
            rate_data.append({"County": county, "Incidents": count, "Rate": rate})
        rate_df = pd.DataFrame(rate_data).dropna(subset=["Rate"]).sort_values("Rate", ascending=False).head(15)
        chart_card("Top counties by incident rate per 100k",
                   charts.generic_bar(rate_df.set_index("County")["Rate"], color="#0d9488", unit="per 100k"),
                   height=400)

# Heatmap
chart_card("County × offence category heatmap",
           charts.county_offence_heatmap(res, n_counties=10), height=500)

# Victim-per-incident by county
c3, c4 = st.columns(2)
with c3:
    chart_card("Avg victims per incident – by county",
               charts.avg_victims_per_incident(mapped, group_col="County", top_n=10), height=400)
with c4:
    chart_card("Avg victims per incident – by offence category",
               charts.avg_victims_per_incident(res, group_col="Offence Category", top_n=10), height=400)

st.caption(
    "Counties with 'Unknown', 'Multiple Counties', 'Nationwide' or 'Outside Kenya' "
    "cannot be placed on the map. County centroids are approximate. "
    "Incident rate per 100,000 population uses 2019 census estimates."
)
