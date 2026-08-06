"""Sidebar query panel for Kenya CrimeLens.

Workflow preserved from the original app: set filters, click Analyze,
results update on every page. New in this version: a live match-count
preview under the filters, and applied filters exposed for chip display.

Call ``render_sidebar(df)`` at the top of every page, then ``get_filtered(df)``.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils import config as C
from utils.loader import load_logo_b64

_FILTER_KEYS = ("years", "county", "category", "gender", "weapon", "motive")


def _options(df: pd.DataFrame, col: str) -> list[str]:
    return [C.ALL] + sorted(df[col].dropna().unique())


def _preview_count(df: pd.DataFrame, f: dict) -> int:
    """Cheap row count for the pending (not yet applied) selection."""
    return len(_apply(df, f))


def _apply(df: pd.DataFrame, f: dict) -> pd.DataFrame:
    res = df[df[C.COL_YEAR].isin(f["years"])] if f["years"] else df.iloc[0:0]
    pairs = [
        ("county", C.COL_COUNTY), ("category", C.COL_CATEGORY),
        ("gender", C.COL_VICTIM_GENDER), ("weapon", C.COL_WEAPON),
        ("motive", C.COL_MOTIVE),
    ]
    for key, col in pairs:
        if f[key] != C.ALL:
            res = res[res[col] == f[key]]
    return res


def render_sidebar(df: pd.DataFrame) -> None:
    """Render the branded sidebar: logo, navigation, query panel, dataset facts."""
    with st.sidebar:
        logo = load_logo_b64()
        if logo:
            brand_mark = (
                f'<div style="background:#ffffff;border-radius:12px;width:46px;'
                f'height:46px;display:flex;align-items:center;justify-content:center;'
                f'box-shadow:0 3px 8px rgba(0,0,0,0.25);padding:4px;">'
                f'<img src="{logo}" alt="NCRC logo" '
                f'style="max-width:100%;max-height:100%;object-fit:contain;"/></div>'
            )
        else:
            brand_mark = (
                f'<div style="background:linear-gradient(135deg,{C.ACCENT},'
                f'{C.ACCENT_LIGHT});border-radius:11px;width:46px;height:46px;'
                f'display:flex;align-items:center;justify-content:center;'
                f'font-size:20px;box-shadow:0 3px 8px rgba(2,132,199,0.4);">🔍</div>'
            )
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:12px;padding:2px 2px 6px 2px;">
                {brand_mark}
                <div>
                    <div style="font-size:1.2rem;font-weight:800;color:#ffffff;line-height:1.1;">
                        {C.APP_NAME}
                    </div>
                    <div style="font-size:0.72rem;color:rgba(255,255,255,0.75);margin-top:2px;">
                        {C.APP_OWNER}
                    </div>
                </div>
            </div>
            <div style="height:3px;width:100%;border-radius:2px;margin:6px 0 2px 0;
                        background:{C.FLAG_STRIPE};"></div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="cl-side-label">Menu</div>', unsafe_allow_html=True)
        st.page_link("Home.py", label="Home", icon="🏠")
        st.page_link("pages/1_Dashboard.py", label="Dashboard", icon="📊")
        st.page_link("pages/2_County_Analysis.py", label="County Analysis", icon="📍")
        st.page_link("pages/3_Offence_Analysis.py", label="Offence Analysis", icon="📂")
        st.page_link("pages/4_Victim_Profile.py", label="Victim Profile", icon="👥")
        st.page_link("pages/5_Perpetrator_Profile.py", label="Perpetrator Profile", icon="🕵️")
        st.page_link("pages/6_Spatial_Analysis.py", label="Spatial Analysis", icon="🗺️")
        st.page_link("pages/7_Data_Explorer.py", label="Data Explorer", icon="🗃️")

        st.divider()
        st.markdown('<div class="cl-side-label">Query</div>', unsafe_allow_html=True)

        years_all = sorted(df[C.COL_YEAR].unique())
        pending = {
            "years": st.multiselect("Year", years_all, default=years_all, key="f_years"),
            "county": st.selectbox("County", _options(df, C.COL_COUNTY), key="f_county"),
            "category": st.selectbox("Offence Category", _options(df, C.COL_CATEGORY),
                                     key="f_category"),
            "gender": st.selectbox("Victim Gender", _options(df, C.COL_VICTIM_GENDER),
                                   key="f_gender"),
            "weapon": st.selectbox("Weapon", _options(df, C.COL_WEAPON), key="f_weapon"),
            "motive": st.selectbox("Motive", _options(df, C.COL_MOTIVE), key="f_motive"),
        }

        st.caption(f"Matches for this selection: **{_preview_count(df, pending):,}** incidents")

        c1, c2 = st.columns(2)
        analyze = c1.button("🔍 Analyze", type="primary", use_container_width=True)
        reset = c2.button("↺ Reset", use_container_width=True)

        st.divider()
        st.markdown('<div class="cl-side-label">Dataset</div>', unsafe_allow_html=True)
        st.caption(
            f"{len(df):,} incidents mined from Kenyan print media  \n"
            f"{df[C.COL_DATE].min():%Y-%m-%d} to {df[C.COL_DATE].max():%Y-%m-%d}  \n"
            "Sources: Daily Nation, The Standard, The Star, People Daily and others"
        )
        st.caption(f"Note: {C.DATA_DISCLAIMER}")

    if reset:
        st.session_state.pop("applied", None)
        st.rerun()

    if analyze:
        if not pending["years"]:
            st.sidebar.warning("Select at least one year.")
        else:
            st.session_state["applied"] = pending


def default_query(df: pd.DataFrame) -> dict:
    """The unfiltered national view used before the user clicks Analyze."""
    return {
        "years": sorted(df[C.COL_YEAR].unique()),
        "county": C.ALL, "category": C.ALL, "gender": C.ALL,
        "weapon": C.ALL, "motive": C.ALL,
    }


def get_filtered(df: pd.DataFrame) -> pd.DataFrame:
    """Return the filtered DataFrame for the applied query.

    Before the user clicks Analyze, this falls back to the full national view
    so every page loads immediately with data. Once Analyze is clicked, the
    user's selection is applied instead.
    """
    f = st.session_state.get("applied") or default_query(df)
    return _apply(df, f)


def active_filters(df: pd.DataFrame | None = None) -> dict | None:
    """The applied filter dict, or the default national query before Analyze.

    Passing ``df`` returns the default query (for chip display) when nothing
    has been applied yet; omitting it preserves the old None-before-Analyze
    behaviour for callers that want to distinguish the two states.
    """
    applied = st.session_state.get("applied")
    if applied is not None:
        return applied
    return default_query(df) if df is not None else None
