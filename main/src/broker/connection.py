import pika
import os


class Connection:
    def __init__(self, host=os.getenv('BROKER_HOST'), queue=os.getenv('BROKER_QUEUE'), port=int(os.getenv('BROKER_PORT'))):
        self.queue = queue
        credentials = pika.PlainCredentials("user", "pwd")
        params = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
        # params = pika.ConnectionParameters(host=host, port=port)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)

    def close(self):
        self.connection.close()
