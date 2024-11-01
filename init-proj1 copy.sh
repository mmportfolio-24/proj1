echo "--------------------------------"
echo "RUNNING KAFKA SETUP"
echo "--------------------------------"

cd kafka
bash ./init-kafka.sh
cd ..

echo "--------------------------------"
echo "RUNNING AIRFLOW SETUP"
echo "--------------------------------"

cd airflow
bash ./init-airflow.sh
cd ..

echo "--------------------------------"
echo "ALLOWING AIRFLOW 2m TO COLD START"
echo "--------------------------------"
sleep 2m

echo "--------------------------------"
echo "END PROJ1 SETUP"
echo "--------------------------------"
read -p ""