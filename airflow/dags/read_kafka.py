# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# from __future__ import annotations

import functools
import json
import logging
from datetime import datetime, timedelta

from airflow import DAG

# This is just for setting up connections in the demo - you should use standard
# methods for setting these connections in production
from airflow.operators.python import PythonOperator
from airflow.providers.apache.kafka.operators.consume import ConsumeFromTopicOperator

default_args = {
    "owner": "airflow",
    "depend_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}



def load_connections():
    # Connections needed for this example dag to finish
    from airflow.models import Connection
    from airflow.utils import db

    db.merge_conn(
        Connection(
            conn_id="donki-cme-broker",
            conn_type="kafka",
            extra=json.dumps({"bootstrap.servers": "broker:9092",
                    "group.id": "donki-cme-reader-z1",
                    "enable.auto.commit": False,
                    "auto.offset.reset": "beginning"})

            
        )
    )

consumer_logger = logging.getLogger("airflow")


def consumer_function(messages, prefix=None):
    for message in messages:
        key = message.key()
        value = message.value()
        topic = message.topic()
        offset = message.offset()
        # print("%s %s @ %s; %s : %s", prefix, message.topic(), message.offset(), key, value)
        # consumer_logger.info("%s %s @ %s; %s : %s", prefix, message.topic(), message.offset(), key, value)
        print("%s %s @ %s; %s : %s", prefix, topic, offset, key, value)
        consumer_logger.info("%s %s @ %s; %s : %s", prefix, topic, offset, key, value)
    return


with DAG(
    "read_kafka",
    default_args=default_args,
    description="Read NASA DONKI CME Data From Kafka",
    schedule=None,
    start_date=datetime(2024, 10, 1),
    catchup=False,
    tags=["DONKI"],
) as dag:

    t0 = PythonOperator(task_id="load_connections", python_callable=load_connections)
    t0.doc_md = "Establishes Kafka cluster connections."


    t1 = ConsumeFromTopicOperator(
        kafka_config_id="donki-cme-broker",
        task_id="read_from_kafka",
        topics=["donki-cme"],
        apply_function_batch=functools.partial(consumer_function, prefix="consumed:::"),
        commit_cadence="end_of_batch",
        max_messages=30,
        max_batch_size=10,
    )
    t1.doc_md = "Reads data from the `donki-cme` topic of the kafka cluster."

    
    t0 >> t1