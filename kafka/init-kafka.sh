echo "--------------------------------"
echo "CREATING KAFKA BROKERS"
echo "--------------------------------"
docker compose up -d
sleep 22s

echo "--------------------------------"
echo "CREATING KAFKA TOPICS"
echo "--------------------------------"

# if [[ "$OSTYPE" == "msys" ]]; then 
#     docker exec --workdir //opt/kafka/bin/ broker-1 sh -c "./kafka-topics.sh --bootstrap-server broker-1:19092,broker-2:19092,broker-3:19092 --create --if-not-exists --topic donki-cme"
# else 
#     docker exec --workdir /opt/kafka/bin/ broker-1 sh -c "./kafka-topics.sh --bootstrap-server broker-1:19092,broker-2:19092,broker-3:19092 --create --if-not-exists --topic donki-cme"
# fi

if [[ "$OSTYPE" == "msys" ]]; then 
    docker exec --workdir //opt/kafka/bin/ broker-1 sh -c "./kafka-topics.sh --bootstrap-server localhost:9092 --create --if-not-exists --topic donki-cme"
else 
    docker exec --workdir /opt/kafka/bin/ broker-1 sh -c "./kafka-topics.sh --bootstrap-server localhost:9092 --create --if-not-exists --topic donki-cme"
fi

echo
echo "--------------------------------"
echo "LIST OF KAFKA TOPICS"
echo "--------------------------------"

# if [[ "$OSTYPE" == "msys" ]]; then 
#     docker exec --workdir //opt/kafka/bin/ broker-1 sh -c "./kafka-topics.sh --bootstrap-server broker-1:19092,broker-2:19092,broker-3:19092 --list"
# else 
#     docker exec --workdir /opt/kafka/bin/ broker-1 sh -c "./kafka-topics.sh --bootstrap-server broker-1:19092,broker-2:19092,broker-3:19092 --list"
# fi

if [[ "$OSTYPE" == "msys" ]]; then 
    docker exec --workdir //opt/kafka/bin/ broker-1 sh -c "./kafka-topics.sh --bootstrap-server localhost:9092 --list"
else 
    docker exec --workdir /opt/kafka/bin/ broker-1 sh -c "./kafka-topics.sh --bootstrap-server localhost:9092 --list"
fi

echo
echo "--------------------------------"
echo "END KAFKA SETUP..."
echo "--------------------------------"
