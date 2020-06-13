import os
from main.src.broker.connection import Connection
from main.src.service.Runner import Runner
import json


class Message:
    connection_in = Connection(os.getenv('BROKER_HOST'), os.getenv('BROKER_QUEUE_IN'), int(os.getenv('BROKER_PORT')))
    connection_out = Connection(os.getenv('BROKER_HOST'), os.getenv('BROKER_QUEUE_OUT'), int(os.getenv('BROKER_PORT')))

    def send(self, message):
        self.connection_out.channel.basic_publish(exchange='',
                                                  routing_key=self.connection_in.queue,
                                                  body=message)
        print(' [x] Sent', message)

    def receive(self, limit):
        i = 0
        while True:
            if limit and i >= limit:
                break
            result = self.connection_in.channel.basic_get(queue=self.connection_in.queue, auto_ack=False)
            if not result[0]:
                print('Channel Empty.')
                break
            print(' [x] Received', result[2])
            self.connection_in.channel.basic_ack(result[0].delivery_tag)
            i += 1
        self.connection_in.channel.close()
        self.connection_in.close()

    def liveReceive(self):
        self.connection_in.channel.basic_consume(queue=self.connection_in.queue,
                                                 on_message_callback=self.callbackMessage,
                                                 auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.connection_in.channel.start_consuming()

    def callbackMessage(self, ch, method, properties, body):
        print(' [x] Received ', body)
        commands = json.loads(body)
        process = commands['process_id']
        project = commands['project_path']
        runner = Runner(project)
        i = 0
        for item in commands['commands']:
            rowOut = runner.run(item['command'])
            msg_out = {
                'process_id': process,
                'command': item['command'],
                'output': {
                    'stdout': rowOut.output[0] if rowOut.exit_code == 0 else '',
                    'stderr': rowOut.output[0] if rowOut.exit_code != 0 else '',
                    'status': 'success' if rowOut.exit_code == 0 else 'error'
                },
                'status': i
            }
            self.send(msg_out)
            i += 1
        runner.stop()
