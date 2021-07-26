import json

import environ
import pika
from django.core.serializers.json import DjangoJSONEncoder

QUEUE_NAME = 'EventBus'

env = environ.Env()

connection = None
channel = None


def connect():
    global connection, channel
    if connection is None:
        connection = pika.BlockingConnection(pika.URLParameters(env.str("RABBIT_MQ_URL")))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
    return channel


def publish_event(obj):
    channel = connect()
    # TODO: IMPORTANT: Add a key "eventName" to the event (obj) dictionary (from caller)
    payload = json.dumps(obj, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
    channel.basic_publish(exchange='', routing_key='', body=bytes(payload, encoding='utf-8'))
