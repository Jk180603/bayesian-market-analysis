import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

n_days = 180

dates = pd.date_range(start="2025-01-01", periods=n_days, freq="D")

channels = ["Google Ads", "Meta Ads", "LinkedIn Ads", "Email", "Organic"]

rows = []

for date in dates:
    seasonality = 1 + 0.15 * np.sin(2 * np.pi * date.dayofyear / 30)

    for channel in channels:
        base_spend = {
            "Google Ads": 900,
            "Meta Ads": 700,
            "LinkedIn Ads": 400,
            "Email": 120,
            "Organic": 0,
        }[channel]

        spend = max(0, np.random.normal(base_spend, base_spend * 0.25)) if base_spend > 0 else 0

        effectiveness = {
            "Google Ads": 0.055,
            "Meta Ads": 0.045,
            "LinkedIn Ads": 0.035,
            "Email": 0.080,
            "Organic": 0.020,
        }[channel]

        impressions = int(spend * np.random.uniform(70, 130)) if spend > 0 else np.random.randint(2500, 6000)
        clicks = int(impressions * np.random.uniform(0.015, 0.055))

        expected_conversions = (
            clicks * effectiveness * seasonality
            + np.random.normal(0, 2)
        )

        conversions = max(0, int(expected_conversions))
        avg_order_value = np.random.normal(85, 15)
        revenue = conversions * avg_order_value

        rows.append({
            "date": date,
            "channel": channel,
            "spend": round(spend, 2),
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "revenue": round(revenue, 2),
        })

df = pd.DataFrame(rows)

df.to_csv(DATA_DIR / "marketing_campaign_data.csv", index=False)

print("Dataset created successfully!")
print(df.head())
print(f"Rows: {len(df)}")