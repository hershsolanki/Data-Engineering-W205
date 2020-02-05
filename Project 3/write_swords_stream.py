#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType


# Specify the schema here. Note I added two fields at the top to reflect sword_purchases, and two fields at the bottom
# as my additional pieces of metadata
def purchase_sword_event_schema():    
    return StructType([
        StructField("raw_event", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User_Agent", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("description", StringType(), True),
        StructField("discount", StringType(), True)
    ])


# Tells us what event this is - sword or guild
@udf('boolean')
def is_sword_purchase(event_as_json):
    """udf for filtering events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'purchase_sword':
        return True
    return False


def main():
    """main
    """
#     Start spark session
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()
    
#  Read data from Kafka, where we have exposed 29092
    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "events") \
        .load()
    
#     Have to specificy this to match the schema above. Tells us we are looking at data from swords only
    sword_purchases = raw_events \
    .filter(is_sword_purchase(raw_events.value.cast('string'))) \
    .select(raw_events.value.cast('string').alias('raw_event'),
            raw_events.timestamp.cast('string'),
            from_json(raw_events.value.cast('string'),
                      purchase_sword_event_schema()).alias('json')) \
    .select('raw_event', 'timestamp', 'json.Accept', 'json.Host',       'json.User_Agent', 'json.event_type', 'json.description', 'json.discount')
        

#     Check every 120 seconds for new updates
    sink = sword_purchases \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_sword_purchases") \
        .option("path", "/tmp/sword_purchases") \
        .trigger(processingTime="120 seconds") \
        .start()

#     Infinite loop
    sink.awaitTermination()


if __name__ == "__main__":
    main()
