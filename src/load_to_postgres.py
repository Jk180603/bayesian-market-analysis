import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "marketing_db")
DB_USER = os.getenv("DB_USER", "jaykhakhar")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DATA_PATH = Path("data/marketing_campaign_data.csv")
SCHEMA_PATH = Path("sql/schema.sql")

if DB_PASSWORD:
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def main():
    df = pd.read_csv(DATA_PATH)

    schema_sql = SCHEMA_PATH.read_text()

    with engine.begin() as conn:
        for statement in schema_sql.split(";"):
            statement = statement.strip()
            if statement:
                conn.execute(text(statement))

    df.to_sql(
        "marketing_campaigns",
        engine,
        if_exists="append",
        index=False,
    )

    print(f"Loaded {len(df)} rows into marketing_campaigns")

if __name__ == "__main__":
    main()