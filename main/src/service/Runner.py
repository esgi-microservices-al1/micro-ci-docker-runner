import docker
from docker.types import Mount
from src.service.StatusService import *

class Runner:
    def __init__(self, path):
        self.statusService = StatusService()

        self.client = docker.from_env()
        self.image, logs = self.client.images.build(path=f'/projects/{path}', dockerfile='Dockerfile')
        mounts = [Mount(target="/var/run/docker.sock", source="/var/run/docker.sock", type='bind')]
        self.container = self.client.containers.run(image=self.image.id, tty=True, detach=True, mounts=mounts)
        self.statusService.add_image_ids(self.image.id, self.container.id, path)

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
        self.client.images.remove(self.image.id)
        self.statusService.delete_by_image_id(image_id)
