from dataclasses import dataclass, field

from main.src.broker.connection import Connection
from main.src.service.Runner import Runner
import json


@dataclass
class Message:
    connection = Connection()

    def send(self, message):
        self.connection.channel.basic_publish(exchange='',
                                              routing_key=self.connection.queue,
                                              body=message)
        print(' [x] Sent', message)

    def receive(self, limit):
        i = 0
        while True:
            if limit and i >= limit:
                break
            result = self.connection.channel.basic_get(queue=self.connection.queue, auto_ack=False)
            if not result[0]:
                print('Channel Empty.')
                break
            print(' [x] Received', result[2])
            self.connection.channel.basic_ack(result[0].delivery_tag)
            i += 1
        self.connection.channel.close()
        self.connection.close()

    def liveReceive(self):
        self.connection.channel.basic_consume(queue=self.connection.queue,
                                              on_message_callback=self.callbackMessage,
                                              auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.connection.channel.start_consuming()

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
            # self.send(msg_out)
            print(msg_out)
            i += 1
        runner.stop()
