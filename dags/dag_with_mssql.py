from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mssql_hook import MsSqlHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.dates import days_ago
import logging

# Default arguments
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

# Instantiate the DAG
dag = DAG(
    'mssql_to_postgresql',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
)

def extract_from_mssql(**kwargs):
    mssql_hook = MsSqlHook(mssql_conn_id='sqlserver_con')
    sql = "SELECT * FROM [dbo].[posts]"
    records = mssql_hook.get_records(sql)
    kwargs['ti'].xcom_push(key='mssql_data', value=records)

def transform_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(key='mssql_data', task_ids='extract_from_mssql')
    transformed_data = [
        {
            'userId': record[0],
            'id': record[1],
            'title': record[2],
            'body': record[3],
            'rectime': record[4]
        } for record in data
    ]
    kwargs['ti'].xcom_push(key='transformed_data', value=transformed_data)

def load_to_postgresql(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(key='transformed_data', task_ids='transform_data')
    pg_hook = PostgresHook(postgres_conn_id='postgres_con')
    
    insert_query = """
    INSERT INTO raw_data.posts (userId, id, title, body, rectime)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    for record in data:
        pg_hook.run(insert_query, parameters=(record['userId'], record['id'], record['title'], record['body'], record['rectime']))

# Tasks
extract_task = PythonOperator(
    task_id='extract_from_mssql',
    python_callable=extract_from_mssql,
    provide_context=True,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_postgresql',
    python_callable=load_to_postgresql,
    provide_context=True,
    dag=dag,
)

# Task dependencies
extract_task >> transform_task >> load_task
