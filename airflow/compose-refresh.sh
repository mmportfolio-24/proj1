# for Windows, run using "./compose-refresh.sh", and run using Git app
# https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.2/docker-compose.yaml'

## change these in "docker-compose.yaml" after refreshing:
##     # image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.10.2}
##     build: .
##     AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
