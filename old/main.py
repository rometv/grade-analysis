from datetime import datetime

from airflow import DAG
from airflow.decorators import task

with DAG(
        dag_id='generate_analysis_charts',
        schedule='*/3 * * * *',  # <-- Cron expression
        start_date=datetime(2023, 4, 8),
        catchup=False,
        tags=["analysis"]) as dag:
    """
    # Data unpacking
    Data is unpacked using the unpacker function.
    """


    @task()
    def unpack_data(data_url):
        from unpacker import unpack
        return unpack(data_url)


    """
    # Data analysing
    Data is analysed and visualised using the Altair library.
    """


    @task()
    def analyse_data(submissions, sys_users, submissions_per_student, all_in_one):
        from analysis import analyse
        analyse(submissions, sys_users, submissions_per_student, all_in_one)


    url = 'https://drive.google.com/uc?export=download&id=1IxGl4Oj2mYPyULvLRS1B_UmbXE8N984s'
    subs, users, per_student, aio = unpack_data(url)
    analyse_data(subs, users, per_student, aio)
