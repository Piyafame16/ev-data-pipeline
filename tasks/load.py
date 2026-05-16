import os
import pandas as pd
from sqlalchemy import create_engine, text

CLEAN_PATH = "/opt/airflow/data/ev_cleaned.csv"
TABLE_NAME = "electric_vehicles"

def load_to_mysql():
    host = os.getenv("EV_DB_HOST", "mysql")
    port = os.getenv("EV_DB_PORT", "3306")
    db   = os.getenv("EV_DB_NAME", "ev_db")
    user = os.getenv("EV_DB_USER", "ev_user")
    pw   = os.getenv("EV_DB_PASSWORD", "ev_pass")

    url    = f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}"
    engine = create_engine(url)

    df = pd.read_csv(CLEAN_PATH)
    print(f"🚀 Loading {len(df)} rows → {TABLE_NAME}")

    df.to_sql(TABLE_NAME, con=engine, if_exists="replace", index=False, chunksize=500)

    with engine.connect() as conn:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}")).scalar()
    print(f"✅ Verified: {count} rows in MySQL")