"""Data Explorer: search, browse and export the filtered incident records."""

from io import BytesIO

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Data Explorer · Kenya CrimeLens", page_icon="🗃️", layout="wide")

from utils.loader import load_data
from utils.theme import apply_theme, page_header, info_banner
from utils.filters import render_sidebar, get_filtered

apply_theme()
df = load_data()
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

# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------
search = st.text_input("🔎 Search incidents",
                       placeholder="e.g. murder, Nairobi, firearm, land dispute...")
table = res.sort_values("Date", ascending=False)
if search:
    q = search.lower()
    haystack = (table[["Offence", "County", "Offence Category", "Case Summary",
                       "Motive", "Weapon", "Source"]]
                .astype(str).agg(" ".join, axis=1).str.lower())
    table = table[haystack.str.contains(q, regex=False)]

st.caption(f"Showing **{len(table):,}** of {len(res):,} records from the current query")

cols = ["Date", "County", "Offence Category", "Offence", "Victim Tally",
        "Victim Gender", "Perpetrator Tally", "Weapon", "Motive", "Source",
        "Case Summary"]

st.dataframe(
    table[cols],
    use_container_width=True,
    hide_index=True,
    height=520,
    column_config={
        "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
        "Victim Tally": st.column_config.NumberColumn("Victims"),
        "Perpetrator Tally": st.column_config.NumberColumn("Perpetrators"),
        "Case Summary": st.column_config.TextColumn("Case Summary", width="large"),
    },
)

# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
st.subheader("Export")
e1, e2 = st.columns(2)

csv_bytes = table[cols].to_csv(index=False).encode("utf-8")
e1.download_button("⬇ Download as CSV", data=csv_bytes,
                   file_name="kenya_crimelens_incidents.csv", mime="text/csv",
                   use_container_width=True)

buf = BytesIO()
with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
    table[cols].to_excel(writer, index=False, sheet_name="Incidents")
e2.download_button("⬇ Download as Excel", data=buf.getvalue(),
                   file_name="kenya_crimelens_incidents.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                   use_container_width=True)
