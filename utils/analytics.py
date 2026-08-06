"""Shared analytics helpers for Kenya CrimeLens.

Provides top-N aggregations, standard KPI blocks and an automatic narrative
engine. The narrative goes beyond describing counts: it detects trend
direction, month-over-month change, geographic concentration, outlier months
and severity extremes, so the summary reads like an analyst's briefing.
"""

from __future__ import annotations

import html

import numpy as np
import pandas as pd

from utils import config as C


def top_n(series: pd.Series, n: int = 1, exclude_unknown: bool = True) -> pd.Series:
    """Value counts of the top-n values, optionally excluding 'Unknown'."""
    s = series[series != C.UNKNOWN] if exclude_unknown else series
    return s.value_counts().head(n)


def kpis(res: pd.DataFrame) -> list[dict]:
    """Standard 4 KPI cards for a filtered result set."""
    victims = int(res[C.COL_VICTIMS].sum())
    perps = int(res[C.COL_PERPS].sum(skipna=True) or 0)
    tc = top_n(res[C.COL_COUNTY], 1)
    tcat = top_n(res[C.COL_CATEGORY], 1, exclude_unknown=False)
    return [
        {"icon": "📈", "label": "Incidents", "value": f"{len(res):,}",
         "sub": f"{res[C.COL_COUNTY].nunique()} counties affected"},
        {"icon": "👥", "label": "Victims", "value": f"{victims:,}",
         "sub": f"{perps:,} recorded perpetrators"},
        {"icon": "📍", "label": "Top County",
         "value": tc.index[0] if len(tc) else "—",
         "sub": f"{tc.iloc[0]} incidents" if len(tc) else ""},
        {"icon": "📂", "label": "Top Category",
         "value": tcat.index[0] if len(tcat) else "—",
         "sub": f"{tcat.iloc[0]} incidents" if len(tcat) else ""},
    ]


def county_scoreboard(res: pd.DataFrame) -> pd.DataFrame:
    """Per-county incidents, victims, perpetrators, top category and shares."""
    known = res[res[C.COL_COUNTY] != C.UNKNOWN]
    if known.empty:
        return pd.DataFrame()
    tbl = (
        known.groupby(C.COL_COUNTY)
        .agg(
            Incidents=(C.COL_COUNTY, "size"),
            Victims=(C.COL_VICTIMS, "sum"),
            Perpetrators=(C.COL_PERPS, "sum"),
            **{"Top Category": (C.COL_CATEGORY, lambda s: s.value_counts().index[0])},
        )
        .reset_index()
    )
    tbl["% of incidents"] = (tbl["Incidents"] / len(known) * 100).round(1)
    total_victims = known[C.COL_VICTIMS].sum()
    tbl["% of victims"] = (tbl["Victims"] / total_victims * 100).round(1) if total_victims else 0.0
    tbl["Victims / incident"] = (tbl["Victims"] / tbl["Incidents"]).round(2)
    return tbl.sort_values("Incidents", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Narrative engine
# ---------------------------------------------------------------------------
def _b(value: object) -> str:
    """Bold an escaped value for the HTML summary."""
    return f"<b>{html.escape(str(value))}</b>"


def _trend_sentence(res: pd.DataFrame) -> str:
    """Trend direction from a linear fit over monthly counts.

    A trailing month that is clearly incomplete (its calendar days are only
    partly covered by the data's own maximum date) would otherwise register
    as a sharp fake drop and a false outlier, so it is dropped before any
    month-over-month or outlier reasoning. The reader is told the comparison
    uses complete months only.
    """
    monthly = res.groupby(C.COL_MONTH).size()
    if len(monthly) < 3:
        return ""

    last_period = pd.Period(monthly.index[-1], freq="M")
    max_date = res[C.COL_DATE].max()
    coverage = max_date.day / last_period.days_in_month
    dropped_partial = coverage < 0.9 and len(monthly) > 3
    if dropped_partial:
        monthly = monthly.iloc[:-1]

    y = monthly.values.astype(float)
    slope = np.polyfit(np.arange(len(y)), y, 1)[0]
    mean = y.mean() or 1.0
    rel = slope / mean
    if rel > 0.05:
        direction = "an upward trend"
    elif rel < -0.05:
        direction = "a downward trend"
    else:
        direction = "a broadly flat trend"

    last, prev = y[-1], y[-2]
    mom = (last - prev) / prev * 100 if prev else 0.0
    complete_note = " (complete months only)" if dropped_partial else ""
    txt = (f" Monthly reporting shows {_b(direction)} across the period"
           f"{complete_note}, with the most recent full month at "
           f"{_b(f'{int(last):,}')} incidents "
           f"({_b(f'{mom:+.0f}%')} versus the month before).")

    if len(y) >= 4:
        z = (y - y.mean()) / (y.std() or 1.0)
        if abs(z).max() >= 2:
            peak_month = monthly.index[int(abs(z).argmax())]
            txt += (f" {_b(peak_month)} stands out as a statistical outlier "
                    f"({int(monthly.loc[peak_month]):,} incidents) and merits "
                    "closer review.")
    return txt


def _concentration_sentence(res: pd.DataFrame) -> str:
    """How geographically concentrated the incidents are."""
    known = res[res[C.COL_COUNTY] != C.UNKNOWN]
    counts = known[C.COL_COUNTY].value_counts()
    if len(counts) < 3:
        return ""
    top3_share = counts.head(3).sum() / counts.sum() * 100
    counties = ", ".join(counts.head(3).index)
    level = "highly concentrated" if top3_share >= 50 else "moderately spread"
    return (f" Geographically, activity is {_b(level)}: the top three counties "
            f"({html.escape(counties)}) account for {_b(f'{top3_share:.0f}%')} "
            f"of located incidents.")


def _severity_sentence(res: pd.DataFrame) -> str:
    """Which category carries the heaviest toll per incident."""
    agg = res.groupby(C.COL_CATEGORY).agg(
        incidents=(C.COL_CATEGORY, "size"), victims=(C.COL_VICTIMS, "sum")
    )
    agg = agg[agg["incidents"] >= C.MIN_INCIDENTS_FOR_RATIO]
    if agg.empty:
        return ""
    agg["ratio"] = agg["victims"] / agg["incidents"]
    worst = agg["ratio"].idxmax()
    worst_ratio = float(agg.loc[worst, "ratio"])
    overall = res[C.COL_VICTIMS].sum() / len(res)
    return (f" On a per-incident basis, {_b(worst)} carries the heaviest toll at "
            f"{_b(f'{worst_ratio:.1f}')} victims per incident (versus an overall "
            f"average of {_b(f'{overall:.1f}')}), typically reflecting a few "
            "high-victim cases rather than every incident.")


def build_summary(res: pd.DataFrame, f: dict) -> str:
    """Auto-generated, insight-driven analysis of the filtered selection.

    Returns HTML (with <b> tags) intended for ``theme.summary_box``.
    """
    if res.empty:
        return "No incidents match the selected filters. Try broadening your query."

    victims = int(res[C.COL_VICTIMS].sum())
    top_cat = res[C.COL_CATEGORY].value_counts().head(1)
    top_county = top_n(res[C.COL_COUNTY], 1)
    top_weapon = top_n(res[C.COL_WEAPON], 1)
    top_motive = top_n(res[C.COL_MOTIVE], 1)

    scope: list[str] = []
    if f.get("county", C.ALL) != C.ALL:
        scope.append(f"in {_b(f['county'])}")
    if f.get("category", C.ALL) != C.ALL:
        scope.append(f"for {_b(f['category'])} offences")
    scope_txt = " " + " ".join(scope) if scope else ""

    text = (
        f"Between {_b(f'{res[C.COL_DATE].min():%Y-%m-%d}')} and "
        f"{_b(f'{res[C.COL_DATE].max():%Y-%m-%d}')}, "
        f"{_b(f'{len(res):,} incidents')}{scope_txt} were reported in the media, "
        f"involving {_b(f'{victims:,} victims')} "
        f"(an average of {_b(f'{victims / len(res):.1f}')} per incident). "
        f"{_b(top_cat.index[0])} was the most frequent category "
        f"({top_cat.iloc[0]:,} incidents, "
        f"{round(top_cat.iloc[0] / len(res) * 100)}% of the selection)."
    )
    if len(top_county):
        text += (f" {_b(top_county.index[0])} recorded the highest number of "
                 f"incidents ({top_county.iloc[0]:,}).")

    text += _trend_sentence(res)
    text += _concentration_sentence(res)
    text += _severity_sentence(res)

    if len(top_weapon):
        text += (f" The most common recorded weapon was {_b(top_weapon.index[0])} "
                 f"({top_weapon.iloc[0]:,} cases)")
        if len(top_motive):
            text += (f", and the leading motive was {_b(top_motive.index[0])} "
                     f"({top_motive.iloc[0]:,} cases).")
        else:
            text += "."
    elif len(top_motive):
        text += (f" The leading recorded motive was {_b(top_motive.index[0])} "
                 f"({top_motive.iloc[0]:,} cases).")

    y25, y26 = len(res[res[C.COL_YEAR] == 2025]), len(res[res[C.COL_YEAR] == 2026])
    if y25 > 0 and y26 > 0:
        change = (y26 - y25) / y25 * 100
        text += (f" Year on year, 2026 has logged {_b(f'{y26:,}')} incidents against "
                 f"{_b(f'{y25:,}')} in 2025 ({change:+.0f}%, with 2026 still partial).")
    return text
