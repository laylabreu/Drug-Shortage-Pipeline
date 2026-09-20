import sys

sys.path.append('/opt/airflow/src')
from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from run_shortage_ingestion import fetch_shortages

with DAG(dag_id= 'shortage_dag', start_date=datetime(2026, 9, 18) , schedule = '@daily', catchup=False) as dag:
    shortage_task = PythonOperator(task_id = 'load_shortages', python_callable = fetch_shortages)

