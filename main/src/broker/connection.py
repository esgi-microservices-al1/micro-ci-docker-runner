import pika
import os


class Connection:
    def __init__(self, host, queue, port):
        self.queue = queue
        credentials = pika.PlainCredentials(os.getenv('BROKER_LOGIN'), os.getenv('BROKER_PASSWORD'))
        params = pika.ConnectionParameters(host, port, '/', credentials=credentials)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)

    def close(self):
        self.connection.close()
