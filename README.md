# Kenya CrimeLens

A professional, multi-page interactive dashboard for analysing media-mined crime
incidents across Kenya (January 2025 – July 2026), built with **Streamlit** and **Plotly**.

![Stack](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b)
![Charts](https://img.shields.io/badge/charts-Plotly-0ea5e9)

## What it does

The app turns the Cumulative Media Mining Dataset 2025–2026 (1,530 incidents mined from
Kenyan print media) into a query-driven analytics tool modelled on crime-intelligence
dashboards: you set filters in the sidebar, click **Analyze**, and every page updates.

### Pages

| Page | Contents |
|---|---|
| **Home** | National overview: KPIs, monthly trend, category and county rankings |
| **Dashboard** | Auto-written analysis summary, KPIs, trend, categories, counties, gender, weapons, motives |
| **County Analysis** | County rankings, county × category stacked bars, treemap, county scoreboard |
| **Offence Analysis** | 19 offence categories, top-20 specific offences, treemap, offence scoreboard |
| **Victim Profile** | Gender splits (incidents vs toll), victim toll by category and month, deadliest incidents |
| **Perpetrator Profile** | Recorded perpetrator counts, gender, group sizes, category breakdown |
| **Spatial Analysis** | Interactive bubble map of Kenya (no map token needed) plus rankings |
| **Data Explorer** | Full-text search across case summaries, browse records, export to CSV / Excel |

### Sidebar query panel

Year (multi-select), County, Offence Category, Victim Gender, Weapon and Motive —
applied with an **Analyze** button, cleared with **Reset**.

## Project structure

```
├── Home.py                       # Landing page (entry point)
├── pages/                        # The 7 analytical modules
├── utils/
│   ├── theme.py                  # Design system (CSS, KPI cards, chart cards)
│   ├── filters.py                # Sidebar query panel + filter state
│   ├── loader.py                 # Cached data loading
│   ├── analytics.py              # KPIs, top-N, auto-generated summaries
│   └── charts.py                 # Unified Plotly chart factory + county map
├── data/
│   └── cleaned_crime_data.csv    # Cleaned, categorized dataset
├── data_cleaning.py              # Raw Excel -> cleaned CSV pipeline
├── CUMULATIVE MEDIA MINING DATA 2025-2026 (1).xlsx   # Raw source
└── requirements.txt
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repository (keep the structure exactly as above).
2. Go to <https://share.streamlit.io> → **New app**.
3. Pick the repo, branch `main`, main file path `Home.py` → **Deploy**.

## Reproduce the cleaned data

```bash
python data_cleaning.py   # reads the raw Excel, writes data/cleaned_crime_data.csv
```

The pipeline fixes the two-row header, repairs day/month-transposed dates,
standardizes counties (towns mapped to counties, spelling mistakes corrected,
multi-county entries grouped), normalizes genders/weapons/motives, treats a
missing victim tally as 1, and maps 256 raw offence spellings into 19 offence
categories.

## Data notes

- Figures reflect **media-reported incidents**, not official police statistics.
- A missing victim count is treated as 1 victim.
- County coordinates on the map are approximate centroids; records marked
  "Unknown", "Multiple Counties", "Nationwide" or "Outside Kenya" are unmappable.
