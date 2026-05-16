import pandas as pd

CSV_PATH = "/opt/airflow/data/ev_dataset.csv"

def validate_csv():
    print("🔍 Validating CSV...")
    df = pd.read_csv(CSV_PATH)

    assert len(df) > 0, "CSV is empty!"
    assert df.isnull().mean().max() < 0.5, "Too many nulls (>50%) in some column!"

    print(f" Validated: {len(df)} rows, {len(df.columns)} columns")
    return True