# APACHE AIRFLOW & APACHE KAFKA
mmulkey.dev

## DESCRIPTION
This project is for fun, not production-ready, and was for the purposes of learning more about the technologies involved.
This project runs Airflow & Kafka together in a single Docker container.
One topic "donki-cme" will be created automatically by following the steps below.
The Airflow instance contains two DAGs, one to write to Kafka, and one to read from Kafka.
The data is retrieved from the NASA DONKI API by the "write_kafka" DAG.
The results are written to the Kafka topic by the "write_kafka" DAG, and are consumed by the "read_kafka" DAG on-demand.
DAGs are disabled by default.

## STEPS TO RUN FOR YOURSELF

- make sure you have DOCKER installed on your machine
- download my code from GITHUB
- in a terminal window, navigate to the   \proj1   directory
- run:   ./init-proj1.sh   to create the local Airflow/Kafka instances (NOTE: I have only tested this on Windows. "Should" work on UNIX/Linux)
- login to Airflow in a browser by going to http://localhost:8080/ (username & password are both the default "airflow")
- enable & trigger the "read_kafka" DAG and check the task output (no data yet)
- enable & trigger the "write_kafka" DAG to produce the data
- trigger the "read_kafka" DAG again & check the task output (data will be present now)