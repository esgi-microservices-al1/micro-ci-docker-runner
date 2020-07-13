import os
import threading
import docker
import datetime

from flask import Flask
from flask_cors import CORS
from src.service.StatusService import *
from time import sleep

app = Flask(__name__)
CORS(app)


@app.route('/stats')
def getStats():
    responses = {'datas': []}
    statusService = StatusService()
    while StatusService.inUse:
        sleep(0.10)
    statusService.read()
    for image_container_id in StatusService.image_container_ids:
        created = datetime.datetime.strptime(image_container_id[3], '%Y-%m-%d %H:%M:%S.%f')
        difference = datetime.datetime.now() - created
        print('datetime.datetime.now() : '+str(datetime.datetime.now()))
        print('created : '+str(created))
        print('str(difference) : '+str(difference))
        response = {'image_id': image_container_id[0], 'container_id': image_container_id[1],
                    'project_id': image_container_id[2], 'uptime': str(difference)}
        responses['datas'].append(response)
    print(responses)
    return responses


@app.route('/check')
def getCheck():
    return 'OK', 200


class ApiService(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        app.run(host="0.0.0.0", port=os.getenv('API_PORT'))
