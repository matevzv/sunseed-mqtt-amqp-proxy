#!/usr/bin/env python

import sys
import time
import pika
import paho.mqtt.client as mqtt

HOST = "bpl-sunrabbit1.ts.telekom.si"
EXCHANGE = "wams_exchange"
ROUTING_KEY = "wams.pmc"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE,
                         type="topic", durable=True)

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("pmc/+")

def on_message(client, userdata, msg):
    if '"ts":' not in msg.payload:
        msg_ts = msg.payload.split(',', 1)
        msg_ts[0] += ',"ts":'+str(int(round(time.time() * 1000)))
        msg.payload = ",".join(msg_ts)

    channel.basic_publish(exchange=EXCHANGE,
                        routing_key=ROUTING_KEY,
                        body=str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)

client.loop_forever()
