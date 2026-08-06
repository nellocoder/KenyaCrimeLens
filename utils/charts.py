"""Unified Plotly chart factory for Kenya CrimeLens.

All charts share one visual language: Inter font, white background, light
gridlines, deterministic category colours, rich hover templates. The county
map is a true GeoJSON choropleth with a bubble fallback when boundaries are
unavailable.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import config as C
from utils.loader import load_geojson

ACCENT = C.ACCENT
ACCENT_LIGHT = C.ACCENT_LIGHT

_PALETTE = [
    "#dc2626", "#ea580c", "#d97706", "#ca8a04", "#65a30d", "#16a34a", "#0d9488",
    "#0891b2", "#2563eb", "#4f46e5", "#7c3aed", "#a21caf", "#db2777", "#e11d48",
    "#57534e", "#475569", "#0f766e", "#9333ea", "#1d4ed8",
]

_BASE_LAYOUT = dict(
    font=dict(family="Inter, Segoe UI, sans-serif", size=12, color="#334155"),
    plot_bgcolor="white",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=8, r=16, t=8, b=8),
    showlegend=False,
    hoverlabel=dict(bgcolor="white", font_size=12,
                    font_family="Inter, Segoe UI, sans-serif"),
)

MAP_SCALE = "YlOrRd"


def category_colors(categories) -> dict[str, str]:
    """Deterministic colour per offence category (stable across pages)."""
    return {c: _PALETTE[i % len(_PALETTE)] for i, c in enumerate(sorted(categories))}


def _style(fig: go.Figure, y_grid: bool = True) -> go.Figure:
    fig.update_layout(**_BASE_LAYOUT)
    if y_grid:
        fig.update_yaxes(gridcolor="#f1f5f9", zerolinecolor="#e2e8f0")
    fig.update_xaxes(linecolor="#e2e8f0")
    return fig


def empty_state(message: str) -> go.Figure:
    """Placeholder figure shown when a chart has no data to draw."""
    fig = go.Figure()
    fig.add_annotation(text=message, showarrow=False,
                       font=dict(size=13, color="#94a3b8"))
    fig.update_layout(**_BASE_LAYOUT, xaxis_visible=False, yaxis_visible=False)
    return fig


# ---------------------------------------------------------------------------
# Time series
# ---------------------------------------------------------------------------
def monthly_trend(df: pd.DataFrame, value: str = "incidents") -> go.Figure:
    """Area chart of incidents (or victims) per month with a peak annotation."""
    if value == "victims":
        g = df.groupby(C.COL_MONTH)[C.COL_VICTIMS].sum().reset_index(name="Value")
        unit = "victims"
    else:
        g = df.groupby(C.COL_MONTH).size().reset_index(name="Value")
        unit = "incidents"
    if g.empty:
        return empty_state("No data for the current selection")

    fig = px.area(g, x=C.COL_MONTH, y="Value")
    fig.update_traces(line_color=ACCENT_LIGHT, fillcolor="rgba(14,165,233,0.18)",
                      line_width=2.5,
                      hovertemplate=f"%{{x}}<br>%{{y:,}} {unit}<extra></extra>")
    peak = g.loc[g["Value"].idxmax()]
    fig.add_annotation(x=peak[C.COL_MONTH], y=peak["Value"],
                       text=f"Peak: {int(peak['Value']):,}",
                       showarrow=True, arrowhead=2, ax=0, ay=-28,
                       font=dict(size=11, color="#0f172a"),
                       bgcolor="rgba(255,255,255,0.85)")
    fig.update_yaxes(title_text="", rangemode="tozero")
    fig.update_xaxes(title_text="")
    return _style(fig)


def monthly_trend_with_ma(df: pd.DataFrame, value: str = "incidents",
                          window: int = 3) -> go.Figure:
    """Monthly area chart with a moving-average overlay to expose the trend."""
    if value == "victims":
        g = df.groupby(C.COL_MONTH)[C.COL_VICTIMS].sum().reset_index(name="Value")
    else:
        g = df.groupby(C.COL_MONTH).size().reset_index(name="Value")
    if g.empty:
        return empty_state("No data for the current selection")

    g["MA"] = g["Value"].rolling(window=window, min_periods=1).mean()
    fig = px.area(g, x=C.COL_MONTH, y="Value")
    fig.update_traces(line_color=ACCENT_LIGHT, fillcolor="rgba(14,165,233,0.18)",
                      line_width=2.5, name="Monthly",
                      hovertemplate="%{x}<br>%{y:,}<extra></extra>")
    fig.add_scatter(x=g[C.COL_MONTH], y=g["MA"], mode="lines",
                    line=dict(color="#0f172a", width=2, dash="dot"),
                    name=f"{window}-month avg",
                    hovertemplate="%{x}<br>Avg: %{y:.1f}<extra></extra>")
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                  xanchor="right", x=1, font=dict(size=10)))
    fig.update_yaxes(title_text="", rangemode="tozero")
    fig.update_xaxes(title_text="")
    fig = _style(fig)
    fig.update_layout(showlegend=True)
    return fig


# ---------------------------------------------------------------------------
# Categorical bars, donuts, treemaps
# ---------------------------------------------------------------------------
def category_bar(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar of incidents by offence category with share tooltips."""
    counts = df[C.COL_CATEGORY].value_counts().sort_values()
    if counts.empty:
        return empty_state("No data for the current selection")
    total = counts.sum()
    share = (counts / total * 100).round(1)
    fig = px.bar(x=counts.values, y=counts.index, orientation="h",
                 color=counts.index, color_discrete_map=category_colors(counts.index),
                 labels={"x": "", "y": ""})
    fig.update_traces(customdata=share.values.reshape(-1, 1),
                      hovertemplate="%{y}<br>%{x:,} incidents · %{customdata[0]}%"
                                    "<extra></extra>")
    return _style(fig, y_grid=False)


def top_counties_bar(df: pd.DataFrame, n: int = 12) -> go.Figure:
    counts = df[df[C.COL_COUNTY] != C.UNKNOWN][C.COL_COUNTY].value_counts().head(n)
    if counts.empty:
        return empty_state("No located counties in the current selection")
    fig = px.bar(x=counts.index, y=counts.values, labels={"x": "", "y": ""},
                 color_discrete_sequence=["#2563eb"])
    fig.update_traces(hovertemplate="%{x}<br>%{y:,} incidents<extra></extra>")
    return _style(fig)


def donut(series_counts: pd.Series, colors: list[str] | None = None) -> go.Figure:
    if series_counts.empty:
        return empty_state("No data for the current selection")
    fig = px.pie(values=series_counts.values, names=series_counts.index, hole=0.55,
                 color_discrete_sequence=colors or px.colors.qualitative.Set2)
    fig.update_traces(textinfo="percent",
                      hovertemplate="%{label}<br>%{value:,} · %{percent}<extra></extra>")
    fig.update_layout(**{**_BASE_LAYOUT, "showlegend": True,
                         "legend": dict(orientation="h", yanchor="bottom", y=-0.15)})
    return fig


def generic_barh(counts: pd.Series, color: str = "#8b5cf6",
                 unit: str = "cases") -> go.Figure:
    if counts.empty:
        return empty_state("No data for the current selection")
    fig = px.bar(x=counts.values, y=counts.index, orientation="h",
                 labels={"x": "", "y": ""}, color_discrete_sequence=[color])
    fig.update_traces(hovertemplate=f"%{{y}}<br>%{{x:,}} {unit}<extra></extra>")
    return _style(fig, y_grid=False)


def generic_bar(counts: pd.Series, color: str = "#0d9488",
                unit: str = "cases") -> go.Figure:
    if counts.empty:
        return empty_state("No data for the current selection")
    fig = px.bar(x=counts.index, y=counts.values, labels={"x": "", "y": ""},
                 color_discrete_sequence=[color])
    fig.update_traces(hovertemplate=f"%{{x}}<br>%{{y:,}} {unit}<extra></extra>")
    return _style(fig)


def stacked_county_category(df: pd.DataFrame, n_counties: int = 10) -> go.Figure:
    top = df[df[C.COL_COUNTY] != C.UNKNOWN][C.COL_COUNTY].value_counts().head(n_counties).index
    cross = (df[df[C.COL_COUNTY].isin(top)]
             .groupby([C.COL_COUNTY, C.COL_CATEGORY]).size().reset_index(name="Count"))
    if cross.empty:
        return empty_state("No located counties in the current selection")
    fig = px.bar(cross, x=C.COL_COUNTY, y="Count", color=C.COL_CATEGORY,
                 color_discrete_map=category_colors(df[C.COL_CATEGORY].unique()),
                 labels={C.COL_COUNTY: ""})
    fig.update_traces(hovertemplate="%{x}<br>%{fullData.name}: %{y:,}<extra></extra>")
    fig.update_layout(**{**_BASE_LAYOUT, "showlegend": True,
                         "legend": dict(font=dict(size=10), title_text="")})
    fig.update_yaxes(gridcolor="#f1f5f9")
    return fig


def treemap(df: pd.DataFrame, path: list[str]) -> go.Figure:
    if df.empty:
        return empty_state("No data for the current selection")
    g = df.groupby(path).size().reset_index(name="Count")
    fig = px.treemap(g, path=path, values="Count",
                     color=path[0], color_discrete_map=category_colors(df[path[0]].unique()))
    fig.update_layout(font=dict(family="Inter, Segoe UI, sans-serif", size=12,
                                color="#334155"),
                      margin=dict(l=8, r=8, t=8, b=8),
                      paper_bgcolor="rgba(0,0,0,0)")
    fig.update_traces(textinfo="label+value",
                      hovertemplate="%{label}<br>%{value:,} incidents<extra></extra>")
    return fig


def victims_by_category(df: pd.DataFrame) -> go.Figure:
    g = (df.groupby(C.COL_CATEGORY)[C.COL_VICTIMS].sum().sort_values().reset_index())
    if g.empty:
        return empty_state("No data for the current selection")
    fig = px.bar(g, x=C.COL_VICTIMS, y=C.COL_CATEGORY, orientation="h",
                 color=C.COL_CATEGORY, color_discrete_map=category_colors(g[C.COL_CATEGORY]),
                 labels={C.COL_VICTIMS: "", C.COL_CATEGORY: ""})
    fig.update_traces(hovertemplate="%{y}<br>%{x:,} victims<extra></extra>")
    return _style(fig, y_grid=False)


def county_category_composition(df: pd.DataFrame, n_counties: int = 10,
                                use_percent: bool = True) -> go.Figure:
    """100% stacked bar of offence categories within the top counties."""
    top_counties = (df[df[C.COL_COUNTY] != C.UNKNOWN][C.COL_COUNTY]
                    .value_counts().head(n_counties).index)
    cross = (df[df[C.COL_COUNTY].isin(top_counties)]
             .groupby([C.COL_COUNTY, C.COL_CATEGORY]).size().reset_index(name="Count"))
    if cross.empty:
        return empty_state("No located counties in the current selection")

    pivot = cross.pivot(index=C.COL_COUNTY, columns=C.COL_CATEGORY,
                        values="Count").fillna(0)
    if use_percent:
        pivot = pivot.div(pivot.sum(axis=1), axis=0) * 100
    pivot = pivot[sorted(pivot.columns)]

    fig = px.bar(pivot, x=pivot.columns, y=pivot.index, orientation="h",
                 color_discrete_map=category_colors(pivot.columns))
    fig.update_layout(**_BASE_LAYOUT)
    fig.update_layout(barmode="stack", showlegend=True,
                      legend=dict(font=dict(size=10), title_text="",
                                  orientation="h", yanchor="bottom", y=1.02,
                                  xanchor="right", x=1),
                      margin=dict(l=8, r=8, t=35, b=8))
    fig.update_yaxes(categoryorder="total ascending")
    fig.update_xaxes(title_text="% of incidents" if use_percent else "Incidents")
    tpl = ("%{y}<br>%{fullData.name}: %{x:.1f}%<extra></extra>" if use_percent
           else "%{y}<br>%{fullData.name}: %{x:,} incidents<extra></extra>")
    fig.update_traces(hovertemplate=tpl)
    return fig


def avg_victims_per_incident(df: pd.DataFrame, group_col: str = C.COL_COUNTY,
                             top_n: int = 10) -> go.Figure:
    """Average victims per incident for the top-N groups (min 5 incidents)."""
    agg = df.groupby(group_col).agg(
        incidents=(group_col, "size"), victims=(C.COL_VICTIMS, "sum")
    ).reset_index()
    agg = agg[agg["incidents"] >= C.MIN_INCIDENTS_FOR_RATIO]
    if agg.empty:
        return empty_state(f"Fewer than {C.MIN_INCIDENTS_FOR_RATIO} incidents per group")
    agg["avg_victims"] = agg["victims"] / agg["incidents"]
    top = (agg.sort_values("avg_victims", ascending=False).head(top_n)
           .sort_values("avg_victims"))
    fig = px.bar(top, x="avg_victims", y=group_col, orientation="h",
                 labels={"avg_victims": "", group_col: ""},
                 color_discrete_sequence=[C.KENYA_RED])
    fig.update_traces(customdata=top[["incidents"]].values,
                      hovertemplate="%{y}<br>%{x:.1f} victims per incident · "
                                    "%{customdata[0]:,} incidents<extra></extra>")
    return _style(fig, y_grid=False)


# ---------------------------------------------------------------------------
# Spatial: choropleth + bubble fallback
# ---------------------------------------------------------------------------
COUNTY_COORDS: dict[str, tuple[float, float]] = {
    "Baringo": (0.4667, 35.9667), "Bomet": (-0.7813, 35.3416),
    "Bungoma": (0.5635, 34.5606), "Busia": (0.4608, 34.1115),
    "Elgeyo Marakwet": (0.8167, 35.4500), "Embu": (-0.5311, 37.4506),
    "Garissa": (-0.4532, 39.6461), "Homa Bay": (-0.5273, 34.4571),
    "Isiolo": (0.3546, 37.5822), "Kajiado": (-1.8533, 36.7768),
    "Kakamega": (0.2827, 34.7519), "Kericho": (-0.3689, 35.2863),
    "Kiambu": (-1.1714, 36.8356), "Kilifi": (-3.2192, 39.7400),
    "Kirinyaga": (-0.4989, 37.2803), "Kisii": (-0.6773, 34.7796),
    "Kisumu": (-0.0917, 34.7680), "Kitui": (-1.3667, 38.0167),
    "Kwale": (-4.1737, 39.4521), "Laikipia": (0.2000, 36.5333),
    "Lamu": (-2.2717, 40.9020), "Machakos": (-1.5177, 37.2634),
    "Makueni": (-1.8033, 37.6200), "Mandera": (3.9373, 41.8569),
    "Marsabit": (2.3284, 37.9899), "Meru": (0.0463, 37.6559),
    "Migori": (-1.0634, 34.4731), "Mombasa": (-4.0435, 39.6682),
    "Murang'a": (-0.7833, 37.1000), "Nairobi": (-1.2921, 36.8219),
    "Nakuru": (-0.3031, 36.0800), "Nandi": (0.1833, 35.1000),
    "Narok": (-1.0833, 35.8667), "Nyamira": (-0.5667, 34.9333),
    "Nyandarua": (-0.1833, 36.5167), "Nyeri": (-0.4167, 36.9500),
    "Samburu": (1.1000, 36.7000), "Siaya": (-0.0607, 34.2881),
    "Taita Taveta": (-3.4000, 38.3667), "Tana River": (-1.5000, 39.5000),
    "Tharaka Nithi": (-0.3000, 37.8500), "Trans Nzoia": (1.0167, 35.0000),
    "Turkana": (3.1167, 35.6000), "Uasin Gishu": (0.5167, 35.2833),
    "Vihiga": (0.0667, 34.7167), "Wajir": (1.7471, 40.0629),
    "West Pokot": (1.2333, 35.1167),
}

_METRIC_META = {
    "incidents": ("Incidents", "%{customdata[0]:,} incidents"),
    "victims": ("Victims", "%{customdata[1]:,} victims"),
    "severity": ("Avg victims / incident", "%{customdata[2]:.2f} victims per incident"),
}


def _county_agg(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate incidents, victims and severity per mappable county."""
    g = (df[df[C.COL_COUNTY].isin(COUNTY_COORDS)]
         .groupby(C.COL_COUNTY)
         .agg(incidents=(C.COL_COUNTY, "size"), victims=(C.COL_VICTIMS, "sum"))
         .reset_index())
    g["severity"] = g["victims"] / g["incidents"]
    g.loc[g["incidents"] < C.MIN_INCIDENTS_FOR_RATIO, "severity"] = pd.NA
    g["rank"] = g["incidents"].rank(method="min", ascending=False).astype(int)
    top_cat = (df.groupby(C.COL_COUNTY)[C.COL_CATEGORY]
               .agg(lambda s: s.value_counts().index[0]))
    g["top_category"] = g[C.COL_COUNTY].map(top_cat)
    return g


def county_choropleth(df: pd.DataFrame, metric: str = "incidents") -> go.Figure | None:
    """True choropleth over Kenya county boundaries.

    Returns None when the GeoJSON asset is unavailable so callers can fall
    back to the bubble map.
    """
    geojson = load_geojson()
    if geojson is None:
        return None
    g = _county_agg(df)
    if metric == "severity":
        g = g.dropna(subset=["severity"])
    if g.empty:
        return empty_state("No mappable counties in the current selection")

    title, metric_line = _METRIC_META.get(metric, _METRIC_META["incidents"])
    custom = g[["incidents", "victims", "severity", "rank", "top_category"]].fillna(0)

    trace_kwargs = dict(
        geojson=geojson,
        featureidkey="properties.county",
        locations=g[C.COL_COUNTY],
        z=g[metric].astype(float),
        colorscale=MAP_SCALE,
        marker_line_color="#94a3b8",
        marker_line_width=0.6,
        customdata=custom.values,
        hovertemplate=("<b>%{location}</b><br>" + metric_line +
                       "<br>%{customdata[0]:,} incidents · "
                       "%{customdata[1]:,} victims"
                       "<br>Rank by incidents: #%{customdata[3]}"
                       "<br>Top category: %{customdata[4]}<extra></extra>"),
        colorbar=dict(title=title, thickness=12),
    )
    view = dict(style="carto-positron", zoom=5.1, center=dict(lat=0.3, lon=37.8))
    if hasattr(go, "Choroplethmap"):  # Plotly >= 5.24 (MapLibre)
        fig = go.Figure(go.Choroplethmap(**trace_kwargs))
        fig.update_layout(map=view)
    else:  # legacy Mapbox traces
        fig = go.Figure(go.Choroplethmapbox(**trace_kwargs))
        fig.update_layout(mapbox=view)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family="Inter, Segoe UI, sans-serif", size=12, color="#334155"),
    )
    return fig


def county_map(df: pd.DataFrame, metric: str = "incidents") -> go.Figure:
    """Bubble map fallback: size shows volume, colour shows the chosen metric."""
    g = _county_agg(df)
    if metric == "severity":
        g = g.dropna(subset=["severity"])
    if g.empty:
        return empty_state("No mappable counties in the current selection")

    g["lat"] = g[C.COL_COUNTY].map(lambda c: COUNTY_COORDS[c][0])
    g["lon"] = g[C.COL_COUNTY].map(lambda c: COUNTY_COORDS[c][1])
    color_col = metric if metric in ("incidents", "victims", "severity") else "incidents"
    title, _ = _METRIC_META.get(metric, _METRIC_META["incidents"])

    scatter_kwargs = dict(
        lat="lat", lon="lon", size="incidents", color=color_col,
        size_max=42, color_continuous_scale=MAP_SCALE, hover_name=C.COL_COUNTY,
        custom_data=["incidents", "victims", "severity", "rank", "top_category"],
        zoom=5.1, center=dict(lat=0.3, lon=37.8),
    )
    if hasattr(px, "scatter_map"):  # Plotly >= 5.24 (MapLibre)
        fig = px.scatter_map(g, **scatter_kwargs)
        fig.update_layout(map_style="carto-positron")
    else:
        fig = px.scatter_mapbox(g, **scatter_kwargs)
        fig.update_layout(mapbox_style="carto-positron")
    fig.update_traces(hovertemplate=(
        "<b>%{hovertext}</b><br>%{customdata[0]:,} incidents · "
        "%{customdata[1]:,} victims<br>Rank: #%{customdata[3]} · "
        "Top category: %{customdata[4]}<extra></extra>"))
    fig.update_layout(
        font=dict(family="Inter, Segoe UI, sans-serif", size=12, color="#334155"),
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(title=title, thickness=12),
    )
    return fig
