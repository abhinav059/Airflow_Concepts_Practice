from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import datetime, timedelta
import requests



default_args = {
    'owner': 'Abhinav',
    'start_date': datetime(2024, 9, 29),
    'schedule_interval': '@daily',
    'catchup': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id = 'ETL_Server_Access_Log_Processing',
    default_args=default_args,
    description='DAG to process server access logs'
    
)

def extract_file():
    url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt'
    response = requests.get(url)
    file_path = '/Users/abhinavkumar/Desktop/dataload/web-server-access-log.txt'
    
    with open(file_path, 'wb') as f:
        f.write(response.content)
    
    return file_path

def transform_data():
    file_path = extract_file()
    
    df = pd.read_csv(file_path, delim_whitespace=True, header=None,
                     names=['timestamp', 'latitude', 'longitude', 'visitorid', 
                            'accessed_from_mobile', 'browser_code'])
    
    df['visitorid'] = df['visitorid'].str.upper()
    transformed_data = df[['timestamp', 'visitorid']]
    
    output_file_path = '/Users/abhinavkumar/Desktop/dataload/capitalized.txt'
    transformed_data.to_csv(output_file_path, index=False, header=False)
    
    return output_file_path

def load_data():
    output_file_path = transform_data()
    print(f'Transformed data saved to: {output_file_path}')

extract_task = PythonOperator(
    task_id='extract_file',
    python_callable=extract_file,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

extract_task >> transform_task >> load_task
