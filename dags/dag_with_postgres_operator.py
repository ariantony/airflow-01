from airflow import DAG
from airflow.decorators import task
# from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime, timedelta 

dag_owner = 'Tony Arianto'

default_args = {
        'owner': dag_owner,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
        }

with DAG(dag_id='dag_postgresql_06',
        default_args=default_args,
        description='DAG With Postgresql',
        start_date=datetime(2024, 5, 11),
        schedule_interval='@daily',
        catchup=False
) as dag:
    task1 = PostgresOperator(
        task_id='PostgresOperator_task',
        postgres_conn_id='postgres_con',
        sql="""
            create table if not exists dag_runs_01 (
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            )
        """
    )
    task2 = PostgresOperator(
        task_id = 'PostgresOperator_insert',
        postgres_conn_id='postgres_con',
        sql="""
            insert into dag_runs_01 (dt, dag_id) values (
                '{{ ds }}',
                '{{ dag.dag_id }}'
            )
        """
    )
    
    task3 = PostgresOperator(
        task_id = 'PostgresOperator_delete',
        postgres_conn_id='postgres_con',
        sql="""
        delete from dag_runs_01 where dt ='{{ ds }}' and dag_id = '{{ dag.dag_id }}'
        """        
    )

task1 >> task3 >> task2