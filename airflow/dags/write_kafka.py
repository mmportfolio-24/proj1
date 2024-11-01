import requests
import json
from datetime import datetime, timedelta
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
# import airflow.models.taskinstance
import logging

# https://ccmc.gsfc.nasa.gov/support/DONKI-webservices.php

# Coronal Mass Ejection (CME):
# https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/CME?startDate=yyyy-MM-dd&endDate=yyyy-MM-dd
# startDate: default to 30 days prior to current UTC date
# endDate: default to current UTC date

# return JSON object:
# activityID, startTime, sourceLocation, activeRegionNum, instruments, cmeAnalyses, linkedEvents[(list of) activityID], note, catalog 


def load_connections():
    # Connections needed for this example dag to finish
    from airflow.models import Connection
    from airflow.utils import db

    db.merge_conn(
        Connection(
            conn_id="donki-cme-broker",
            conn_type="kafka",
            extra=json.dumps({"socket.timeout.ms": 10, "bootstrap.servers": "broker:9092"})
            # extra=json.dumps({"socket.timeout.ms": 10, "bootstrap.servers": "localhost:9092"})
            # extra=json.dumps({"socket.timeout.ms": 10, "bootstrap.servers": "broker:29092"})
            # extra=json.dumps({"socket.timeout.ms": 10, "bootstrap.servers": "localhost:29092"})

            
        )
    )


def getCME():
    #get data
    endpoint = "https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/CME"
    startDate= (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    params = f"?startDate={startDate}"
    j = requests.get(url=(endpoint+params)).json()

    #log result
    logging.info(f"The Response from DONKI CME API was: {j}")
    
    #format messages, activityID is the key, all other data is the value
    df = pd.DataFrame().from_records(data=j, index="activityID")
    messages = df.to_dict(orient="index")

    #send to ProduceToTopicOperator
    for key, value in messages.items():
        str_value = str(value)
        logging.info(f"Sending msg to Producer function: {key}: {str_value}")
        yield (key, str_value)


default_args = {
    "owner": "airflow",
    "depend_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="write_kafka",
    default_args=default_args,
    description="Write NASA DONKI CME Data To Kafka",
    schedule="@hourly",
    start_date=datetime(2024, 10, 1),
    catchup=False,
    tags=["DONKI"],
) as dag:
    
    t0 = PythonOperator(task_id="load_connections", python_callable=load_connections, do_xcom_push=False)
    t0.doc_md = "Establishes Kafka cluster connections."


    t1 = ProduceToTopicOperator(
        kafka_config_id="donki-cme-broker",
        task_id="write_to_kafka",
        topic="donki-cme",
        producer_function=getCME
    )
    t1.doc_md = "Gets & formats DONKI CME JSON data and sends to the `donki-cme` topic of the kafka cluster."

    t0 >> t1