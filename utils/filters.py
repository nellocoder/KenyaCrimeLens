"""
Sidebar query panel for Kenya CrimeLens.
Replicates the CrimeLens workflow: set filters -> click Analyze -> results update.
Call render_sidebar(df) at the top of every page; then call get_filtered(df).
"""

import pandas as pd
import streamlit as st

ALL = "All"


def render_sidebar(df: pd.DataFrame):
    """Render the branded sidebar with the query panel. Returns nothing."""
    with st.sidebar:
        # ---- Brand ----
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:12px;padding:2px 2px 6px 2px;">
                <div style="background:linear-gradient(135deg,#0284c7,#0ea5e9);
                            border-radius:11px;width:42px;height:42px;display:flex;
                            align-items:center;justify-content:center;font-size:20px;
                            box-shadow:0 3px 8px rgba(2,132,199,0.4);">
                    🔍
                </div>
                <div>
                    <div style="font-size:1.2rem;font-weight:800;color:#f1f5f9;line-height:1.1;">
                        Kenya CrimeLens
                    </div>
                    <div style="font-size:0.72rem;color:#94a3b8;margin-top:2px;">
                        Media-mined crime data analysis · 2025–2026
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---- Branded navigation (native menu is hidden in theme CSS) ----
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

        # ---- Query panel ----
        st.markdown('<div class="cl-side-label">Query</div>', unsafe_allow_html=True)

        years_all = sorted(df["Year"].unique())
        years = st.multiselect("Year", years_all, default=years_all, key="f_years")
        county = st.selectbox("County", [ALL] + sorted(df["County"].unique()), key="f_county")
        category = st.selectbox("Offence Category",
                                [ALL] + sorted(df["Offence Category"].unique()), key="f_category")
        gender = st.selectbox("Victim Gender",
                              [ALL] + sorted(df["Victim Gender"].unique()), key="f_gender")
        weapon = st.selectbox("Weapon", [ALL] + sorted(df["Weapon"].unique()), key="f_weapon")
        motive = st.selectbox("Motive", [ALL] + sorted(df["Motive"].unique()), key="f_motive")

        c1, c2 = st.columns(2)
        analyze = c1.button("🔍 Analyze", type="primary", use_container_width=True)
        reset = c2.button("↺ Reset", use_container_width=True)

        st.divider()
        st.markdown('<div class="cl-side-label">Dataset</div>', unsafe_allow_html=True)
        st.caption(
            f"{len(df):,} incidents mined from Kenyan print media  \n"
            f"{df['Date'].min():%Y-%m-%d} to {df['Date'].max():%Y-%m-%d}  \n"
            "Sources: Daily Nation, The Standard, The Star, People Daily and others"
        )
        st.caption(
            "Note: figures reflect media-reported incidents, not official police "
            "statistics. A missing victim count is treated as 1."
        )

    if reset:
        st.session_state.pop("applied", None)
        st.rerun()

    if analyze:
        if not years:
            st.sidebar.warning("Select at least one year.")
        else:
            st.session_state["applied"] = {
                "years": years, "county": county, "category": category,
                "gender": gender, "weapon": weapon, "motive": motive,
            }


def get_filtered(df: pd.DataFrame) -> pd.DataFrame | None:
    """Return the filtered dataframe for the applied query, or None if not yet run."""
    f = st.session_state.get("applied")
    if f is None:
        return None

    res = df[df["Year"].isin(f["years"])]
    if f["county"] != ALL:
        res = res[res["County"] == f["county"]]
    if f["category"] != ALL:
        res = res[res["Offence Category"] == f["category"]]
    if f["gender"] != ALL:
        res = res[res["Victim Gender"] == f["gender"]]
    if f["weapon"] != ALL:
        res = res[res["Weapon"] == f["weapon"]]
    if f["motive"] != ALL:
        res = res[res["Motive"] == f["motive"]]
    return res


def active_filters() -> dict | None:
    return st.session_state.get("applied")