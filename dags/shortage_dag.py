import sys
sys.path.append('/opt/airflow/src')
from run_shortage_ingestion import fetch_shortages
from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime


with DAG(dag_id= 'shortage_dag', start_date=datetime(2026, 9, 18) , schedule = None) as dag:
    shortage_task = PythonOperator(task_id = 'load_shortages', python_callable = fetch_shortages)

