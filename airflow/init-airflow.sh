echo "--------------------------------"
echo "AIRFLOW PREREQS"
echo "--------------------------------"
bash ./airflow-setup.sh

echo "--------------------------------"
echo "BUILDING AIRFLOW VIA DOCKER COMPOSE"
echo "--------------------------------"
docker compose up -d

echo "--------------------------------"
echo "END AIRFLOW SETUP..."
echo "--------------------------------"
