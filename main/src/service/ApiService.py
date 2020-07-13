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
    client = docker.APIClient()
    statusService = StatusService()
    while StatusService.inUse:
        sleep(0.10)
    statusService.read()
    for image_container_id in StatusService.image_container_ids:
        image2 = client.inspect_image(image_container_id[0])
        created_base = image2.get('Created')[:-4] + 'Z'
        created = datetime.datetime.strptime(created_base, "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(hours=2)
        difference = datetime.datetime.now() - created
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
