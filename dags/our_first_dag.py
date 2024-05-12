from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'tony arianto',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='tutorial_v6',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval='@daily',
    start_date=datetime(2024, 5, 10, 2),
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo Hello World, this if the first task!"
    )
    task2 = BashOperator(
        task_id='second_task',
        bash_command="echo Hai...ini task2 akan dijalankan setelah task1!"
    )
    task3 = BashOperator(
        task_id='third_task',
        bash_command="echo Hai...ini task2 akan dijalankan setelah task1!"
    )
    
# cara 1     
# task1.set_downstream(task2)
# task1.set_downstream(task3)

# cara 2
# task1 >> task2
# task1 >> task3

# cara 3
task1 >> [task2, task3]