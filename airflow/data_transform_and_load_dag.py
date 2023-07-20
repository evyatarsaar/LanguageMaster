import sqlite3
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.sqlite_operator import SQLiteOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_transform_and_load_dag',
    default_args=default_args,
    description='Data Transform and Load DAG',
    schedule_interval=timedelta(days=1),
)


def load_to_new_table(**context):
    transformed_data = context['ti'].xcom_pull(task_ids='transform_data_task')

    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()

    # Create a new table with the desired schema
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS new_translations (
            id INTEGER PRIMARY KEY,
            original_sentence TEXT,
            german_translation TEXT,
            dutch_translation TEXT,
            spanish_translation TEXT,
            french_translation TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    '''
    cursor.execute(create_table_query)

    # Insert the transformed data into the new table
    insert_query = '''
        INSERT INTO new_translations (original_sentence, german_translation, dutch_translation, spanish_translation, french_translation)
        VALUES (?, ?, ?, ?, ?)
    '''
    cursor.executemany(insert_query, transformed_data)

    conn.commit()
    conn.close()


load_to_new_table_task = PythonOperator(
    task_id='load_to_new_table_task',
    python_callable=load_to_new_table,
    provide_context=True,  # Pass the output of transform_data_task to this task
    dag=dag,
)

transform_data_task = SQLiteOperator(
    task_id='transform_data_task',
    sql='''
        SELECT DISTINCT LOWER(original_sentence) AS original_sentence, 
                        LOWER(german_translation) AS german_translation,
                        LOWER(dutch_translation) AS dutch_translation,
                        LOWER(spanish_translation) AS spanish_translation,
                        LOWER(french_translation) AS french_translation
        FROM translations
    ''',
    dag=dag,
)

load_to_new_table_task << transform_data_task
