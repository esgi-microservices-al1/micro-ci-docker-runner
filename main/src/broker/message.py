from main.src.broker.connection import Connection


def send(message, connection: Connection):
    connection.channel.basic_publish(exchange='',
                                     routing_key=connection.queue,
                                     body=message)
    print(' [x] Sent', message)


def receive(connection: Connection, limit):
    i = 0
    while True:
        if limit and i >= limit:
            break
        result = connection.channel.basic.get(queue=connection.queue,
                                              no_ack=False)
        if not result:
            print('Channel Empty.')
            break
        print(' [x] Received', result['body'])
        connection.channel.basic_ack(result['method']['delivery_tag'])
        i += 1
    connection.channel.close()
    connection.close()


def liveReceive(connection: Connection):
    connection.channel.basic_consume(queue=connection.queue,
                                     on_message_callback=callback,
                                     auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    connection.channel.start_consuming()


def callback(ch, method, properties, body):
    print(' [x] Received ', body)
