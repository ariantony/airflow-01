from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta 

default_args = {
        'owner': 'TonyA',
        'retries': 5,
        'retry_delay': timedelta(minutes=5)
        }

def greet(age, ti):
    # name = ti.xcom_pull(task_ids='get_name')
    
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    
    print(
        f"Hello World! My name is {first_name} {last_name},"
        f"and Im {age} years old!"
        )
    
def get_name(ti):
    ti.xcom_push(key='first_name', value='Achasza')
    ti.xcom_push(key='last_name', value='Arianto')
    
with DAG(
        dag_id='our_dag_with_python_operator_v06',
        default_args=default_args,
        description='Using python operator',
        start_date=datetime(2023, 7, 12),
        schedule_interval='@daily',
) as dag:
    
    task1 = PythonOperator(
        task_id = 'greet',
        python_callable=greet,
        op_kwargs={'age':43}
    )

    task2 = PythonOperator(
        task_id = 'get_name',
        python_callable=get_name,
    )

task2 >> task1