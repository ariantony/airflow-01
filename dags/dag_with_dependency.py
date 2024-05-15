from airflow import DAG
from datetime import datetime, timedelta 
from airflow.operators.python import PythonOperator

dag_owner = 'tony arianto'

default_args = {
            'owner': dag_owner,
            'depends_on_past': False,
            'retries': 2,
            'retry_delay': timedelta(minutes=5)
        }
def get_sklearn():
    import sklearn
    print(f"Sklearn version: {sklearn.__version__}")

with DAG(dag_id='dag_with_dependency_01',
        default_args=default_args,
        description='dag_with_dependency_01',
        start_date=datetime(2023, 5, 14),
        schedule_interval='@daily',
        catchup=False
) as dag: 
    
    get_sklearn = PythonOperator(
        task_id='get_sklearn',
        python_callable=get_sklearn
    )
    
get_sklearn