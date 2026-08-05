# 🇰🇪 Kenya CrimeLens

### Media-mined crime intelligence and analytical insights for Kenya

**Kenya CrimeLens** is an interactive crime intelligence and research application built with **Streamlit**, **Plotly**, and **Python**. It analyses **1,530+ media-reported crime incidents** recorded between **January 2025 and July 2026**, transforming structured media-mining data into interactive intelligence on crime trends, geographic concentration, offence types, victims, and suspects.

<p align="center">

<a href="https://kenyacrimelens.streamlit.app/">
  <img src="https://img.shields.io/badge/🚀%20LIVE%20DEMO-Kenya%20CrimeLens-009639?style=for-the-badge" alt="Live Demo">
</a>

</p>

<p align="center">

<a href="https://streamlit.io/">
<img src="https://img.shields.io/badge/Framework-Streamlit-ff4b4b?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
</a>
<a href="https://plotly.com/python/">
<img src="https://img.shields.io/badge/Visualisation-Plotly-3F4F75?style=flat-square" alt="Plotly">
</a>
<img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Data-1,530%2B%20incidents-009639?style=flat-square" alt="Dataset">
<img src="https://img.shields.io/badge/Coverage-Jan%202025--Jul%202026-0066CC?style=flat-square" alt="Coverage">
<img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT License">

</p>

---

## 📊 Dashboard Preview

<p align="center">
  <img src="assets/dashboard-overview.png" alt="Kenya CrimeLens Dashboard Overview" width="100%">
</p>

> **Tip:** Add your best screenshot to `assets/dashboard-overview.png`. Ideally, use the Executive Overview page showing the KPI cards, key findings, trend chart, and geographic visualisation.

### More views

| Executive Overview                                   | Crime Trends                             |
| ---------------------------------------------------- | ---------------------------------------- |
| ![Executive Overview](assets/executive-overview.png) | ![Crime Trends](assets/crime-trends.png) |

| Geography & Maps                   | Crime Types                            |
| ---------------------------------- | -------------------------------------- |
| ![Geography](assets/geography.png) | ![Crime Types](assets/crime-types.png) |

| Victims                        | Data Explorer                              |
| ------------------------------ | ------------------------------------------ |
| ![Victims](assets/victims.png) | ![Data Explorer](assets/data-explorer.png) |

---

# 🎯 What is Kenya CrimeLens?

Kenya CrimeLens converts media-mined crime records into an interactive analytical environment for exploring:

* **What** crimes are being reported?
* **Where** are reported incidents concentrated?
* **When** are patterns changing?
* **Who** are the reported victims?
* **Who** are the reported suspects or alleged perpetrators?
* **How** do crime patterns differ across counties and periods?

The application combines descriptive analytics, geographic analysis, population-adjusted rates, interactive visualisation, automated narrative summaries, and record-level exploration.

---

# ✨ Key Features

<table>
<tr>
<td width="50%">

### 📈 Crime Trends

Explore monthly and periodic changes in reported incidents and victim counts, including moving averages and period comparisons.

</td>
<td width="50%">

### 🗺️ Geographic Intelligence

Analyse county-level concentrations, incident rates, and offence patterns using interactive maps and spatial visualisations.

</td>
</tr>

<tr>
<td width="50%">

### 🔎 Crime Typologies

Explore offence categories, weapons, motives, and the composition of reported crime across locations and periods.

</td>
<td width="50%">

### 👥 Victim Analysis

Examine reported victim counts, gender distributions, victim burden, and differences between incident-level and victim-level measures.

</td>
</tr>

<tr>
<td width="50%">

### 🕵️ Suspect Analysis

Explore reported suspect counts, gender, group sizes, and offence associations while maintaining appropriate caution around allegations.

</td>
<td width="50%">

### 🧠 Narrative Intelligence

Automatically generate plain-language summaries that help users move from charts and statistics to interpretable findings.

</td>
</tr>

<tr>
<td width="50%">

### 📊 Crime Rates

Compare absolute incident counts with population-adjusted reported incident rates per 100,000 population using 2019 census data.

</td>
<td width="50%">

### 🔍 Data Explorer

Search, filter, inspect, and export the underlying records in CSV or Excel format.

</td>
</tr>
</table>

---

# 🧭 Analytical Framework

Kenya CrimeLens is organised around four core intelligence questions:

```text
                         KENYA CRIMELENS
                              │
              ┌───────────────┼───────────────┐
              │               │               │
             WHAT?           WHERE?          WHEN?
              │               │               │
          Crime Types      Geography        Trends
          Offences         Counties         Periods
          Weapons          Rates            Changes
          Motives          Maps             Emerging
              │               │               │
              └───────────────┼───────────────┘
                              │
                             WHO?
                              │
                  ┌───────────┴───────────┐
                  │                       │
                Victims              Suspects
                  │                       │
                  └───────────┬───────────┘
                              │
                              ↓
                    SPATIAL INTELLIGENCE
                              │
                              ↓
                       DATA EXPLORER
                              │
                              ↓
                     METHODOLOGY & DATA
```

The goal is to move beyond simply displaying statistics and provide a structured environment for **exploration, comparison, interpretation, and evidence generation**.

---

# 🧩 Application Modules

## 🏠 National Overview

Provides the baseline picture of the complete dataset without analytical filters.

Includes:

* Total reported incidents
* Reported victim information
* County distribution
* Dominant offence categories
* Overall trends
* High-level national patterns

---

## 📊 Executive Overview

A decision-oriented view for quickly understanding the current analytical selection.

Includes:

* Key performance indicators
* Active filter context
* Automated analytical summary
* Crime trends
* Geographic patterns
* Dominant crime categories
* High-level findings

---

## 📈 Crime Trends

Examines how reported crime changes over time.

Includes:

* Monthly incident trends
* Reported victim trends
* Three-month moving averages
* Period comparisons
* Year-on-year changes where applicable
* Changes in offence composition

---

## 🗺️ Geography & Maps

Explores the geographic distribution of reported incidents across Kenya.

Includes:

* County-level incident counts
* Population-adjusted incident rates
* County rankings
* County × offence patterns
* Interactive geographic visualisations

### Count vs rate

Users should distinguish between:

> **Absolute number of reported incidents**

and:

> **Reported incidents per 100,000 population**

This prevents large-population counties from automatically appearing to have the highest burden simply because they have more residents.

---

## 🗂️ Crime Types

Examines the structure and composition of reported crime.

Includes:

* Offence categories
* Specific offences
* Weapons
* Motives
* County × offence relationships
* Crime composition over time

---

## 👥 Victims

Provides a victim-focused analytical view.

Includes:

* Reported victim counts
* Victim gender
* Victim burden by offence category
* Incident-level versus victim-level distributions
* Victim trends over time

Where information is unavailable in the source material, it is retained as missing rather than being silently converted into an observed value.

---

## 🕵️ Suspects & Alleged Perpetrators

Examines information reported about suspected or alleged offenders.

Includes:

* Reported suspect counts
* Suspect gender
* Suspect group sizes
* Offences associated with reported suspects

> **Important:** Information in this module represents reported or alleged information from media sources. It should not be interpreted as evidence of guilt, conviction, or criminal responsibility.

---

## 🔍 Data Explorer

Provides direct access to the underlying analytical records.

Features include:

* Full-text search
* Active-filter browsing
* Record-level inspection
* CSV export
* Excel export
* Underlying incident information

The Data Explorer provides an important link between:

> **Aggregated insight → underlying records → source evidence**

---

## 📖 Methodology

Documents how Kenya CrimeLens is constructed and how its outputs should be interpreted.

The methodology module covers:

* Data sources
* Data coverage
* Unit of analysis
* Crime classification
* Coding decisions
* Missing-data treatment
* Data completeness
* Geographic classification
* Population data
* Media-reporting bias
* Interpretation limitations

---

# 🎛️ Interactive Filtering

The application provides a shared query panel across analytical modules.

### Time

* Year

### Geography

* County

### Crime

* Offence category

### Victim / Suspect

* Victim gender

### Context

* Weapon
* Motive

Users can:

**Apply Filters** → update the analysis

**Reset All** → clear the current selection

Active filters are displayed to maintain analytical context.

---

# 🧠 Narrative Intelligence

A key feature of Kenya CrimeLens is its analytical narrative layer.

Rather than requiring users to interpret every chart independently, filtered results can be translated into plain-language findings.

For example:

> **Key finding:** Homicide/unlawful death represents the largest share of reported incidents in the current selection.

The narrative layer can highlight:

* Dominant offence categories
* Geographic concentration
* Temporal changes
* Reported victim burden
* Comparative differences
* Important interpretation cautions

The purpose is not to replace the underlying data or analysis, but to make patterns easier to identify and communicate.

---

# 📐 Analytical Measures

Kenya CrimeLens uses several descriptive measures to support comparison.

### Reported incident rate

Where population-adjusted analysis is available:

```text
Reported incident rate per 100,000
=
(Number of reported incidents / Population)
× 100,000
```

Population figures are based on the **2019 Kenya Population and Housing Census**.

### Average victims per incident

```text
Average victims per incident
=
Reported victims / Reported incidents
```

This metric is intentionally described as **average victims per incident** rather than "severity".

---

# 🧪 Data Processing Pipeline

```text
Raw Media-Mining Data
        │
        ▼
Data Cleaning
        │
        ▼
Standardisation & Classification
        │
        ▼
Duplicate / Record Checks
        │
        ▼
Missing-Data Handling
        │
        ▼
Clean Analytical Dataset
        │
        ▼
Analytical Functions
        │
        ▼
Interactive Visualisations
        │
        ▼
Narrative Insights
        │
        ▼
User Exploration
```

The separation between data preparation, analytical functions, visualisation, and application presentation helps maintain consistency across the dashboard.

---

# 📁 Project Structure

```text
KenyaCrimeLens/
│
├── app.py
│
├── pages/
│   ├── 1_Executive_Overview.py
│   ├── 2_Trends.py
│   ├── 3_Geography.py
│   ├── 4_Crime_Types.py
│   ├── 5_Victims.py
│   ├── 6_Suspects.py
│   ├── 7_Data_Explorer.py
│   └── 8_Methodology.py
│
├── utils/
│   ├── theme.py
│   ├── filters.py
│   ├── loader.py
│   ├── analytics.py
│   ├── charts.py
│   └── population.py
│
├── data/
│   └── cleaned_crime_data.csv
│
├── assets/
│   ├── dashboard-overview.png
│   ├── executive-overview.png
│   ├── crime-trends.png
│   ├── geography.png
│   ├── crime-types.png
│   ├── victims.png
│   └── data-explorer.png
│
├── data_cleaning.py
├── CUMULATIVE MEDIA MINING DATA 2025-2026 (1).xlsx
├── requirements.txt
├── LICENSE
└── README.md
```

---

# 🛠️ Technology Stack

| Technology    | Purpose                                 |
| ------------- | --------------------------------------- |
| **Python**    | Core programming and analytical logic   |
| **Streamlit** | Interactive application framework       |
| **Plotly**    | Interactive charts and visualisations   |
| **Pandas**    | Data manipulation and analysis          |
| **NumPy**     | Numerical operations                    |
| **OpenPyXL**  | Excel processing                        |
| **CSS**       | Application styling and UI presentation |

---

# 🚀 Run Locally

## 1. Clone the repository

```bash
git clone <repository-url>
cd KenyaCrimeLens
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Start the application

```bash
streamlit run app.py
```

The application will open in your default browser.

---

# ⚠️ Data & Interpretation Disclaimer

Kenya CrimeLens is based on **media-reported crime incidents**, not a complete administrative crime database.

The dataset therefore should **not** be interpreted as:

* A complete census of crimes committed in Kenya
* Official police crime statistics
* A direct measure of crime prevalence
* A direct measure of crime risk
* Evidence that one county is inherently more criminal than another

Media reporting may be affected by:

* Population size
* Geographic location
* Media presence
* Public interest
* Incident severity
* Political significance
* Availability of information
* Reporting practices
* Source selection

Therefore:

> **A high concentration of media reports does not necessarily imply a proportionally high level of underlying crime.**

Likewise:

> **The absence of a media-reported incident does not imply the absence of crime.**

---

# 🔬 Data Quality Principles

Kenya CrimeLens follows several principles designed to improve analytical transparency.

### Missing values remain missing

Missing victim counts are not automatically converted to one.

### Definitions matter

The application distinguishes between:

* Reported incidents
* Reported victims
* Fatalities, where supported
* Suspects
* Alleged perpetrators

### Counts and rates are different

County comparisons should consider both:

* Absolute reported incidents
* Population-adjusted reported incident rates

### Allegations are not convictions

Reported suspects or alleged perpetrators should not be interpreted as convicted offenders.

### Transparency over false precision

Where source data is incomplete, the application aims to expose that limitation rather than conceal it.

---

# 📊 Dataset

**Coverage:** January 2025 – July 2026

**Records:** 1,530+ media-reported incidents

**Geographic scope:** Kenya

**Primary unit of analysis:** Reported crime incident

**Primary data source:** Media-mined crime reports

---

# 🗺️ Roadmap

Potential future development areas include:

* [ ] County choropleth mapping
* [ ] Sub-county spatial analysis
* [ ] Incident-level point mapping
* [ ] Kernel Density Estimation (KDE)
* [ ] Statistical hotspot analysis
* [ ] Additional population-adjusted indicators
* [ ] More detailed victim age analysis
* [ ] Source-level media coverage analysis
* [ ] Data completeness dashboard
* [ ] Incident-level source/evidence trail
* [ ] Advanced period comparison
* [ ] Automated emerging-crime detection
* [ ] Additional analytical indicators

---

# 🤝 Intended Use

Kenya CrimeLens is intended to support:

* Crime research
* Exploratory data analysis
* Evidence-informed policy discussions
* Crime trend monitoring
* Geographic analysis
* Research reporting
* Data storytelling
* Intelligence-oriented exploration
* Identification of areas requiring further investigation

It is designed as a **research and analytical tool**, not as a replacement for official crime reporting systems.

---

# 📜 License

This project is licensed under the **MIT License**.

See [`LICENSE`](./LICENSE) for the full license text.

---

<p align="center">

### 🇰🇪 Kenya CrimeLens

**Turning media-reported crime data into structured analytical insight.**

<a href="https://kenyacrimelens.streamlit.app/">
  <strong>🚀 Explore the Live Dashboard →</strong>
</a>

</p>
