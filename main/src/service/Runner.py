import docker
from docker.types import Mount
from src.service.StatusService import *
import requests
import datetime


class Runner:
    def __init__(self, path, statusService):
        self.statusService = statusService
        self.client = docker.from_env()
        self.image, logs = self.client.images.build(path=f'/projects/{path}', dockerfile='Dockerfile')
        mounts = [Mount(target="/var/run/docker.sock", source="/var/run/docker.sock", type='bind')]
        self.container = self.client.containers.run(image=self.image.id, tty=True, detach=True, mounts=mounts)
        self.statusService.add_image_ids(self.image.id, self.container.id, path, datetime.datetime.now())

        for logLine in logs:
            print(logLine)

    def run(self, command):
        cmdLogs = self.container.exec_run(command, stdout=True, stderr=True, stdin=False, tty=True, detach=False, demux=True)
        print(cmdLogs)
        return cmdLogs

    def stop(self):
        self.container.stop()
        self.container.remove()
        image_id = self.image.id
        if self.statusService.checkIfOtherImage(image_id) == 1:
            print("before remove image")
            try:
                self.client.images.remove(self.image.id)
            except (requests.exceptions.HTTPError, docker.errors.APIError):
                print("Image used by other container")
            print("done delete image")
        self.statusService.delete_by_image_id(image_id)
        print("removed container and image")
