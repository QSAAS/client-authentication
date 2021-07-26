from django.core.management.base import BaseCommand, CommandError
import environ
import time
import pika
import json

from reservations.models import QueueNode

env = environ.Env()


class Command(BaseCommand):
    help = 'Digests an event from rabbit mq'

    def handle(self, *args, **options):
        self.stdout.write("Starting event handler")
        # time.sleep(10)
        connection = pika.BlockingConnection(pika.URLParameters(env.str("RABBIT_MQ_URL")))
        self.stdout.write("Connected to RMQ")
        channel = connection.channel()
        channel.queue_declare(queue='EventBus_ClientAuthentication')
        channel.queue_bind(exchange='EventBus',
                           queue='EventBus_ClientAuthentication')
        channel.basic_consume(queue='EventBus_ClientAuthentication',
                              auto_ack=True,
                              on_message_callback=self.digest)
        channel.start_consuming()

    def digest(self, ch, method, properties, body):
        self.stdout.write("Received message %s" % body)
        obj = json.loads(body)
        # todo future work
        if obj['eventName'] != "QueueNodeCreated":
            return
        queue_node_id = obj["id"]["id"]
        node = QueueNode(id=queue_node_id, last_number_in_queue=0)
        node.save()
