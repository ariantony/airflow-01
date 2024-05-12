from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta 

default_args = {
        'owner': 'TonyA',
        'retries': 5,
        'retry_delay': timedelta(minutes=5)
        }

def greet(ti):
    # name = ti.xcom_pull(task_ids='get_name')
    
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    
    print(
        f"Hello World! My name is {first_name} {last_name},"
        f"and Im {age} years old!"
        )
    
def get_name(ti):
    ti.xcom_push(key='first_name', value='Achasza')
    ti.xcom_push(key='last_name', value='Arianto')
 
def get_age(ti):
    ti.xcom_push(key='age', value='12')
    
with DAG(
        dag_id='our_dag_with_python_operator_v07',
        default_args=default_args,
        description='Using python operator',
        start_date=datetime(2023, 7, 12),
        schedule_interval='@daily',
) as dag:
    
    task1 = PythonOperator(
        task_id = 'greet',
        python_callable=greet
    )

    task2 = PythonOperator(
        task_id = 'get_name',
        python_callable=get_name,
    )

    task3 = PythonOperator(
        task_id = 'get_age',
        python_callable=get_age,
    )
    
[task2, task3] >> task1