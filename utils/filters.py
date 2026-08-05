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
                        Media-mined crime intelligence · 2025–2026
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---- Branded navigation ----
        st.markdown('<div class="cl-side-label">ANALYSIS MODULES</div>', unsafe_allow_html=True)
        st.page_link("Home.py", label="National Overview", icon="🏠")
        st.page_link("pages/1_Executive_Overview.py", label="Executive Overview", icon="📊")
        st.page_link("pages/2_Trends.py", label="Crime Trends", icon="📈")
        st.page_link("pages/3_Geography.py", label="Geography & Maps", icon="🗺️")
        st.page_link("pages/4_Crime_Types.py", label="Crime Types", icon="📂")
        st.page_link("pages/5_Victims.py", label="Victims", icon="👥")
        st.page_link("pages/6_Suspects.py", label="Suspects", icon="🕵️")
        st.page_link("pages/7_Data_Explorer.py", label="Data Explorer", icon="🗃️")
        st.page_link("pages/8_Methodology.py", label="Methodology", icon="📖")

        st.divider()

        # ---- Filters ----
        st.markdown('<div class="cl-side-label">FILTERS</div>', unsafe_allow_html=True)

        with st.expander("⏱️ Time", expanded=True):
            years_all = sorted(df["Year"].unique())
            years = st.multiselect("Year", years_all, default=years_all, key="f_years")

        with st.expander("📍 Geography", expanded=True):
            county = st.selectbox("County", [ALL] + sorted(df["County"].unique()), key="f_county")

        with st.expander("📂 Crime", expanded=True):
            category = st.selectbox("Offence Category",
                                    [ALL] + sorted(df["Offence Category"].unique()), key="f_category")

        with st.expander("👥 Victim / Suspect", expanded=False):
            gender = st.selectbox("Victim Gender",
                                  [ALL] + sorted(df["Victim Gender"].unique()), key="f_gender")

        with st.expander("🔪 Context", expanded=False):
            weapon = st.selectbox("Weapon", [ALL] + sorted(df["Weapon"].unique()), key="f_weapon")
            motive = st.selectbox("Motive", [ALL] + sorted(df["Motive"].unique()), key="f_motive")

        c1, c2 = st.columns(2)
        analyze = c1.button("🔍 Apply Filters", type="primary", use_container_width=True)
        reset = c2.button("↺ Reset All", use_container_width=True)

        if st.session_state.get("applied"):
            active = st.session_state["applied"]
            st.markdown("**Active filters:**")
            active_str = []
            if active["years"] != years_all:
                active_str.append(f"Years: {active['years']}")
            if active["county"] != ALL:
                active_str.append(f"County: {active['county']}")
            if active["category"] != ALL:
                active_str.append(f"Category: {active['category']}")
            if active["gender"] != ALL:
                active_str.append(f"Victim gender: {active['gender']}")
            if active["weapon"] != ALL:
                active_str.append(f"Weapon: {active['weapon']}")
            if active["motive"] != ALL:
                active_str.append(f"Motive: {active['motive']}")
            if active_str:
                st.caption(" · ".join(active_str))
            else:
                st.caption("Showing all data (no filter applied)")

        st.divider()
        st.markdown('<div class="cl-side-label">DATASET</div>', unsafe_allow_html=True)
        st.caption(
            f"{len(df):,} media‑reported incidents  \n"
            f"{df['Date'].min():%Y-%m-%d} to {df['Date'].max():%Y-%m-%d}  \n"
            "Sources: Daily Nation, Standard, Star, People Daily, others"
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
