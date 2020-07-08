import threading
import time
import docker
import datetime
import dateutil.parser

from flask import Flask
from src.service.StatusService import *

app = Flask(__name__)


@app.route('/stats')
def getStats():
    responses = {'datas': []}
    client = docker.APIClient()
    statusService = StatusService()
    statusService.read()
    for image_container_id in StatusService.image_container_ids:
        image2 = client.inspect_image(image_container_id[0])
        created_base = image2.get('Created')[:-4]+'Z'
        created = datetime.datetime.strptime(created_base, "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(hours=2)
        difference = datetime.datetime.now() - created
        response = {'image_id': image_container_id[0], 'container_id': image_container_id[1],
                    'project_id': image_container_id[2], 'uptime': str(difference)}
        responses['datas'].append(response)
    print(responses)
    return responses


@app.route('/check')
def getCheck():
    return 'Hello, from Team-Runner!'


class ApiService(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        app.run(port=8156)