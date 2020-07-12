import os
from src.broker.connection import Connection
from src.service.Runner import Runner
import json


def checkIntegrity(commands):
    if not all(k in commands for k in ('project_id', 'commands')):
        print("Missing project_id or commands parameter")
        return False
    for command in commands['commands']:
        if not all(k in command for k in ('command', 'stdout')):
            print("Invalid command")
            return False
    if not os.path.exists(f'/projects/{commands["project_id"]}/Dockerfile'):
        print("Dockerfile doesnt exist at the destination")
        return False
    return True


class Message:
    connection_in = Connection(os.getenv('BROKER_HOST'), os.getenv('BROKER_QUEUE_IN'), int(os.getenv('BROKER_PORT')))
    connection_out = Connection(os.getenv('BROKER_HOST'), os.getenv('BROKER_QUEUE_OUT'), int(os.getenv('BROKER_PORT')))

    def send(self, message):
        self.connection_out.channel.basic_publish(exchange='',
                                                  routing_key=self.connection_out.queue,
                                                  body=message)
        print(' [x] Sent', message)

    def sendToUs(self, message):
        self.connection_in.channel.basic_publish(exchange='',
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
        if not checkIntegrity(commands):
            print(' error: Invalid message')
            return
        process = commands['project_id']
        # project = commands['project_path']
        runner = Runner(process)
        i = 0
        for item in commands['commands']:
            rowOut = runner.run(item['command'])
            stdout = ""
            if rowOut.exit_code == 0 and rowOut.output[0] is not None:
                stdout = str(rowOut.output[0], 'utf-8')
            stderr = ""
            if rowOut.exit_code != 0 and rowOut.output[0] is not None:
                stderr = str(rowOut.output[0], 'utf-8')
            status = "success"
            if rowOut.exit_code != 0:
                status = "error"
            msg_out = '{'
            msg_out += '"process_id": ' + str(process) + ','
            msg_out += '"command": "' + str(item['command']) + '",'
            msg_out += '"output": {'
            msg_out += '"stdout": "' + stdout + '",'
            msg_out += '"stderr": "' + stderr + '",'
            msg_out += '"status": "' + status + '"'
            msg_out += '},'
            msg_out += '"status": ' + str(i)
            msg_out += '}'

            self.send(msg_out)
            i += 1
        runner.stop()

