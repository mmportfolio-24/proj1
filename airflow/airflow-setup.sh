# for Windows, run using "./compose-refresh.sh", and run using Git app
# https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
# mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env