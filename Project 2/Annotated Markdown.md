```
cd w205 
```

```
ls
```

```
cd project-2-honlineh
```

Spinning up the cluster.
```
docker-compose up -d
```

Check the Kafka Logs
```
docker-compose logs -f kafka
```


This creates the topic, and we name it "assessments" after taking a look at the file in a JSON viewer. We only need 1 partition, and we specificy the Zookeper port. All of this is happening in Kafka
```
  docker-compose exec kafka   
  kafka-topics     
  --create     
  --topic assessments     
  --partitions 1    
  --replication-factor 1     
  --if-not-exists     
  --zookeeper zookeeper:32181

```
Download the Dataset
```
curl -L -o assessment-attempts-20180128-121051-nested.json https://goo.gl/ME6hjp`
```
Use Kafkacat to publish the json through Kafka, on the topic assesements. Note listens in on.kafka:29092
```
docker-compose exec mids \
  bash -c "cat /w205/project-2-honlineh/assessment-attempts-20180128-121051-nested.json \
    | jq '.[]' -c \
    | kafkacat -P -b kafka:29092 -t assessments"

```

Usually, I would spin up PySpark in the terminal. However, using this to connect to Jupyter notebook. Here, had to configure the firewall to allow port 8888 at IP 0.0.0.0.
```
docker-compose exec spark \
  env \
    PYSPARK_DRIVER_PYTHON=jupyter \
    PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --port 8888 --ip 0.0.0.0 --allow-root' \
  pyspark  
```  
  
 NOW, everything happens in Pyspark. For this, visit the Jupyter notebook that is entitled "Pyspark side".
 This shuts down docker.
```
  docker-compose down

```

  
  
  
  
  
