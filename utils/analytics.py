"""Shared analytics helpers: top-N aggregations, KPIs, auto-generated summary."""

import pandas as pd
from utils.population import COUNTY_POPULATION


def top_n(series: pd.Series, n: int = 1, exclude_unknown: bool = True) -> pd.Series:
    s = series
    if exclude_unknown:
        s = s[s != "Unknown"]
    return s.value_counts().head(n)


def kpis(res: pd.DataFrame) -> list[dict]:
    """Standard 4 KPI cards for a filtered result set."""
    total_incidents = len(res)
    reported_victims = int(res["Victim Tally"].sum())
    known_victim_incidents = res["Victim Known"].sum()
    perps = int(res["Perpetrator Tally"].sum())
    tc = top_n(res["County"], 1)
    tcat = top_n(res["Offence Category"], 1, exclude_unknown=False)

    return [
        {"icon": "📈", "label": "Reported incidents",
         "value": f"{total_incidents:,}",
         "sub": f"{res['County'].nunique()} counties mentioned"},
        {"icon": "👥", "label": "Reported victims",
         "value": f"{reported_victims:,}",
         "sub": f"{known_victim_incidents} incidents with known victim count"},
        {"icon": "📍", "label": "Top county (incidents)",
         "value": tc.index[0] if len(tc) else "—",
         "sub": f"{tc.iloc[0]} incidents" if len(tc) else ""},
        {"icon": "📂", "label": "Top category",
         "value": tcat.index[0] if len(tcat) else "—",
         "sub": f"{tcat.iloc[0]} incidents" if len(tcat) else ""},
    ]


def crime_rate(incidents: int, county: str) -> float | None:
    """Incidents per 100,000 population."""
    pop = COUNTY_POPULATION.get(county)
    if pop:
        return round(incidents / pop * 100000, 1)
    return None


def build_summary(res: pd.DataFrame, f: dict) -> str:
    """Auto-generated plain-language analysis of the filtered selection."""
    if res.empty:
        return "No incidents match the selected filters."

    total_inc = len(res)
    total_victims = int(res["Victim Tally"].sum())
    known_victim = res["Victim Known"].sum()
    top_cat = res["Offence Category"].value_counts().head(1)
    top_county = top_n(res["County"], 1)
    top_weapon = top_n(res["Weapon"], 1)
    top_motive = top_n(res["Motive"], 1)

    scope = []
    if f.get("county", "All") != "All":
        scope.append(f"in <b>{f['county']}</b>")
    if f.get("category", "All") != "All":
        scope.append(f"for <b>{f['category']}</b> offences")
    scope_txt = " " + " ".join(scope) if scope else ""

    text = (
        f"Between <b>{res['Date'].min():%Y-%m-%d}</b> and <b>{res['Date'].max():%Y-%m-%d}</b>, "
        f"<b>{total_inc:,} media‑reported incidents</b>{scope_txt} were recorded. "
        f"Among those, <b>{total_victims:,} victims</b> were reported "
        f"(victim count was available for {known_victim} of {total_inc} incidents). "
        f"<b>{top_cat.index[0]}</b> was the most frequent category "
        f"({top_cat.iloc[0]} incidents, {round(top_cat.iloc[0] / total_inc * 100)}%)."
    )

    if len(top_county):
        text += f" <b>{top_county.index[0]}</b> had the highest incident count ({top_county.iloc[0]})."
    if len(top_weapon):
        text += f" The most common weapon mentioned was <b>{top_weapon.index[0]}</b> ({top_weapon.iloc[0]} cases),"
    if len(top_motive):
        text += f" and the leading recorded motive was <b>{top_motive.index[0]}</b> ({top_motive.iloc[0]} cases)."

    y25 = len(res[res["Year"] == 2025])
    y26 = len(res[res["Year"] == 2026])
    if y25 > 0 and y26 > 0:
        text += (f" {y26} of these were recorded in 2026 against {y25} in 2025 "
                 "(note: 2026 data is partial).")

    text += ("<br><br><i>Caution: These figures reflect media‑reported incidents, "
             "not official police statistics. Missing victim counts are not imputed.</i>")

    return text
