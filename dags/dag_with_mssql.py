from airflow import DAG
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
from datetime import datetime, timedelta 

dag_owner = 'Tony Arianto'

default_args = {
        'owner': dag_owner,
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
        }

with DAG(
        dag_id='test_mssql_01',
        default_args=default_args,
        description='Test Mssql',
        start_date=datetime(24,5,14),
        schedule_interval='@daily',
        catchup=False
) as dag:
    
    run_query = MsSqlOperator(
        task_id='test_mssql',
        mssql_conn_id='sqlserver_con',
        sql="SELECT * FROM dbo.posts",
    )
    
run_query