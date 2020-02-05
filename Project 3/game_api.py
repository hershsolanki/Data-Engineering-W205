#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request
import random

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')


# Give a 1/5 chance to get an silver sword, 1/25 to get gold
def sword_type():
    sword = 'Bronze'
    number = random.randint(1,100)
    if number % 5 == 0:
        sword = 'Silver'
        if number % 25 == 0:
            sword = 'Gold'
    return sword
   
# 1/100 chance to get a discount
def discount():
    number = random.randint(1,101)
    if number % 100 == 0:
        return 'Yes'
    return 'No'

# Two types of guilds, with an even breakdown
def guild_assignment():
    number = random.randint(1,101)
    if number % 2 == 0:
        return '1'
    return '2'

# Log events to Kafka
def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())

# Not really used, only to make sure routes are working in the first place
@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"


# This is the purchase sword route, where we can specify type of sword, and whether or not there was a discount offered.
@app.route("/purchase_a_sword")
def purchase_a_sword():
    
    purchase_sword_event = {'event_type': 'purchase_sword',
                           'description' : sword_type(),
                           'discount' : discount()}
    log_to_kafka('events', purchase_sword_event)
    return "Sword Purchased!\n"

# We do the same for guild here. Note there are two types of guilds here.
@app.route("/join_guild")
def join_guild():
    
    join_guild_event = {'event_type': 'join_guild',
                       'guild_type' : guild_assignment()}
    log_to_kafka('events', join_guild_event)  
    return "Guild Joined\n"
