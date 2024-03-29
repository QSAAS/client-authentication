import json
import environ
import pika
from django.core.serializers.json import DjangoJSONEncoder

EXCHANGE_NAME = 'EventBus'

env = environ.Env()

connection = None
channel = None


def connect():
    global connection, channel
    if connection is None or connection.is_closed:
        connection = pika.BlockingConnection(pika.URLParameters(env.str("RABBIT_MQ_URL")))
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')

    print("connected xD")


def publish_event(obj):
    print("Publishing event")
    global channel
    connect()
    print("Connected")
    print(channel)
    # TODO: IMPORTANT: Add a key "eventName" to the event (obj) dictionary (from caller)
    obj['eventName'] = 'ReservationCreated'
    payload = json.dumps(obj, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
    print("Publishing event %s" % payload)
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='', body=bytes(payload, encoding='utf-8'))
    print("Event published")
