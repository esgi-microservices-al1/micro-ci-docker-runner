from src.broker.message import Message

msg = Message()
msg_out = {
    'process_id': 1,
    'command': "ls",
    'output': {
        'stdout': '',
        'stderr': '',
        'status': 'success'
    },
    'status': 6
}
msg.send(msg_out)


for i in range(1, 6):
    msg.sendToUs('''
        {
         "project_id": '''+str(i)+''',
         "commands": [
             {
                "command": "mkdir cc",
                "stdout": true
             },
             {
                "command": "ls",
                "stdout": true
             },
             {
                "command": "git poule",
                "stdout": false
             }
         ]
        }
        ''')
