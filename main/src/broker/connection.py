import pika


class Connection:
    def __init__(self, host='localhost', queue='default'):
        self.queue = queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)

    def close(self):
        self.connection.close()
