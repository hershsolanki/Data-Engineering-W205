#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType

# Specify the schema here. Note I added two fields at the top to reflect sword_purchases, and one field at the bottom
# as my additional pieces of metadata
def join_guild_event_schema():
    
    return StructType([
        StructField("raw_event", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User_Agent", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("guild_type", StringType(), True)
    ])

# Tells us what event this is - sword or guild
@udf('boolean')
def is_join_guild(event_as_json):
    """udf for filtering events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'join_guild':
        return True
    return False


def main():
    """main
    """
    #  Start spark session
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

    #     Have to specificy this to match the schema above. Tells us we are looking at data from guilds only
    guild_join = raw_events \
        .filter(is_join_guild(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          join_guild_event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.Accept', 'json.Host', 'json.User_Agent', 'json.event_type', 'json.guild_type')
    
    # Check every 120 seconds for new updates. Sink as the namesake.
    sink = guild_join \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_guild_join") \
        .option("path", "/tmp/guild_join") \
        .trigger(processingTime="120 seconds") \
        .start()

    sink.awaitTermination()


if __name__ == "__main__":
    main()
