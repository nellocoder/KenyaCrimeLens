"""
Kenya CrimeLens - Data Cleaning Pipeline
=========================================
Takes the raw "CUMULATIVE MEDIA MINING DATA 2025-2026" Excel file and produces
a cleaned, categorized CSV ready for the Streamlit app.

Usage:
    python data_cleaning.py

Input : CUMULATIVE MEDIA MINING DATA 2025-2026 (1).xlsx  (same folder)
Output: cleaned_crime_data.csv
"""

import re
import pandas as pd

RAW_FILE = "CUMULATIVE MEDIA MINING DATA 2025-2026 (1).xlsx"
OUT_FILE = "cleaned_crime_data.csv"

# Reference date used to detect day/month-transposed dates (dataset runs to mid-2026)
TODAY = pd.Timestamp("2026-08-03")

# ---------------------------------------------------------------------------
# 1. LOAD (the sheet has a two-row header: group titles in row 1, real
#    column names in row 2, so header=1)
# ---------------------------------------------------------------------------
df = pd.read_excel(RAW_FILE, sheet_name=0, header=1)
df.columns = [
    "DATE", "OFFENCE", "VICTIM_TALLY", "COUNTY", "SPECIFIC_AREA",
    "VICTIM_NATIONALITY", "VICTIM_GENDER", "VICTIM_IDENTITY", "VICTIM_AGE",
    "PERP_TALLY", "PERP_NATIONALITY", "PERP_GENDER", "PERP_AGE",
    "PERP_IDENTITY", "MOTIVE", "WEAPON", "SOURCE", "SUMMARY",
    "X18", "X19", "X20", "X21",
]
df = df.drop(columns=["X18", "X19", "X20", "X21"])  # empty trailing columns

# ---------------------------------------------------------------------------
# 2. DATES - parse, then fix day/month transpositions (dates in the future)
# ---------------------------------------------------------------------------
df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
future = df["DATE"] > TODAY
df.loc[future, "DATE"] = df.loc[future, "DATE"].apply(
    lambda x: pd.Timestamp(x.year, x.day, x.month)
)
df["YEAR"] = df["DATE"].dt.year
df["MONTH"] = df["DATE"].dt.to_period("M").astype(str)
df["QUARTER"] = df["DATE"].dt.to_period("Q").astype(str).str.replace("Q", " Q")

# ---------------------------------------------------------------------------
# 3. COUNTY standardization
#    - towns mapped to their county (Eldoret -> Uasin Gishu, etc.)
#    - spelling mistakes fixed (Narobi, Garrisa, Lykipia, ...)
#    - multi-county / regional entries grouped as "Multiple Counties"
# ---------------------------------------------------------------------------
town_to_county = {
    "eldoret": "Uasin Gishu", "naivasha": "Nakuru", "malindi": "Kilifi",
    "bondo": "Siaya", "rongo": "Migori", "nanyuki": "Laikipia",
    "trans-mara": "Narok", "trans mara": "Narok",
}
county_fix = {
    "narobi": "Nairobi", "garrisa": "Garissa", "west pokot": "West Pokot",
    "muranga": "Murang'a", "lykipia": "Laikipia", "homabay": "Homa Bay",
    "taita": "Taita Taveta", "taita-taveta": "Taita Taveta",
    "taitataveta": "Taita Taveta", "thara-ka- nithi": "Tharaka Nithi",
    "tharaka-nithi": "Tharaka Nithi", "nandi county": "Nandi",
    "elgeyo-marakwet": "Elgeyo Marakwet",
}

def clean_county(c):
    c = str(c).strip()
    cl = c.lower().strip(" .,")
    if cl in ("nan", "unknown", "counties", ""):
        return "Unknown"
    if cl == "kenya":
        return "Nationwide"
    if cl in ("somalia", "myanmar", "vietnam", "haiti"):
        return "Outside Kenya"
    if cl in town_to_county:
        return town_to_county[cl]
    if cl in county_fix:
        return county_fix[cl]
    if ("," in c or " and " in cl or "/" in c or "several" in cl
            or "counties" in cl or "rift valley" in cl or "nyanza" in cl
            or "conservanc" in cl or "(" in c):
        return "Multiple Counties"
    return c.title().replace("'S", "'s")

df["COUNTY"] = df["COUNTY"].apply(clean_county).replace({"Murang'A": "Murang'a"})

# ---------------------------------------------------------------------------
# 4. GENDER / WEAPON / MOTIVE standardization
# ---------------------------------------------------------------------------
def clean_gender(g):
    g = str(g).strip().lower()
    if g in ("nan", "unknown", ""):
        return "Unknown"
    if g == "male":
        return "Male"
    if g == "female":
        return "Female"
    if "female and children" in g:
        return "Female and Children"
    if "and" in g:
        return "Male and Female"
    return g.title()

df["VICTIM_GENDER"] = df["VICTIM_GENDER"].apply(clean_gender)
df["PERP_GENDER"] = df["PERP_GENDER"].apply(clean_gender)

weapon_map = {
    "gun": "Firearm", "firearm": "Firearm", "fire arm": "Firearm",
    "panga": "Machete", "nan": "Unknown", "unknown": "Unknown", "": "Unknown",
}

def clean_weapon(w):
    w = str(w).strip()
    wl = w.lower()
    if wl in weapon_map:
        return weapon_map[wl]
    return w.title() if w.isupper() else w[0].upper() + w[1:]

df["WEAPON"] = df["WEAPON"].apply(clean_weapon)
df["MOTIVE"] = df["MOTIVE"].apply(
    lambda m: "Unknown" if str(m).strip().lower() in ("nan", "unknown", "")
    else str(m).strip()[0].upper() + str(m).strip()[1:]
)

# ---------------------------------------------------------------------------
# 5. TALLIES - numeric; a missing victim tally is treated as 1 victim
# ---------------------------------------------------------------------------
df["VICTIM_TALLY"] = pd.to_numeric(df["VICTIM_TALLY"], errors="coerce").fillna(1).astype(int)
df["PERP_TALLY"] = pd.to_numeric(df["PERP_TALLY"], errors="coerce")

# ---------------------------------------------------------------------------
# 6. OFFENCE normalization + categorization
#    256 raw spellings -> normalized names -> 19 offence categories
# ---------------------------------------------------------------------------
typo_fix = {
    "insuarance fraud": "insurance fraud",
    "wreckless driving": "reckless driving",
    "child ponography": "child pornography",
    "illegal posession of firearm": "illegal possession of firearm",
    "illegal possession of firearms": "illegal possession of firearm",
    "mudered": "murder",
}

def norm_offence(o):
    o = re.sub(r"\s+", " ", str(o).strip().lower())
    return typo_fix.get(o, o)

df["OFFENCE_NORM"] = df["OFFENCE"].apply(norm_offence)

# (category, keywords) - first match wins
CAT_RULES = [
    ("Homicide & Unlawful Killing", ["murder", "manslaughter", "femicide", "infanticide",
        "homicide", "mob justice", "mob injustice", "lynching", "causing death",
        "killing", "matricide", "patricide", "fratricide"]),
    ("Sexual & Gender-Based Violence", ["defilement", "rape", "sexual", "sodomy",
        "incest", "pornography", "gender based violence", "gbv", "fgm",
        "female genital", "indecent"]),
    ("Abduction & Kidnapping", ["abduction", "kidnap", "child stealing", "missing child"]),
    ("Police Misconduct", ["police brutality", "extra-judicial", "extrajudicial",
        "police shooting", "unlawful detention"]),
    ("Robbery, Theft & Burglary", ["robbery", "theft", "stealing", "burglary",
        "carjacking", "cattle rustling", "stock theft", "shoplifting", "mugging"]),
    ("Assault & Bodily Harm", ["assault", "grievous harm", "grievous bodily",
        "torture", "battery", "affray", "violence"]),
    ("Organized Crime & Terrorism", ["terror", "banditry", "gang", "organised crime",
        "organized crime", "radicalis", "radicaliz", "arms possession",
        "possession of firearm", "criminal gang", "militia"]),
    ("Fraud & Financial Crimes", ["fraud", "forgery", "embezzlement", "money laundering",
        "tax evasion", "impersonat", "counterfeit", "false pretence",
        "pyramid", "ponzi", "insurance"]),
    ("Corruption & Abuse of Office", ["corruption", "bribery", "abuse of office",
        "conflict of interest", "economic crime", "misappropriat"]),
    ("Human Trafficking & Smuggling", ["human trafficking", "organ trafficking",
        "organ theft", "child trafficking", "person smuggling"]),
    ("Drugs & Contraband", ["drug", "narcotic", "smuggling", "illicit brew",
        "contraband", "trafficking"]),
    ("Property Destruction & Arson", ["arson", "malicious damage", "vandalism",
        "destruction of property", "torching"]),
    ("Political & Electoral Offences", ["political", "election", "electoral", "incitement"]),
    ("Land & Eviction Offences", ["land grabbing", "eviction", "trespass",
        "land fraud", "boundary"]),
    ("Cybercrime", ["cyber", "hacking", "online"]),
    ("Environmental & Wildlife Crimes", ["environment", "poaching", "illegal mining",
        "pollution", "logging", "sand harvesting", "wildlife", "fishing"]),
    ("Traffic & Safety Offences", ["driving", "aviation", "traffic", "road safety"]),
    ("Public Order & Administration of Justice", ["contempt of court",
        "unlawful assembly", "hate speech", "defamation", "perjury", "obstruction",
        "aiding and abetting", "conspiracy", "escape", "riot", "trespass to land"]),
]

def categorize(o):
    for cat, kws in CAT_RULES:
        if any(k in o for k in kws):
            return cat
    return "Other Offences"

df["CATEGORY"] = df["OFFENCE_NORM"].apply(categorize)

# Second pass: exact fixes for entries that fell into "Other"
second_pass = {
    "extortion": "Fraud & Financial Crimes", "bribe": "Corruption & Abuse of Office",
    "child abuse": "Sexual & Gender-Based Violence", "voyeurism": "Sexual & Gender-Based Violence",
    "harassement": "Assault & Bodily Harm", "harassment": "Assault & Bodily Harm",
    "threat to life": "Assault & Bodily Harm", "threats": "Assault & Bodily Harm",
    "hate crime": "Assault & Bodily Harm", "aggression": "Assault & Bodily Harm",
    "massacre": "Homicide & Unlawful Killing", "unclear death": "Homicide & Unlawful Killing",
    "illegal exhumation of a body": "Homicide & Unlawful Killing",
    "illegal possession and use of firearms": "Organized Crime & Terrorism",
    "religious extremism": "Organized Crime & Terrorism", "piracy": "Organized Crime & Terrorism",
    "vigilantism": "Organized Crime & Terrorism",
    "enforced disappearance": "Abduction & Kidnapping",
    "illicit trade": "Drugs & Contraband", "possession of uncustomed goods": "Drugs & Contraband",
    "contempt": "Public Order & Administration of Justice",
    "creating disturbance": "Public Order & Administration of Justice",
    "disorderly conduct": "Public Order & Administration of Justice",
    "breach of peace": "Public Order & Administration of Justice",
    "public mischief": "Public Order & Administration of Justice",
    "unlawful imprisonment": "Public Order & Administration of Justice",
    "swearing to false affidavit": "Public Order & Administration of Justice",
    "disertation from duty": "Public Order & Administration of Justice",
    "unlawful docking": "Public Order & Administration of Justice",
    "breach of data protection laws": "Cybercrime", "violation of privacy": "Cybercrime",
}
df.loc[df["OFFENCE_NORM"].isin(second_pass), "CATEGORY"] = df["OFFENCE_NORM"].map(second_pass)
df["OFFENCE"] = df["OFFENCE_NORM"].str.title()

# ---------------------------------------------------------------------------
# 7. FINAL SELECTION & EXPORT
# ---------------------------------------------------------------------------
out = df[[
    "DATE", "CATEGORY", "OFFENCE", "VICTIM_TALLY", "COUNTY", "SPECIFIC_AREA",
    "VICTIM_GENDER", "VICTIM_AGE", "PERP_TALLY", "PERP_GENDER", "PERP_AGE",
    "MOTIVE", "WEAPON", "SOURCE", "SUMMARY", "YEAR", "MONTH", "QUARTER",
]].copy()
out.columns = [
    "Date", "Offence Category", "Offence", "Victim Tally", "County",
    "Specific Area", "Victim Gender", "Victim Age", "Perpetrator Tally",
    "Perpetrator Gender", "Perpetrator Age", "Motive", "Weapon", "Source",
    "Case Summary", "Year", "Month", "Quarter",
]
out = out.sort_values("Date")
out["Date"] = out["Date"].dt.strftime("%Y-%m-%d")
out.to_csv(OUT_FILE, index=False)

print(f"Saved {len(out)} records to {OUT_FILE}")
print(out["Offence Category"].value_counts().to_string())
