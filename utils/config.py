"""Central configuration for Kenya CrimeLens.

Single source of truth for brand tokens, column names and shared constants
so pages and modules never hard-code magic strings.
"""

from __future__ import annotations

import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT_DIR, "data", "cleaned_crime_data.csv")
GEOJSON_PATH = os.path.join(ROOT_DIR, "assets", "kenya_counties.geojson")

# ---------------------------------------------------------------------------
# Brand tokens (Kenyan flag derived)
# ---------------------------------------------------------------------------
KENYA_GREEN = "#006B3D"        # deep flag green, sidebar base
KENYA_GREEN_DARK = "#004D2C"   # input backgrounds inside sidebar
KENYA_RED = "#B91C1C"          # flag red, reserved for severity accents
KENYA_BLACK = "#111827"
ACCENT = "#0284c7"             # sky-600, primary interactive accent
ACCENT_LIGHT = "#0ea5e9"
PAGE_BG = "#f6f8fa"
INK = "#0f172a"
MUTED = "#64748b"

# Tri-stripe used as the visual signature across headers and cards
FLAG_STRIPE = (
    f"linear-gradient(90deg, {KENYA_BLACK} 0 33.3%, "
    f"{KENYA_RED} 33.3% 66.6%, {KENYA_GREEN} 66.6% 100%)"
)

# ---------------------------------------------------------------------------
# Dataset columns
# ---------------------------------------------------------------------------
COL_DATE = "Date"
COL_YEAR = "Year"
COL_MONTH = "Month"
COL_COUNTY = "County"
COL_CATEGORY = "Offence Category"
COL_OFFENCE = "Offence"
COL_VICTIMS = "Victim Tally"
COL_VICTIM_GENDER = "Victim Gender"
COL_PERPS = "Perpetrator Tally"
COL_PERP_GENDER = "Perpetrator Gender"
COL_WEAPON = "Weapon"
COL_MOTIVE = "Motive"
COL_SOURCE = "Source"
COL_SUMMARY = "Case Summary"

CATEGORICAL_COLS = [
    COL_COUNTY, COL_CATEGORY, COL_OFFENCE, COL_VICTIM_GENDER,
    COL_PERP_GENDER, COL_WEAPON, COL_MOTIVE, COL_SOURCE,
]

UNKNOWN = "Unknown"
ALL = "All"

# Values that can never be placed on the county map
NON_MAPPABLE = {UNKNOWN, "Multiple Counties", "Nationwide", "Outside Kenya"}

# Minimum incidents before a per-incident ratio is considered reliable
MIN_INCIDENTS_FOR_RATIO = 5

APP_NAME = "Kenya CrimeLens"
APP_TAGLINE = "Media-mined crime intelligence · 2025–2026"
DATA_DISCLAIMER = (
    "Figures reflect media-reported incidents, not official police statistics. "
    "A missing victim count is treated as 1."
)
