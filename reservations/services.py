import json

import environ
import pika

QUEUE_NAME = 'EventBus'

env = environ.Env()

print(env["RABBIT_MQ_URL"])
connection = pika.BlockingConnection(pika.ConnectionParameters(env.str("RABBIT_MQ_URL")))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)


def publish_event(obj):
    # TODO: IMPORTANT: Add a key "eventName" to the event (obj) dictionary (from caller)
    payload = json.dumps(obj)
    channel.basic_publish(exchange='', routing_key='', body=bytes(payload))