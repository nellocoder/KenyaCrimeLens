"""Shared analytics helpers: top-N aggregations, KPIs, auto-generated summary."""

import pandas as pd


def top_n(series: pd.Series, n: int = 1, exclude_unknown: bool = True) -> pd.Series:
    s = series
    if exclude_unknown:
        s = s[s != "Unknown"]
    return s.value_counts().head(n)


def kpis(res: pd.DataFrame) -> list[dict]:
    """Standard 4 KPI cards for a filtered result set."""
    victims = int(res["Victim Tally"].sum())
    perps = int(res["Perpetrator Tally"].sum())
    tc = top_n(res["County"], 1)
    tcat = top_n(res["Offence Category"], 1, exclude_unknown=False)
    return [
        {"icon": "📈", "label": "Incidents", "value": f"{len(res):,}",
         "sub": f"{res['County'].nunique()} counties affected"},
        {"icon": "👥", "label": "Victims", "value": f"{victims:,}",
         "sub": f"{perps:,} recorded perpetrators"},
        {"icon": "📍", "label": "Top County",
         "value": tc.index[0] if len(tc) else "—",
         "sub": f"{tc.iloc[0]} incidents" if len(tc) else ""},
        {"icon": "📂", "label": "Top Category",
         "value": tcat.index[0] if len(tcat) else "—",
         "sub": f"{tcat.iloc[0]} incidents" if len(tcat) else ""},
    ]


def build_summary(res: pd.DataFrame, f: dict) -> str:
    """Auto-generated plain-language analysis of the filtered selection."""
    if res.empty:
        return "No incidents match the selected filters. Try broadening your query."

    victims = int(res["Victim Tally"].sum())
    top_cat = res["Offence Category"].value_counts().head(1)
    top_county = top_n(res["County"], 1)
    top_weapon = top_n(res["Weapon"], 1)
    top_motive = top_n(res["Motive"], 1)

    scope = []
    if f["county"] != "All":
        scope.append(f"in <b>{f['county']}</b>")
    if f["category"] != "All":
        scope.append(f"for <b>{f['category']}</b> offences")
    scope_txt = " " + " ".join(scope) if scope else ""

    text = (
        f"Between <b>{res['Date'].min():%Y-%m-%d}</b> and <b>{res['Date'].max():%Y-%m-%d}</b>, "
        f"<b>{len(res):,} incidents</b>{scope_txt} were reported in the media, involving "
        f"<b>{victims:,} victims</b>. <b>{top_cat.index[0]}</b> was the most frequent "
        f"category ({top_cat.iloc[0]} incidents, {round(top_cat.iloc[0] / len(res) * 100)}%)."
    )
    if len(top_county):
        text += (f" <b>{top_county.index[0]}</b> recorded the highest number of "
                 f"incidents ({top_county.iloc[0]}).")
    if len(top_weapon):
        text += f" The most common weapon was <b>{top_weapon.index[0]}</b> ({top_weapon.iloc[0]} cases),"
    if len(top_motive):
        text += f" and the leading recorded motive was <b>{top_motive.index[0]}</b> ({top_motive.iloc[0]} cases)."

    y25 = len(res[res["Year"] == 2025])
    y26 = len(res[res["Year"] == 2026])
    if y25 > 0 and y26 > 0:
        text += (f" {y26} of these were recorded in 2026 against {y25} in 2025 "
                 "(note: 2026 data is partial).")
    return text
