import pandas as pd
import psycopg2 as psql
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def connect_database(**kwargs):
    connection = psql.connect(
        user='airflow',
        password='airflow',
        host='postgres',
        port='5432',
        dbname='airflow'
    )

    df = pd.read_sql("select * from table_m3 limit 5000", connection)
    df.to_csv('/opt/airflow/dags/P2M3_Jonathan_Tuahta_Raw.csv')
    print("-------Data Saved------")

def cleaning_data(**kwargs):
    data = pd.read_csv('/opt/airflow/dags/P2M3_Jonathan_Tuahta_Raw.csv' )

    # renaming data
    data_renamed = data.rename(columns={
        'VIN (1-10)': 'VIN_(1-10)',
        'County': 'country',
        'City': 'city',
        'State': 'state',
        'Postal Code': 'postal_code',
        'Model Year': 'model_year',
        'Make': 'make',
        'Model': 'model',
        'Electric Vehicle Type': 'electric_vehicle_type',
        'Clean Alternative Fuel Vehicle (CAFV) Eligibility': 'clean_alternative_fuel_vehicle_eligibility',
        'Electric Range': 'electric_range',
        'Base MSRP': 'base_MSRP',
        'Legislative District': 'legislative_district',
        'DOL Vehicle ID': 'DOL_vehicle_ID',
        'Vehicle Location': 'vehicle_location',
        'Electric Utility': 'electric_utility',
        '2020 Census Tract': '2020_census_tract'})

    # drop missing values and drop duplicates data
    data_final = data_renamed.dropna().drop_duplicates()
    data_final.reset_index(inplace=True)

    # saved the clean dataframe
    data_final.to_csv('/opt/airflow/dags/P2M3_Jonathan_Tuahta_clean.csv', index=False)

def elasticsearch_indexing(**kwargs):
    es = Elasticsearch("http://elasticsearch:9200")
    try:
        dataframe = pd.read_csv('/opt/airflow/dags/P2M3_Jonathan_Tuahta_clean.csv')
        for i, r in dataframe.iterrows():
            doc = r.to_json()
            res = es.index(index="milestone3_jonathan", doc_type="doc", body=doc)
            print(res)
    except Exception as e:
        print(f"Error indexing data into Elasticsearch: {str(e)}")

default_args = {
    'owner': 'Jonathan Tuahta',
    'start_date': datetime(2023, 11, 21, 6, 30),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('milestone3',
         default_args=default_args,
         schedule_interval='@daily',
         ) as dag:

    getData = PythonOperator(
        task_id='QueryPostgreSQL',
        python_callable=connect_database,
        provide_context=True,
    )

    cleanData = PythonOperator(
        task_id='CleanData',
        python_callable=cleaning_data,
        provide_context=True,
    )

    insertData = PythonOperator(
        task_id='InsertDataElasticsearch',
        python_callable=elasticsearch_indexing,  # Changed the function name
        provide_context=True,
    )

    # Set task dependencies
    getData >> cleanData >> insertData
