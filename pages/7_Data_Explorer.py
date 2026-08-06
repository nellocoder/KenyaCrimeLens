"""Data Explorer: search, browse and export the filtered incident records."""

import streamlit as st

st.set_page_config(page_title="Data Explorer · Kenya CrimeLens", page_icon="🗃️",
                   layout="wide")

from utils import charts
from utils import config as C
from utils import export
from utils.filters import active_filters, get_filtered, render_sidebar
from utils.loader import load_data
from utils.theme import (apply_theme, filter_chips, info_banner, page_header,
                         styled_table)

apply_theme()
df = load_data()
if df.empty:
    st.stop()
render_sidebar(df)

page_header("🗃️", "Data Explorer",
            "Search the incident records behind your query and export them for reporting")

res = get_filtered(df)
if res is None:
    info_banner()
    st.stop()
if res.empty:
    st.warning("No incidents match the selected filters.")
    st.stop()

filter_chips(active_filters())

# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------
search = st.text_input("🔎 Search incidents",
                       placeholder="e.g. murder, Nairobi, firearm, land dispute...")
table = res.sort_values(C.COL_DATE, ascending=False)
if search:
    q = search.lower()
    haystack = (table[[C.COL_OFFENCE, C.COL_COUNTY, C.COL_CATEGORY, C.COL_SUMMARY,
                       C.COL_MOTIVE, C.COL_WEAPON, C.COL_SOURCE]]
                .astype(str).agg(" ".join, axis=1).str.lower())
    table = table[haystack.str.contains(q, regex=False)]

st.caption(f"Showing **{len(table):,}** of {len(res):,} records from the current query")

# Compact view matching the app's styled table (pills, muted secondary fields).
# The full column set is preserved in the exports below.
display_cols = [C.COL_DATE, C.COL_COUNTY, C.COL_CATEGORY, C.COL_OFFENCE,
                C.COL_VICTIMS, C.COL_WEAPON, C.COL_MOTIVE]
cat_colors = charts.category_colors(res[C.COL_CATEGORY].unique())
styled_table(
    table[display_cols].rename(columns={C.COL_VICTIMS: "Victims"}),
    pill_columns={C.COL_CATEGORY: cat_colors},
    strong_columns=(C.COL_OFFENCE,),
    numeric_columns=("Victims",),
    muted_columns=(C.COL_WEAPON, C.COL_MOTIVE),
    date_columns=(C.COL_DATE,),
    max_rows=250,
)

# Full record set (all columns) available on demand and in exports.
export_cols = [C.COL_DATE, C.COL_COUNTY, C.COL_CATEGORY, C.COL_OFFENCE, C.COL_VICTIMS,
               C.COL_VICTIM_GENDER, C.COL_PERPS, C.COL_WEAPON, C.COL_MOTIVE,
               C.COL_SOURCE, C.COL_SUMMARY]
with st.expander("Show all columns (including case summaries) in a sortable grid"):
    st.dataframe(
        table[export_cols],
        use_container_width=True,
        hide_index=True,
        height=520,
        column_config={
            C.COL_DATE: st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            C.COL_VICTIMS: st.column_config.NumberColumn("Victims"),
            C.COL_PERPS: st.column_config.NumberColumn("Perpetrators"),
            C.COL_SUMMARY: st.column_config.TextColumn("Case Summary", width="large"),
        },
    )

cols = export_cols

# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
st.subheader("Export")
e1, e2 = st.columns(2)

with st.spinner("Preparing exports..."):
    csv_bytes = export.to_csv_bytes(table[cols])
    xlsx_bytes = export.to_excel_bytes(table[cols])

e1.download_button("⬇ Download as CSV", data=csv_bytes,
                   file_name="kenya_crimelens_incidents.csv", mime="text/csv",
                   use_container_width=True)
e2.download_button("⬇ Download as Excel", data=xlsx_bytes,
                   file_name="kenya_crimelens_incidents.xlsx",
                   mime=("application/vnd.openxmlformats-officedocument."
                         "spreadsheetml.sheet"),
                   use_container_width=True)

st.caption(
    "Charts across the app can be saved as PNG images via the camera icon in "
    "each chart's toolbar. A PDF briefing of the current query is available on "
    "the Dashboard page."
)
