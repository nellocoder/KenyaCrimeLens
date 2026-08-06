"""Design system for Kenya CrimeLens.

Injects the global CSS theme and provides the shared UI components
(page headers, KPI cards, chart cards, summary box, filter chips)
used across all pages.

Visual signature: a Kenyan flag tri-stripe (black / red / green) that runs
under the page title and across the top of every KPI card, anchoring the
dashboard to its subject without shouting.
"""

from __future__ import annotations

import html

import streamlit as st

from utils import config as C

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', sans-serif;
}}
.stApp {{ background-color: {C.PAGE_BG}; }}
.block-container {{ padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1440px; }}

h1, h2, h3, .cl-header h1 {{ font-family: 'Archivo', 'Inter', sans-serif; }}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {C.KENYA_GREEN} 0%, {C.KENYA_GREEN_DARK} 100%);
    border-right: 1px solid rgba(0,0,0,0.2);
}}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {{ display: none; }}
section[data-testid="stSidebar"] > div:first-child {{ padding-top: 1.4rem; }}

section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {{
    border-radius: 8px; padding: 4px 10px; margin: 2px 0;
    border-left: 3px solid transparent; transition: background-color .15s ease;
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {{
    background-color: rgba(255,255,255,0.10);
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] p {{
    font-size: 0.92rem !important; font-weight: 500 !important;
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][disabled],
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-disabled="true"] {{
    background-color: rgba(255,255,255,0.14);
    border-left: 3px solid #facc15;
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][disabled] p,
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-disabled="true"] p {{
    color: #ffffff !important; font-weight: 700 !important;
}}

.cl-side-label {{
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: rgba(255,255,255,0.65);
    margin: 12px 0 2px 2px;
}}
section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] small {{ color: #e8f5ee !important; }}
section[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.18); }}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background-color: {C.KENYA_GREEN_DARK};
    border-color: rgba(255,255,255,0.25); color: #f1f5f9;
}}
section[data-testid="stSidebar"] div[data-baseweb="select"] span {{ color: #f1f5f9 !important; }}
section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
    background-color: {C.ACCENT};
}}
section[data-testid="stSidebar"] .stCaption, section[data-testid="stSidebar"] small {{
    color: rgba(255,255,255,0.70) !important;
}}
section[data-testid="stSidebar"] button[kind="primary"] {{
    background-color: {C.ACCENT}; border: none; color: #fff; font-weight: 600;
}}
section[data-testid="stSidebar"] button[kind="primary"]:hover {{ background-color: {C.ACCENT_LIGHT}; }}
section[data-testid="stSidebar"] button[kind="secondary"] {{
    background: transparent; border: 1px solid rgba(255,255,255,0.35); color: #d7e9de;
}}
section[data-testid="stSidebar"] button[kind="secondary"]:hover {{
    background: rgba(255,255,255,0.10); border-color: rgba(255,255,255,0.55);
}}

/* ---------- Page header with flag stripe ---------- */
.cl-header {{ display: flex; align-items: center; gap: 14px; margin-bottom: 2px; }}
.cl-header-icon {{
    background: linear-gradient(135deg, {C.ACCENT}, {C.ACCENT_LIGHT});
    border-radius: 12px; width: 46px; height: 46px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; box-shadow: 0 4px 10px rgba(2,132,199,0.30);
}}
.cl-header h1 {{ margin: 0; padding: 0; font-size: 1.85rem; font-weight: 800; color: {C.INK}; }}
.cl-stripe {{
    height: 4px; width: 120px; border-radius: 2px;
    background: {C.FLAG_STRIPE};
    margin: 8px 0 6px 60px;
}}
.cl-subtitle {{ color: {C.MUTED}; font-size: 0.95rem; margin: 0 0 1.1rem 60px; }}

/* ---------- KPI cards ---------- */
.kpi-card {{
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 16px 18px 14px 18px; height: 100%;
    border-top: 4px solid transparent;
    background-image: linear-gradient(#fff, #fff), {C.FLAG_STRIPE};
    background-origin: border-box; background-clip: padding-box, border-box;
    box-shadow: 0 1px 3px rgba(15,23,42,0.06);
    transition: box-shadow .15s ease, transform .15s ease;
}}
.kpi-card:hover {{ box-shadow: 0 6px 16px rgba(15,23,42,0.10); transform: translateY(-1px); }}
.kpi-label {{
    display: flex; align-items: center; gap: 6px;
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: {C.MUTED}; margin-bottom: 6px;
}}
.kpi-value {{
    font-size: 1.6rem; font-weight: 800; color: {C.INK}; line-height: 1.15;
    font-variant-numeric: tabular-nums;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}}
.kpi-sub {{ font-size: 0.78rem; color: #94a3b8; margin-top: 4px; }}
.kpi-delta-up {{ color: {C.KENYA_RED}; font-weight: 700; }}
.kpi-delta-down {{ color: {C.KENYA_GREEN}; font-weight: 700; }}

/* ---------- Summary box ---------- */
.summary-box {{
    background: #f0f9ff; border: 1px solid #bae6fd; border-left: 4px solid {C.ACCENT};
    border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;
}}
.summary-box .summary-title {{
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: #0369a1; margin-bottom: 6px;
}}
.summary-box .summary-text {{ color: #334155; font-size: 0.93rem; line-height: 1.65; }}

/* ---------- Chart cards ---------- */
.chart-card {{
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 14px 14px 4px 14px; margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.06);
}}
.chart-title {{
    font-size: 0.88rem; font-weight: 700; color: #1e293b; padding: 2px 6px 2px 6px;
}}
.chart-caption {{ font-size: 0.76rem; color: #94a3b8; padding: 0 6px 8px 6px; }}

/* ---------- Filter chips ---------- */
.cl-chips {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 14px 0; }}
.cl-chip {{
    background: #e0f2fe; color: #075985; border: 1px solid #bae6fd;
    border-radius: 999px; padding: 3px 12px; font-size: 0.78rem; font-weight: 600;
}}

div[data-testid="stAlert"] {{ border-radius: 10px; }}
div[data-testid="stDataFrame"] {{
    border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;
}}

/* ---------- Styled HTML table (pill categories, zebra rows) ---------- */
.cl-table-wrap {{
    border: 1px solid #e2e8f0; border-radius: 12px; overflow: auto;
    box-shadow: 0 1px 3px rgba(15,23,42,0.06); margin-bottom: 8px;
    max-height: 620px;
}}
.cl-table {{
    border-collapse: collapse; width: 100%; font-size: 0.9rem;
    color: {C.INK}; background: #ffffff;
}}
.cl-table thead th {{
    position: sticky; top: 0; z-index: 2;
    background: #f1f5f9; color: #475569; text-align: left;
    font-weight: 700; font-size: 0.82rem; letter-spacing: 0.01em;
    padding: 14px 16px; border-bottom: 1px solid #e2e8f0; white-space: nowrap;
}}
.cl-table tbody td {{
    padding: 12px 16px; border-bottom: 1px solid #eef2f6; vertical-align: middle;
}}
.cl-table tbody tr:nth-child(even) {{ background: #fafcff; }}
.cl-table tbody tr:hover {{ background: #f0f9ff; }}
.cl-table tbody tr:last-child td {{ border-bottom: none; }}
.cl-td-strong {{ font-weight: 600; color: {C.INK}; }}
.cl-td-muted {{ color: #94a3b8; }}
.cl-td-num {{ text-align: right; font-variant-numeric: tabular-nums; font-weight: 600; }}
.cl-pill {{
    display: inline-block; padding: 4px 12px; border-radius: 999px;
    color: #ffffff; font-size: 0.78rem; font-weight: 600; white-space: nowrap;
    line-height: 1.3;
}}

@media (max-width: 780px) {{
    .cl-header h1 {{ font-size: 1.4rem; }}
    .cl-subtitle, .cl-stripe {{ margin-left: 0; }}
    .kpi-value {{ font-size: 1.25rem; }}
}}
@media (prefers-reduced-motion: reduce) {{
    .kpi-card, section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {{
        transition: none;
    }}
}}
</style>
"""


def apply_theme() -> None:
    """Inject the global CSS theme. Call once per page, after set_page_config."""
    st.markdown(_CSS, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = "") -> None:
    """Branded page header: gradient icon tile, title, flag stripe, subtitle."""
    st.markdown(
        f"""
        <div class="cl-header">
            <div class="cl-header-icon">{icon}</div>
            <h1>{html.escape(title)}</h1>
        </div>
        <div class="cl-stripe"></div>
        <div class="cl-subtitle">{html.escape(subtitle)}</div>
        """,
        unsafe_allow_html=True,
    )


def org_banner(logo_b64: str | None) -> None:
    """Top-of-page identity strip: NCRC logo, owner name and product tagline."""
    logo_html = (
        f'<img src="{logo_b64}" alt="NCRC logo" '
        f'style="height:64px;width:auto;object-fit:contain;"/>'
        if logo_b64 else ""
    )
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:16px;
                    padding:6px 2px 14px 2px;border-bottom:1px solid #e2e8f0;
                    margin-bottom:18px;">
            {logo_html}
            <div>
                <div style="font-size:1.05rem;font-weight:800;color:{C.INK};
                            line-height:1.2;letter-spacing:0.01em;">
                    {C.APP_OWNER}
                </div>
                <div style="font-size:0.82rem;color:{C.MUTED};margin-top:2px;">
                    {C.APP_NAME} · {C.APP_TAGLINE}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_cards(cards: list[dict]) -> None:
    """Render a responsive row of KPI cards.

    Each card dict supports: icon, label, value, sub and an optional
    ``delta`` string prefixed with ``+`` or ``-`` (colour-coded: increases in
    crime are red, decreases green).
    """
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        delta = card.get("delta", "")
        delta_html = ""
        if delta:
            cls = "kpi-delta-up" if delta.startswith("+") else "kpi-delta-down"
            delta_html = f' <span class="{cls}">{html.escape(delta)}</span>'
        value = str(card["value"])
        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{card.get('icon', '')} {html.escape(card['label'])}</div>
                    <div class="kpi-value" title="{html.escape(value)}">{html.escape(value)}{delta_html}</div>
                    <div class="kpi-sub">{html.escape(str(card.get('sub', '')))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)


def summary_box(text_html: str) -> None:
    """Sky-tinted auto-analysis narrative box (text may contain <b> tags)."""
    st.markdown(
        f"""
        <div class="summary-box">
            <div class="summary-title">✨ Analysis summary</div>
            <div class="summary-text">{text_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_card(title: str, fig, height: int | None = None, caption: str = "") -> None:
    """Wrap a Plotly figure in a white card with a bold title.

    The toolbar (PNG download, zoom, pan) is hidden by default and appears
    only while the pointer is over the chart, keeping the visuals clean.
    """
    caption_html = f'<div class="chart-caption">{html.escape(caption)}</div>' if caption else ""
    st.markdown(
        f'<div class="chart-card"><div class="chart-title">{html.escape(title)}</div>{caption_html}',
        unsafe_allow_html=True,
    )
    if height:
        fig.update_layout(height=height)
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": "hover",
            "displaylogo": False,
            "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d",
                                       "zoomIn2d", "zoomOut2d"],
            "toImageButtonOptions": {"format": "png", "scale": 2},
        },
    )
    st.markdown("</div>", unsafe_allow_html=True)


def filter_chips(f: dict | None) -> None:
    """Show the applied query as a row of chips so context is never lost."""
    if not f:
        return
    chips: list[str] = []
    if f.get("years"):
        chips.append("Years: " + ", ".join(str(y) for y in f["years"]))
    for key, label in [("county", "County"), ("category", "Category"),
                       ("gender", "Victim gender"), ("weapon", "Weapon"),
                       ("motive", "Motive")]:
        if f.get(key) and f[key] != C.ALL:
            chips.append(f"{label}: {f[key]}")
    if not chips:
        chips.append("Scope: full dataset")
    html_chips = "".join(f'<span class="cl-chip">{html.escape(c)}</span>' for c in chips)
    st.markdown(f'<div class="cl-chips">{html_chips}</div>', unsafe_allow_html=True)


def info_banner() -> None:
    st.info(
        "Choose a county, offence category, year range or other filters in the "
        "sidebar, then click **Analyze**. Leave everything on 'All' for a "
        "national overview.",
        icon="🔍",
    )

def styled_table(
    df,
    pill_columns: dict[str, dict[str, str]] | None = None,
    muted_columns: tuple[str, ...] = (),
    numeric_columns: tuple[str, ...] = (),
    strong_columns: tuple[str, ...] = (),
    date_columns: tuple[str, ...] = (),
    max_rows: int | None = None,
) -> None:
    """Render a DataFrame as a styled HTML table matching the app design.

    Gray sticky header, zebra rows, hover highlight. Selected columns render
    as coloured pills (via ``pill_columns`` mapping each such column to a
    ``{value: hex_colour}`` dict), muted grey text, right-aligned numbers,
    bold emphasis, or formatted dates.

    Everything is HTML-escaped. Pass ``max_rows`` to cap very long tables.
    """
    import pandas as pd

    view = df.head(max_rows) if max_rows else df
    pill_columns = pill_columns or {}

    header = "".join(f"<th>{html.escape(str(c))}</th>" for c in view.columns)
    rows_html: list[str] = []
    for _, row in view.iterrows():
        cells: list[str] = []
        for col in view.columns:
            val = row[col]
            if col in pill_columns:
                key = str(val)
                colour = pill_columns[col].get(key, "#64748b")
                cells.append(
                    f'<td><span class="cl-pill" style="background:{colour}">'
                    f'{html.escape(key)}</span></td>'
                )
            elif col in date_columns:
                try:
                    txt = pd.to_datetime(val).strftime("%Y-%m-%d")
                except (ValueError, TypeError):
                    txt = html.escape(str(val))
                cells.append(f'<td class="cl-td-muted">{txt}</td>')
            elif col in numeric_columns:
                if pd.isna(val):
                    cells.append('<td class="cl-td-num cl-td-muted">—</td>')
                else:
                    num = int(val) if float(val).is_integer() else round(float(val), 2)
                    cells.append(f'<td class="cl-td-num">{num:,}</td>')
            elif col in muted_columns:
                txt = "—" if pd.isna(val) else html.escape(str(val))
                cells.append(f'<td class="cl-td-muted">{txt}</td>')
            elif col in strong_columns:
                cells.append(f'<td class="cl-td-strong">{html.escape(str(val))}</td>')
            else:
                cells.append(f"<td>{html.escape(str(val))}</td>")
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    table = (
        '<div class="cl-table-wrap"><table class="cl-table">'
        f"<thead><tr>{header}</tr></thead>"
        f"<tbody>{''.join(rows_html)}</tbody>"
        "</table></div>"
    )
    st.markdown(table, unsafe_allow_html=True)
    if max_rows and len(df) > max_rows:
        st.caption(f"Showing first {max_rows:,} of {len(df):,} rows. "
                   "Use the Data Explorer to export the full set.")
