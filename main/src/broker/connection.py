import pika


class Connection:
    def __init__(self, host, queue, port):
        self.queue = queue
        credentials = pika.PlainCredentials("user", "pwd")
        params = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
        # params = pika.ConnectionParameters(host=host, port=port)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)

    def close(self):
        self.connection.close()
