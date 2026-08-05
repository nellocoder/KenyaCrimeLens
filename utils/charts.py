"""
Unified Plotly chart factory for Kenya CrimeLens.
All charts share one clean visual language: Inter font, white background,
light gridlines, consistent category colors.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ACCENT = "#0284c7"
ACCENT_LIGHT = "#0ea5e9"

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
)


def category_colors(categories) -> dict:
    """Deterministic color per offence category."""
    return {c: _PALETTE[i % len(_PALETTE)] for i, c in enumerate(sorted(categories))}


def _style(fig, y_grid=True):
    fig.update_layout(**_BASE_LAYOUT)
    if y_grid:
        fig.update_yaxes(gridcolor="#f1f5f9", zerolinecolor="#e2e8f0")
    fig.update_xaxes(linecolor="#e2e8f0")
    return fig


def monthly_trend(df: pd.DataFrame, value: str = "incidents"):
    if value == "victims":
        g = df.groupby("Month")["Victim Tally"].sum().reset_index(name="Value")
    else:
        g = df.groupby("Month").size().reset_index(name="Value")
    fig = px.area(g, x="Month", y="Value")
    fig.update_traces(line_color=ACCENT_LIGHT, fillcolor="rgba(14,165,233,0.18)",
                      line_width=2.5, hovertemplate="%{x}<br>%{y:,}<extra></extra>")
    fig.update_yaxes(title_text="")
    fig.update_xaxes(title_text="")
    return _style(fig)


def monthly_trend_with_ma(df: pd.DataFrame, value: str = "incidents", window: int = 3):
    if value == "victims":
        g = df.groupby("Month")["Victim Tally"].sum().reset_index(name="Value")
    else:
        g = df.groupby("Month").size().reset_index(name="Value")
    g["MA"] = g["Value"].rolling(window=window, min_periods=1).mean()
    fig = px.area(g, x="Month", y="Value")
    fig.update_traces(line_color=ACCENT_LIGHT, fillcolor="rgba(14,165,233,0.18)",
                      line_width=2.5, hovertemplate="%{x}<br>%{y:,}<extra></extra>",
                      name="Monthly")
    fig.add_scatter(x=g["Month"], y=g["MA"], mode="lines",
                    line=dict(color="#0f172a", width=2, dash="dot"),
                    name=f"{window}‑month avg",
                    hovertemplate="%{x}<br>Avg: %{y:.1f}<extra></extra>")
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                  xanchor="right", x=1, font=dict(size=10)))
    fig.update_yaxes(title_text="")
    fig.update_xaxes(title_text="")
    return _style(fig)


def category_bar(df: pd.DataFrame):
    counts = df["Offence Category"].value_counts().sort_values()
    colors = category_colors(counts.index)
    fig = px.bar(counts, x=counts.values, y=counts.index, orientation="h",
                 color=counts.index, color_discrete_map=colors,
                 labels={"x": "", "y": ""})
    fig.update_traces(hovertemplate="%{y}<br>%{x:,} incidents<extra></extra>")
    fig.update_coloraxes(showscale=False)
    return _style(fig, y_grid=False)


def top_counties_bar(df: pd.DataFrame, n: int = 12):
    counts = df[df["County"] != "Unknown"]["County"].value_counts().head(n)
    fig = px.bar(x=counts.index, y=counts.values,
                 labels={"x": "", "y": ""},
                 color_discrete_sequence=["#2563eb"])
    fig.update_traces(hovertemplate="%{x}<br>%{y:,} incidents<extra></extra>")
    return _style(fig)


def donut(series_counts: pd.Series, colors=None):
    fig = px.pie(values=series_counts.values, names=series_counts.index, hole=0.55,
                 color_discrete_sequence=colors or px.colors.qualitative.Set2)
    fig.update_traces(textinfo="percent", hovertemplate="%{label}<br>%{value:,}<extra></extra>")
    fig.update_layout(**{**_BASE_LAYOUT, "showlegend": True,
                         "legend": dict(orientation="h", yanchor="bottom", y=-0.15)})
    return fig


def generic_barh(counts: pd.Series, color: str = "#8b5cf6", unit: str = "cases"):
    fig = px.bar(x=counts.values, y=counts.index, orientation="h",
                 labels={"x": "", "y": ""}, color_discrete_sequence=[color])
    fig.update_traces(hovertemplate=f"%{{y}}<br>%{{x:,}} {unit}<extra></extra>")
    return _style(fig, y_grid=False)


def generic_bar(counts: pd.Series, color: str = "#0d9488", unit: str = "cases"):
    fig = px.bar(x=counts.index, y=counts.values, labels={"x": "", "y": ""},
                 color_discrete_sequence=[color])
    fig.update_traces(hovertemplate=f"%{{x}}<br>%{{y:,}} {unit}<extra></extra>")
    return _style(fig)


def stacked_county_category(df: pd.DataFrame, n_counties: int = 10):
    top = df[df["County"] != "Unknown"]["County"].value_counts().head(n_counties).index
    cross = (df[df["County"].isin(top)]
             .groupby(["County", "Offence Category"]).size().reset_index(name="Count"))
    colors = category_colors(df["Offence Category"].unique())
    fig = px.bar(cross, x="County", y="Count", color="Offence Category",
                 color_discrete_map=colors, labels={"County": ""})
    fig.update_layout(**{**_BASE_LAYOUT, "showlegend": True,
                         "legend": dict(font=dict(size=10), title_text="")})
    fig.update_yaxes(gridcolor="#f1f5f9")
    return fig


def treemap(df: pd.DataFrame, path: list[str]):
    colors = category_colors(df[path[0]].unique())
    g = df.groupby(path).size().reset_index(name="Count")
    fig = px.treemap(g, path=path, values="Count",
                     color=path[0], color_discrete_map=colors)
    fig.update_layout(font=dict(family="Inter, Segoe UI, sans-serif", size=12,
                                color="#334155"),
                      margin=dict(l=8, r=8, t=8, b=8),
                      paper_bgcolor="rgba(0,0,0,0)")
    fig.update_traces(textinfo="label+value")
    return fig


def victims_by_category(df: pd.DataFrame):
    g = (df.groupby("Offence Category")["Victim Tally"].sum()
         .sort_values().reset_index())
    colors = category_colors(g["Offence Category"])
    fig = px.bar(g, x="Victim Tally", y="Offence Category", orientation="h",
                 color="Offence Category", color_discrete_map=colors,
                 labels={"Victim Tally": "", "Offence Category": ""})
    fig.update_traces(hovertemplate="%{y}<br>%{x:,} victims<extra></extra>")
    return _style(fig, y_grid=False)


# ---------------------------------------------------------------------------
# Spatial
# ---------------------------------------------------------------------------
COUNTY_COORDS = {
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


def county_map(df: pd.DataFrame, metric: str = "incidents", rate: bool = False):
    """
    Interactive bubble map (or choropleth placeholder) of Kenya counties.
    metric: "incidents", "victims", or "avg_victims"
    rate: if True, compute incidents per 100k population.
    """
    from utils.population import COUNTY_POPULATION

    g = (df[df["County"].isin(COUNTY_COORDS)]
         .groupby("County")
         .agg(incidents=("County", "size"),
              victims=("Victim Tally", "sum"))
         .reset_index())
    g["lat"] = g["County"].map(lambda c: COUNTY_COORDS[c][0])
    g["lon"] = g["County"].map(lambda c: COUNTY_COORDS[c][1])

    if g.empty:
        fig = go.Figure()
        fig.update_layout(title="No mappable counties in current filter")
        return fig

    if metric == "incidents":
        color_col = "incidents"
        colorbar_title = "Incidents"
        if rate:
            g["rate"] = g.apply(lambda row: crime_rate(row["incidents"], row["County"]), axis=1)
            color_col = "rate"
            colorbar_title = "Incidents per 100k"
    elif metric == "victims":
        color_col = "victims"
        colorbar_title = "Victims"
    elif metric == "avg_victims":
        g["avg_victims"] = g.apply(
            lambda row: row["victims"] / row["incidents"] if row["incidents"] >= 5 else None, axis=1)
        g = g.dropna(subset=["avg_victims"])
        if g.empty:
            fig = go.Figure()
            fig.update_layout(title="Not enough data for average victim calculation")
            return fig
        color_col = "avg_victims"
        colorbar_title = "Avg victims per incident"

    hover_data = {"incidents": True, "victims": ":.0f", "lat": False, "lon": False}
    if metric == "avg_victims":
        hover_data["avg_victims"] = ":.2f"

    try:
        fig = px.scatter_map(
            g, lat="lat", lon="lon", size="incidents", color=color_col,
            size_max=42, color_continuous_scale="Reds",
            hover_name="County", hover_data=hover_data,
            zoom=5.1, center=dict(lat=0.3, lon=37.8)
        )
        fig.update_layout(map_style="carto-positron")
    except Exception:
        fig = px.scatter_mapbox(
            g, lat="lat", lon="lon", size="incidents", color=color_col,
            size_max=42, color_continuous_scale="Reds",
            mapbox_style="carto-positron",
            hover_name="County", hover_data=hover_data,
            zoom=5.1, center=dict(lat=0.3, lon=37.8)
        )

    fig.update_layout(
        font=dict(family="Inter, Segoe UI, sans-serif", size=12, color="#334155"),
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(title=colorbar_title, thickness=12),
    )
    return fig


def county_offence_heatmap(df: pd.DataFrame, n_counties: int = 10):
    """Heatmap: top counties x offence categories."""
    top_counties = df[df["County"] != "Unknown"]["County"].value_counts().head(n_counties).index
    cross = (df[df["County"].isin(top_counties)]
             .groupby(["County", "Offence Category"]).size().reset_index(name="Count"))
    pivot = cross.pivot(index="County", columns="Offence Category", values="Count").fillna(0)
    pivot = pivot[sorted(pivot.columns)]

    fig = px.imshow(pivot, text_auto='.0f', aspect="auto",
                    color_continuous_scale="Blues",
                    labels=dict(x="Offence Category", y="County", color="Incidents"))
    fig.update_xaxes(side="top")
    fig.update_layout(font=dict(family="Inter, Segoe UI, sans-serif", size=11),
                      margin=dict(l=8, r=8, t=50, b=8))
    return fig


def county_category_composition(df, n_counties=10, use_percent=True):
    top = df[df["County"] != "Unknown"]["County"].value_counts().head(n_counties).index
    cross = (df[df["County"].isin(top)]
             .groupby(["County", "Offence Category"]).size().reset_index(name="Count"))
    pivot = cross.pivot(index="County", columns="Offence Category", values="Count").fillna(0)
    if use_percent:
        pivot = pivot.div(pivot.sum(axis=1), axis=0) * 100
    pivot = pivot[sorted(pivot.columns)]
    fig = px.bar(pivot, x=pivot.columns, y=pivot.index, orientation="h",
                 labels={"x": "% of incidents" if use_percent else "Incidents", "y": ""},
                 color_discrete_map=category_colors(pivot.columns))
    fig.update_layout(**_BASE_LAYOUT)
    fig.update_layout(barmode="stack", showlegend=True,
                      legend=dict(font=dict(size=10), title_text="", orientation="h",
                                  yanchor="bottom", y=1.02, xanchor="right", x=1),
                      margin=dict(l=8, r=8, t=35, b=8))
    fig.update_yaxes(categoryorder="total ascending")
    fig.update_xaxes(title_text="")
    fig.update_traces(hovertemplate="%{y}<br>%{x}: %{value:.1f}%<extra></extra>" if use_percent
                      else "%{y}<br>%{x}: %{value} incidents<extra></extra>")
    return fig


def avg_victims_per_incident(df, group_col="County", top_n=10):
    agg = df.groupby(group_col).agg(incidents=("County", "size"),
                                    victims=("Victim Tally", "sum")).reset_index()
    agg = agg[agg["incidents"] >= 5]
    agg["avg_victims"] = agg["victims"] / agg["incidents"]
    top = agg.sort_values("avg_victims", ascending=False).head(top_n)
    top = top.sort_values("avg_victims")
    fig = px.bar(top, x="avg_victims", y=group_col, orientation="h",
                 labels={"avg_victims": "Avg victims per incident", group_col: ""},
                 color_discrete_sequence=["#b91c1c"])
    fig.update_traces(hovertemplate="%{y}<br>%{x:.1f} victims per incident<extra></extra>")
    fig.update_xaxes(title_text="")
    return _style(fig, y_grid=False)
