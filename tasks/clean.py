import pandas as pd

CSV_PATH  = "/opt/airflow/data/ev_dataset.csv"
CLEAN_PATH = "/opt/airflow/data/ev_cleaned.csv"

def clean_data():
    print(" Cleaning data...")
    df = pd.read_csv(CSV_PATH)

    # Clean column names
    df.columns = (
        df.columns.str.strip().str.lower()
        .str.replace(r"[\s\(\)\/\-]", "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates()
    print(f"   Removed {before - len(df)} duplicates")

    df.to_csv(CLEAN_PATH, index=False)
    print(f"Saved cleaned file → {CLEAN_PATH}")