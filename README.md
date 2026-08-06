# Kenya CrimeLens (production refactor)

Interactive Streamlit BI platform for media-mined crime incidents across Kenya.

## Quick start
```bash
pip install -r requirements.txt
# place your cleaned_crime_data.csv in data/, or generate demo data:
python scripts_make_sample_data.py
streamlit run Home.py
```

## Project layout
```
Home.py                      Landing page (national overview + choropleth)
pages/
  1_Dashboard.py             Executive overview, analyst narrative, PDF briefing
  2_County_Analysis.py       County concentration, composition, scoreboard
  3_Offence_Analysis.py      Categories, offences, weapons, motives
  4_Victim_Profile.py        Victim gender, toll and deadliest incidents
  5_Perpetrator_Profile.py   Perpetrator counts, gender, group sizes
  6_Spatial_Analysis.py      Choropleth + bubble map, metric switch, ranking
  7_Data_Explorer.py         Search, browse, CSV / Excel export
utils/
  config.py                  Brand tokens, column names, shared constants
  loader.py                  Cached loading + validation of CSV and GeoJSON
  theme.py                   CSS design system and UI components
  filters.py                 Sidebar query panel (Analyze workflow preserved)
  analytics.py               KPIs, scoreboard, automatic narrative engine
  charts.py                  Plotly chart factory (choropleth, bars, donuts...)
  export.py                  CSV, styled Excel, PDF briefing
assets/
  kenya_counties.geojson     47 county boundaries, names matched to the dataset
```

## Notes
- The choropleth uses `assets/kenya_counties.geojson` (simplified, 174 KB,
  `properties.county` matches the dataset's county names). If the file is
  missing the app falls back to the bubble map automatically.
- Chart PNG download: camera icon in each chart toolbar.
- PDF briefing of the current query: Dashboard page.
- Figures reflect media-reported incidents, not official police statistics.

## This build ships with real data

`data/cleaned_crime_data.csv` is already generated from the raw Excel
(`CUMULATIVE MEDIA MINING DATA 2025-2026 (1).xlsx`) via `data_cleaning.py`
(1,530 incidents, 19 offence categories, Jan 2025 – Jul 2026). To regenerate:

```bash
python data_cleaning.py            # writes cleaned_crime_data.csv next to the script
mv cleaned_crime_data.csv data/    # the app reads from data/
```

The narrative engine drops an incomplete trailing month before computing the
trend, so a partial final month (e.g. mid-July) never shows as a fake drop.
