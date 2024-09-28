from airflow.decorators import dag, task
from datetime import timedelta
from datetime import datetime




default_args = {
    "owner" : "Abhinav",
    "retries" : 5,
    "retry_delay" : timedelta(minutes=5)
}

@dag(dag_id = "dag_taskflow_api",
     default_args=default_args,
     start_date = datetime(2024, 9, 29),
     schedule_interval="@daily"
     )
def hello_world_etl():
    
    @task()
    def get_name():
        return "Akaash"
    
    @task()
    def get_age():
        return 19
    
    @task()
    def greet(name, age):
        print(f"hello world, my name is {name} and i am {age} years old")

    name = get_name()
    age = get_age()
    greet(name = name, age = age)


greet_dag = hello_world_etl()
    