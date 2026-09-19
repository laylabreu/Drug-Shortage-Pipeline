#q. file wont show up in airflow unless has a DAG definition
#1. write imports
from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


def say_hello():
    print('Hello DAG')
#2. define the DAG itself
with DAG(dag_id= 'hello_dag', start_date = datetime(2026, 9, 1), schedule = None) as dag:
    #3. create the task -- dont use say_hello() bc then it will be executed immediaatly and not when airflow needs it to be called later
    hello_task = PythonOperator(task_id= 'say_hello_dag', python_callable = say_hello)