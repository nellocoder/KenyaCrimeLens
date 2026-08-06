"""Generate a synthetic demo dataset for local testing (not real data)."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
n = 1200
counties = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Kiambu", "Machakos",
            "Uasin Gishu", "Garissa", "Turkana", "Kilifi", "Unknown"]
cats = ["Homicide", "Robbery", "Sexual Offences", "Assault", "Banditry",
        "Fraud", "Kidnapping"]
weapons = ["Firearm", "Knife", "Blunt object", "None", "Unknown"]
motives = ["Land dispute", "Robbery", "Domestic", "Unknown", "Revenge"]
dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(
    rng.integers(0, 540, n), unit="D")
df = pd.DataFrame({
    "Date": dates,
    "County": rng.choice(counties, n, p=[.25,.1,.08,.1,.08,.07,.06,.06,.05,.05,.1]),
    "Offence Category": rng.choice(cats, n),
    "Offence": rng.choice(["Murder", "Armed robbery", "Defilement", "GBH",
                           "Cattle rustling", "M-Pesa fraud", "Abduction"], n),
    "Victim Tally": rng.poisson(1.4, n) + 1,
    "Victim Gender": rng.choice(["Male", "Female", "Mixed", "Unknown"], n),
    "Perpetrator Tally": np.where(rng.random(n) < .6, rng.poisson(2, n) + 1, np.nan),
    "Perpetrator Gender": rng.choice(["Male", "Female", "Unknown"], n, p=[.6,.1,.3]),
    "Weapon": rng.choice(weapons, n),
    "Motive": rng.choice(motives, n),
    "Source": rng.choice(["Daily Nation", "The Standard", "The Star"], n),
    "Case Summary": "Synthetic demo record for UI testing.",
})
df.to_csv("data/cleaned_crime_data.csv", index=False)
print(f"Wrote {len(df)} demo rows to data/cleaned_crime_data.csv")
