from src.broker.message import Message

msg = Message()
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
