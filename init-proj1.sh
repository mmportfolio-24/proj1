echo -------------------------------------------------
echo AIRFLOW USER ID
echo -------------------------------------------------
cd airflow
bash airflow-setup.sh
cd ..

echo -------------------------------------------------
echo RUNNING DOCKER COMPOSE TO START REQUIRED SERVICES
echo -------------------------------------------------
docker compose up -d
sleep 5s
echo -------------------------------------------------
echo CREATING KAFKA TOPIC
echo -------------------------------------------------
cd kafka
if [[ "$OSTYPE" == "msys" ]]; then 
    docker exec --workdir //opt/kafka/bin/ broker sh -c "./kafka-topics.sh --bootstrap-server broker:9092 --create --if-not-exists --topic donki-cme"
else 
    docker exec --workdir /opt/kafka/bin/ broker sh -c "./kafka-topics.sh --bootstrap-server broker:9092 --create --if-not-exists --topic donki-cme"
fi
echo -------------------------------------------------
echo VERIFY KAFKA TOPIC EXISTS
echo -------------------------------------------------
if [[ "$OSTYPE" == "msys" ]]; then 
    docker exec --workdir //opt/kafka/bin/ broker sh -c "./kafka-topics.sh --bootstrap-server broker:9092 --list"
else 
    docker exec --workdir /opt/kafka/bin/ broker sh -c "./kafka-topics.sh --bootstrap-server broker:9092 --list"
fi

sleep 22s
echo -------------------------------------------------
echo SETUP DONE
echo -------------------------------------------------