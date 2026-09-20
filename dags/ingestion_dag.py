import sys

sys.path.append('/opt/airflow/src')
from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from run_shortage_ingestion import fetch_shortages
from run_nadac_ingestion import fetch_nadac

with DAG(dag_id= 'ingestion_dags', start_date=datetime(2026, 9, 18) , schedule = '@daily', catchup=False) as dag:
    shortage_task = PythonOperator(task_id = 'load_shortages', python_callable = fetch_shortages)
    nadac_task = PythonOperator(task_id = 'load_prices', python_callable = fetch_nadac)
