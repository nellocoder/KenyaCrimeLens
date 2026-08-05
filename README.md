# Kenya CrimeLens

**Media‑mined crime intelligence for Kenya**  
An interactive, multi‑page analytical application built with Streamlit and Plotly, drawing on 1,530+ media‑reported incidents from January 2025 to July 2026.

[![Built with Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b)](https://streamlit.io)
[![Charts: Plotly](https://img.shields.io/badge/charts-Plotly-0ea5e9)](https://plotly.com)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

---

## What’s new in this release (v2)

- **Analytical rigour** – Missing victim counts are no longer imputed to 1; they are left empty and reported transparently.  
- **Terminology** – “Deadliest incident” → “Incident with highest reported victim count”; “severity” → “average victims per incident”; “perpetrators” → “suspects / alleged perpetrators”.  
- **Crime rates** – Incident rates per 100,000 population using 2019 census data.  
- **Narrative engine** – Every filtered query is accompanied by an auto‑generated plain‑language summary with cautionary notes.  
- **Methodology page** – Transparent description of data sources, coding decisions, limitations, and media‑reporting bias.  
- **Restructured navigation** – Modules answer specific intelligence questions: *What? Where? When? Who?*

---

## Pages

| Module                     | Purpose                                                                 |
|----------------------------|-------------------------------------------------------------------------|
| **National Overview**      | Unfiltered picture of the entire dataset.                                 |
| **Executive Overview**     | Filtered KPIs, auto‑summary, trend and top‑level charts.                 |
| **Crime Trends**           | Monthly incidents & victim toll with 3‑month moving average, year‑on‑year change. |
| **Geography & Maps**       | County‑level bubble map, incident rates, county × offence heatmap.       |
| **Crime Types**            | Dominant offence categories, weapons, motives, and compositional breakdown. |
| **Victims**                | Victim demographics, gender distribution (incidents vs victim toll), burden by category. |
| **Suspects & Alleged Perpetrators** | Suspect counts, gender, group sizes, and offences linked.             |
| **Data Explorer**          | Full‑text search, browse filtered records, export to CSV / Excel.        |
| **Methodology**            | Data sources, definitions, completeness notes, and interpretation guide. |

---

## Sidebar query panel

Filters are grouped logically:

- **Time** – Year (multi‑select)
- **Geography** – County
- **Crime** – Offence category
- **Victim / Suspect** – Victim gender
- **Context** – Weapon, Motive

Click **Apply Filters** to update all pages. Active filters are displayed in the sidebar. A **Reset All** button clears the selection.

---

## Project structure
KenyaCrimeLens/
├── app.py                             # Entry point (National Overview, unfiltered)
├── pages/
│   ├── 1_Executive_Overview.py
│   ├── 2_Trends.py
│   ├── 3_Geography.py
│   ├── 4_Crime_Types.py
│   ├── 5_Victims.py
│   ├── 6_Suspects.py
│   ├── 7_Data_Explorer.py
│   └── 8_Methodology.py
├── utils/
│   ├── theme.py                       # Global CSS & shared UI components
│   ├── filters.py                     # Sidebar query panel & filter state
│   ├── loader.py                      # Cached data loading (no victim imputation)
│   ├── analytics.py                   # KPIs, narrative generation, crime rates
│   ├── charts.py                      # Plotly chart factory, county map, heatmap
│   └── population.py                  # Kenya county population (2019 census)
├── data/
│   └── cleaned_crime_data.csv         # Cleaned & categorized dataset
├── data_cleaning.py                   # Raw Excel → cleaned CSV pipeline
├── CUMULATIVE MEDIA MINING DATA 2025-2026 (1).xlsx   # Raw source
├── requirements.txt
└── README.md
