"""Methodology: data sources, definitions, and limitations."""

import streamlit as st

st.set_page_config(page_title="Methodology · Kenya CrimeLens", page_icon="📖", layout="wide")

from utils.theme import apply_theme, page_header
from utils.filters import render_sidebar
from utils.loader import load_data

apply_theme()
df = load_data()
render_sidebar(df)

page_header("📖", "Methodology & Data",
            "How the dataset was constructed and important limitations")

st.markdown("""
### Data Source
Incidents are extracted from Kenyan print media articles published between January 2025 and June 2026.
Monitored sources include:
- Daily Nation
- The Standard
- The Star
- People Daily
- Other regional and online outlets.

### Incident Definition
Each row represents a **distinct reported crime event**. One article may describe multiple incidents; these are separated where possible.

### Victim and Suspect Counts
- **Victim Tally**: number of victims mentioned in the article. If not stated, the field is **left empty** (not assumed to be 1).
- **Perpetrator Tally**: number of suspects/alleged perpetrators mentioned.
- "Unknown" indicates the article did not specify the gender/age/county etc.

### Offence Categories
Offences are classified into broad categories (e.g., Homicide, Theft, Sexual violence) based on keywords and context.

### Geographic Coding
County is assigned based on the location mentioned in the article. Incidents occurring in "Multiple Counties", "Nationwide", or outside Kenya are excluded from county maps.
County centroids are approximate.

### Data Quality & Completeness
Media-reported crime is **not equivalent to official crime statistics**. Key biases:
- **Reporting bias**: more severe, unusual, or urban incidents are more likely to be reported.
- **Access bias**: areas with more journalists or media outlets may appear to have more crime.
- **Missing data**: victim/suspect demographics are often unreported.

**Therefore, this dashboard should not be used to infer actual crime prevalence or to compare safety between counties without considering population, media coverage, and underreporting.**

### Rates per 100,000 Population
Incident rates are calculated using the 2019 Kenya Population and Housing Census county population figures.
""")

st.caption("For questions or data requests, please contact the NCRC research team.")
