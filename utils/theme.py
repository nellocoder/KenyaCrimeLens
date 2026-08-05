"""
Design system for Kenya CrimeLens.
Injects the global CSS theme and provides shared UI components
(KPI cards, summary box, section headers) used across all pages.
"""

import streamlit as st

# Brand colors
SIDEBAR_BG = "#009639"      # Kenyan flag green (Pantone 355 C)
ACCENT = "#0284c7"          # sky-600
ACCENT_LIGHT = "#0ea5e9"    # sky-500
PAGE_BG = "#f8fafc"         # slate-50

# Derived sidebar elements
SIDEBAR_HOVER = "rgba(255, 255, 255, 0.08)"
SIDEBAR_ACTIVE_BG = "rgba(255, 255, 255, 0.12)"
SIDEBAR_ACTIVE_BORDER = "#66bb6a"   # soft green highlight
SIDEBAR_INPUT_BG = "#005a27"        # deep green for dropdowns / inputs
SIDEBAR_INPUT_BORDER = "#007b33"    # slightly lighter green border

CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', sans-serif;
}}

.stApp {{ background-color: {PAGE_BG}; }}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {{
    background-color: {SIDEBAR_BG};
    border-right: 1px solid rgba(0, 0, 0, 0.15);
}}

/* Hide the default page menu - replaced by branded nav in filters.py */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {{
    display: none;
}}
section[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1.5rem;
}}

/* Branded navigation links (st.page_link) */
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {{
    border-radius: 8px;
    padding: 4px 10px;
    margin: 2px 0;
    border-left: 3px solid transparent;
    transition: background-color 0.15s ease;
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {{
    background-color: {SIDEBAR_HOVER};
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] p {{
    font-size: 0.92rem !important;
    font-weight: 500 !important;
}}
/* Active page */
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][disabled],
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-disabled="true"] {{
    background-color: {SIDEBAR_ACTIVE_BG};
    border-left: 3px solid {SIDEBAR_ACTIVE_BORDER};
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][disabled] p,
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-disabled="true"] p {{
    color: #ffffff !important;
    font-weight: 700 !important;
}}

/* Section labels inside the sidebar */
.cl-side-label {{
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.6);
    margin: 10px 0 2px 2px;
}}

/* General sidebar typography */
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] small {{
    color: #e2e8f0 !important;
}}
section[data-testid="stSidebar"] hr {{ border-color: rgba(255, 255, 255, 0.15); }}

/* Sidebar inputs (select, multiselect) */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background-color: {SIDEBAR_INPUT_BG};
    border-color: {SIDEBAR_INPUT_BORDER};
    color: #f1f5f9;
}}
section[data-testid="stSidebar"] div[data-baseweb="select"] span {{
    color: #f1f5f9 !important;
}}
section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
    background-color: {ACCENT};
}}

/* Sidebar caption text */
section[data-testid="stSidebar"] .stCaption, section[data-testid="stSidebar"] small {{
    color: rgba(255, 255, 255, 0.65) !important;
}}

/* Buttons */
section[data-testid="stSidebar"] button[kind="primary"],
div[data-testid="stSidebar"] button[kind="primary"] {{
    background-color: {ACCENT};
    border: none;
    color: white;
    font-weight: 600;
}}
section[data-testid="stSidebar"] button[kind="primary"]:hover {{
    background-color: {ACCENT_LIGHT};
    border: none;
}}
section[data-testid="stSidebar"] button[kind="secondary"] {{
    background-color: transparent;
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: #cbd5e1;
}}
section[data-testid="stSidebar"] button[kind="secondary"]:hover {{
    background-color: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.5);
}}

/* ---------- Page headers ---------- */
.cl-header {{
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 4px;
}}
.cl-header-icon {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT_LIGHT});
    border-radius: 12px;
    width: 46px; height: 46px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    box-shadow: 0 4px 10px rgba(2, 132, 199, 0.35);
}}
.cl-header h1 {{
    margin: 0; padding: 0;
    font-size: 1.9rem; font-weight: 800; color: #0f172a;
}}
.cl-subtitle {{ color: #64748b; font-size: 0.95rem; margin-bottom: 1.2rem; }}

/* ---------- KPI cards ---------- */
.kpi-card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
    height: 100%;
}}
.kpi-label {{
    display: flex; align-items: center; gap: 6px;
    font-size: 0.72rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.06em;
    color: #64748b; margin-bottom: 6px;
}}
.kpi-value {{
    font-size: 1.65rem; font-weight: 800; color: #0f172a;
    line-height: 1.15;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}}
.kpi-sub {{ font-size: 0.78rem; color: #94a3b8; margin-top: 4px; }}

/* ---------- Summary box ---------- */
.summary-box {{
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
}}
.summary-box .summary-title {{
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em;
    color: #0369a1; margin-bottom: 6px;
}}
.summary-box .summary-text {{ color: #334155; font-size: 0.92rem; line-height: 1.6; }}

/* ---------- Chart cards ---------- */
.chart-card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 14px 14px 4px 14px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
    margin-bottom: 16px;
}}
.chart-title {{
    font-size: 0.88rem; font-weight: 700; color: #1e293b;
    padding: 2px 6px 8px 6px;
}}

/* Info banner tweak */
div[data-testid="stAlert"] {{ border-radius: 10px; }}

/* Dataframe border */
div[data-testid="stDataFrame"] {{
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
}}
</style>
"""


def apply_theme():
    """Inject the global CSS theme. Call once per page, after set_page_config."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    """Branded page header with gradient icon tile."""
    st.markdown(
        f"""
        <div class="cl-header">
            <div class="cl-header-icon">{icon}</div>
            <h1>{title}</h1>
        </div>
        <div class="cl-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def kpi_cards(cards: list[dict]):
    """
    Render a row of KPI cards.
    cards: list of dicts with keys: icon, label, value, sub
    """
    cols = st.columns(len(cards))
    for col, c in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{c['icon']} {c['label']}</div>
                    <div class="kpi-value" title="{c['value']}">{c['value']}</div>
                    <div class="kpi-sub">{c['sub']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)


def summary_box(text: str):
    """Sky-tinted auto-analysis summary box."""
    st.markdown(
        f"""
        <div class="summary-box">
            <div class="summary-title">✨ Analysis summary</div>
            <div class="summary-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_card(title: str, fig, height: int | None = None):
    """Wrap a Plotly figure in a white card with a bold title."""
    st.markdown(f'<div class="chart-card"><div class="chart-title">{title}</div>',
                unsafe_allow_html=True)
    if height:
        fig.update_layout(height=height)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


def info_banner():
    st.info(
        "Choose a county, offence category, year range or other filters in the "
        "sidebar, then click **Analyze**. Leave everything on 'All' for a "
        "national overview.",
        icon="🔍",
    )
