import sqlite3
import os, json
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.operators.python_operator import PythonOperator


# Drop the old table if it exists and create the new table with the desired schema
create_table_query = '''
    DROP TABLE IF EXISTS new_translations;

    CREATE TABLE new_translations (
        id INTEGER PRIMARY KEY,
        original_sentence TEXT,
        german_translation TEXT,
        dutch_translation TEXT,
        spanish_translation TEXT,
        french_translation TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
'''

default_args = {
    'owner': 'airflow_dags',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'data_transform_and_load_dag',
    default_args=default_args,
    description='Data Transform and Load DAG',
    schedule_interval=timedelta(days=1),
)


def transform_data_and_save():
    # Execute the SQL query and retrieve the transformed data
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()
    query = '''
        SELECT DISTINCT LOWER(original_sentence) AS original_sentence, 
                        LOWER(german_translation) AS german_translation,
                        LOWER(dutch_translation) AS dutch_translation,
                        LOWER(spanish_translation) AS spanish_translation,
                        LOWER(french_translation) AS french_translation
        FROM translations
    '''
    cursor.execute(query)
    transformed_data = cursor.fetchall()
    conn.close()

    # Save the transformed data to a temporary file (include unique identifier for parallel execution)
    temp_file_path = f'/path/to/temp_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
    with open(temp_file_path, 'w') as file:
        json.dump(transformed_data, file)


def upload_to_new_table():
    # Read the data from the JSON file
    temp_file_path = f'/path/to/temp_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
    with open(temp_file_path, 'r') as file:
        transformed_data = json.load(file)

    # Upload the data to the new_translations table
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()

    # Insert the transformed data into the new table
    insert_query = '''
        INSERT INTO new_translations (original_sentence, german_translation, dutch_translation, spanish_translation, french_translation)
        VALUES (?, ?, ?, ?, ?)
    '''
    cursor.executemany(insert_query, transformed_data)

    conn.commit()
    conn.close()


# Define the PythonOperator to transform data and save to a file
transform_data_task = PythonOperator(
    task_id='transform_data_task',
    python_callable=transform_data_and_save,
    dag=dag,
)

# Define the PythonOperator to upload data to the new table
upload_to_new_table_task = PythonOperator(
    task_id='upload_to_new_table_task',
    python_callable=upload_to_new_table,
    dag=dag,
)

# Set the task dependencies
transform_data_task >> upload_to_new_table_task
