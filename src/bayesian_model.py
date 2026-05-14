import os
from pathlib import Path

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "marketing_db")
DB_USER = os.getenv("DB_USER", "jaykhakhar")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

RESULTS_DIR = Path("reports")
RESULTS_DIR.mkdir(exist_ok=True)

if DB_PASSWORD:
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


def load_data():
    query = """
    SELECT
        date,
        channel,
        spend,
        clicks,
        conversions,
        revenue
    FROM public.marketing_campaigns;;
    """
    return pd.read_sql(query, engine)


def prepare_data(df):
    df = df.copy()

    df["spend"] = df["spend"].astype(float)
    df["clicks"] = df["clicks"].astype(float)
    df["conversions"] = df["conversions"].astype(float)

    df["log_spend"] = np.log1p(df["spend"])
    df["channel_code"] = df["channel"].astype("category").cat.codes

    channel_mapping = dict(
        enumerate(df["channel"].astype("category").cat.categories)
    )

    return df, channel_mapping


def train_bayesian_model(df):
    channel_idx = df["channel_code"].values
    log_spend = df["log_spend"].values
    conversions = df["conversions"].values.astype(int)

    n_channels = df["channel_code"].nunique()

    with pm.Model() as model:
        alpha = pm.Normal("alpha", mu=1.0, sigma=1.0)

        channel_effect = pm.Normal(
            "channel_effect",
            mu=0.0,
            sigma=1.0,
            shape=n_channels,
        )

        spend_effect = pm.HalfNormal("spend_effect", sigma=1.0)

        mu = pm.math.exp(
            alpha
            + channel_effect[channel_idx]
            + spend_effect * log_spend
        )

        y_obs = pm.Poisson("conversions", mu=mu, observed=conversions)

        trace = pm.sample(
            draws=1000,
            tune=1000,
            chains=2,
            target_accept=0.9,
            random_seed=42,
        )

    return model, trace


def summarize_results(trace, channel_mapping):
    summary = az.summary(trace, var_names=["channel_effect", "spend_effect"])

    summary.to_csv(RESULTS_DIR / "bayesian_model_summary.csv")

    channel_rows = []

    for i, channel in channel_mapping.items():
        param_name = f"channel_effect[{i}]"

        if param_name in summary.index:
            channel_rows.append({
                "channel": channel,
                "mean_effect": summary.loc[param_name, "mean"],
                "lower_94_hdi": summary.loc[param_name, "hdi_3%"],
                "upper_94_hdi": summary.loc[param_name, "hdi_97%"],
            })

    channel_df = pd.DataFrame(channel_rows)
    channel_df.to_csv(RESULTS_DIR / "channel_effectiveness.csv", index=False)

    print("\nBayesian model completed.")
    print("\nChannel effectiveness:")
    print(channel_df)
    print("\nSaved results to reports/")


def main():
    df = load_data()
    df, channel_mapping = prepare_data(df)

    print(f"Loaded {len(df)} rows from PostgreSQL")
    print("Training Bayesian model...")

    model, trace = train_bayesian_model(df)
    summarize_results(trace, channel_mapping)


if __name__ == "__main__":
    main()