from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys

sys.path.insert(0, "/opt/airflow/tasks")
from validate import validate_csv
from clean    import clean_data
from load     import load_to_mysql

default_args = {
    "owner": "ev_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "email_on_failure": False,
}

with DAG(
    dag_id="ev_pipeline",
    default_args=default_args,
    description="EV CSV → MySQL Pipeline",
    schedule="@daily",          # รันทุกวัน (หรือ cron เช่น '0 6 * * *')
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ev", "pipeline"],
) as dag:

    t1 = PythonOperator(
        task_id="validate_csv",
        python_callable=validate_csv,
    )

    t2 = PythonOperator(
        task_id="clean_data",
        python_callable=clean_data,
    )

    t3 = PythonOperator(
        task_id="load_to_mysql",
        python_callable=load_to_mysql,
    )

    t1 >> t2 >> t3   # validate → clean → load