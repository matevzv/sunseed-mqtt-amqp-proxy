#!/usr/bin/env python

import pika
import paho.mqtt.client as mqtt

HOST = "bpl-sunrabbit1.ts.telekom.si"
EXCHANGE = "wams_exchange"
QUEUE_NAME = "wams_save_queue"
ROUTING_KEY = "wams.spm"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE,
                         type="topic", durable=True)

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("spm/+")

def on_message(client, userdata, msg):
    if '"report_n":49' in msg.payload:
        channel.basic_publish(exchange=EXCHANGE,
                          routing_key=ROUTING_KEY,
                          body=str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)

client.loop_forever()
