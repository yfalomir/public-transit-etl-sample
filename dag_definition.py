from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from import_ovapi_transport_data import extract_and_load_ovapi_data

with DAG(
    dag_id="extract_and_load_ovapi_line_data",
    start_date=days_ago(1),
    # The data doesn't seem to change a lot, if necessary could be increased
    schedule="@daily", 
    tags=["extract", "daily", "ovapi"]   
) as DAG:
    PythonOperator(
        "extract_and_load_ovapi_line_data",
        python_callable=extract_and_load_ovapi_data,
        op_kwargs={
            "base_url": "http://v0.ovapi.nl",
            "endpoint": "/line/"
        },
    )