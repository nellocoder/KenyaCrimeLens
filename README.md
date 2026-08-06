# Kenya CrimeLens

**Interactive business-intelligence platform for media-mined crime incidents across Kenya.**

Kenya CrimeLens turns the *Cumulative Media Mining Dataset 2025–2026* (1,530 incidents mined from Kenyan print media) into a query-driven analytics tool modelled on professional crime-intelligence dashboards. Set filters in the sidebar, and every page updates with KPIs, interactive Plotly visualisations, an automatically written analyst briefing, an accurate county choropleth, and one-click exports.

Built with [Streamlit](https://streamlit.io) and [Plotly](https://plotly.com/python/), and prepared for the **National Crime Research Centre**.

🔗 **Live app:** <https://kenyacrimelens.streamlit.app/>

![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b)
![Plotly](https://img.shields.io/badge/charts-Plotly-0ea5e9)
![Python](https://img.shields.io/badge/python-3.10%2B-3776ab)

---

## Table of contents

- [Highlights](#highlights)
- [Pages](#pages)
- [Quick start](#quick-start)
- [Project layout](#project-layout)
- [Data pipeline](#data-pipeline)
- [Deploying to Streamlit Community Cloud](#deploying-to-streamlit-community-cloud)
- [Design and engineering notes](#design-and-engineering-notes)
- [Data disclaimer](#data-disclaimer)

---

## Highlights

- **Loads by default.** Every page opens on the full national overview; the **Analyze** button is only needed to narrow the query.
- **Automatic analyst narrative.** A written briefing detects trend direction, month-over-month change, outlier months, geographic concentration and per-incident severity, rather than merely describing counts.
- **Accurate county choropleth.** A real Kenya GeoJSON (all 47 counties, names matched to the dataset) with incidents / victims / severity metrics, ranking and rich hovers, with an automatic bubble-map fallback.
- **Consistent visual language.** Deterministic, dataset-wide category colours shared across every chart, table pill and treemap, plus a Kenyan-flag design signature.
- **Styled data tables.** Coloured category pills, zebra rows and truncated case summaries (full text on hover).
- **Exports.** Per-chart PNG, filtered CSV, styled Excel, and a one-page PDF briefing of the current query.

---

## Pages

| Page | Contents |
|---|---|
| **Home** | National overview: KPIs, monthly trend with moving average, category and county rankings, county choropleth |
| **Dashboard** | Executive summary of the current query: KPIs, auto-written analyst briefing, trend, categories, counties, victim toll, and a downloadable PDF briefing |
| **County Analysis** | County rankings, county × category heatmap, treemap, victims-per-incident ratios, enriched county scoreboard |
| **Offence Analysis** | 19 offence categories, top specific offences, weapons, motives, category × offence treemap, category detail table |
| **Victim Profile** | Gender splits (incidents vs. toll), victim toll by category and month, deadliest incidents |
| **Perpetrator Profile** | Recorded perpetrator counts, gender, group sizes, category breakdown |
| **Spatial Analysis** | County choropleth and bubble map with a metric switch, ranking table, and top-county charts |
| **Data Explorer** | Full-text search across records, styled browse table, and CSV / Excel export |

### Sidebar query panel

Filter by **Year** (multi-select), **County**, **Offence Category**, **Victim Gender**, **Weapon** and **Motive**, apply with **Analyze**, and clear with **Reset**. A live match-count preview shows how many incidents the current selection returns before you apply it.

---

## Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. The cleaned dataset already ships in data/. To use your own,
#    place cleaned_crime_data.csv in data/ (see Data pipeline below).

# 3. Run the app
streamlit run Home.py
```

The app opens in your browser at `http://localhost:8501`.

**Requirements:** Python 3.10+. Core libraries are Streamlit, Plotly, pandas, numpy, openpyxl, XlsxWriter, reportlab and shapely (see `requirements.txt`).

---

## Project layout

```
Home.py                        Landing page (national overview + choropleth)
pages/
  1_Dashboard.py               Executive overview, analyst narrative, PDF briefing
  2_County_Analysis.py         County concentration, category heatmap, scoreboard
  3_Offence_Analysis.py        Categories, offences, weapons, motives
  4_Victim_Profile.py          Victim gender, toll, deadliest incidents
  5_Perpetrator_Profile.py     Perpetrator counts, gender, group sizes
  6_Spatial_Analysis.py        Choropleth + bubble map, metric switch, ranking
  7_Data_Explorer.py           Search, browse, CSV / Excel export
utils/
  config.py                    Brand tokens, column names, shared constants
  loader.py                    Cached loading + validation of CSV, GeoJSON, logo
  theme.py                     CSS design system and UI components
  filters.py                   Sidebar query panel (Analyze workflow preserved)
  analytics.py                 KPIs, scoreboard, automatic narrative engine
  charts.py                    Plotly chart factory (choropleth, bars, heatmap...)
  export.py                    CSV, styled Excel, PDF briefing
assets/
  kenya_counties.geojson       47 county boundaries, names matched to the dataset
  logo_ncrc.png                National Crime Research Centre logo
data/
  cleaned_crime_data.csv       Cleaned, categorised dataset (ships with the repo)
data_cleaning.py               Raw Excel -> cleaned CSV pipeline
requirements.txt
```

---

## Data pipeline

This build ships with real data. `data/cleaned_crime_data.csv` contains **1,530 incidents** across **19 offence categories**, spanning **January 2025 – July 2026**, generated from the raw Excel workbook (`CUMULATIVE MEDIA MINING DATA 2025-2026 (1).xlsx`) by `data_cleaning.py`.

To regenerate the cleaned data from the raw workbook:

```bash
python data_cleaning.py          # writes cleaned_crime_data.csv next to the script
mv cleaned_crime_data.csv data/  # the app reads from data/
```

The pipeline fixes the two-row Excel header, repairs day/month-transposed dates, standardises counties (towns mapped to counties, spelling corrected, multi-county entries grouped), normalises genders, weapons and motives, treats a missing victim tally as one victim, and maps 256 raw offence spellings into 19 offence categories.

For local testing without the real dataset, `scripts_make_sample_data.py` generates a small synthetic `data/cleaned_crime_data.csv` with the same schema.

---

## Deploying to Streamlit Community Cloud

1. Push this folder to a GitHub repository, keeping the structure above intact.
2. Go to <https://share.streamlit.io> and choose **New app**.
3. Select the repository and branch, set the main file path to `Home.py`, and click **Deploy**.

The live deployment is available at <https://kenyacrimelens.streamlit.app/>.

---

## Design and engineering notes

- **Choropleth.** Uses `assets/kenya_counties.geojson` (simplified to ~174 KB; its `properties.county` values match the dataset's county names). If the file is missing, the app falls back to the bubble map automatically.
- **Category colours** are assigned once against the full dataset, so every category keeps the same colour across all charts, table pills and treemaps regardless of the active filter.
- **Narrative robustness.** The narrative engine drops an incomplete trailing month before computing the trend, so a partial final month (for example mid-July) never registers as a false drop or outlier.
- **Exports.** Every chart can be saved as a PNG via the camera icon that appears on hover; the Dashboard produces a one-page PDF briefing of the current query; the Data Explorer exports the filtered records to CSV or styled Excel.
- **Codebase.** Modular `utils/` package, cached data loading, type hints and docstrings throughout, and a single shared design system so pages stay thin.

---

## Data disclaimer

- Figures reflect **media-reported incidents**, not official police statistics, and are indicative rather than authoritative.
- A missing victim count is treated as one victim.
- County centroids used by the bubble map are approximate; records marked *Unknown*, *Multiple Counties*, *Nationwide* or *Outside Kenya* cannot be placed on the map.
