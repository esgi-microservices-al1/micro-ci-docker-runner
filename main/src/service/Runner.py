import docker
from docker.types import Mount


class Runner:
    def __init__(self, path):
        client = docker.from_env()
        image, logs = client.images.build(path=path, dockerfile='Dockerfile')
        mounts = [Mount(target="/var/run/docker.sock", source="/var/run/docker.sock", type='bind')]
        self.container = client.containers.run(image=image.id, tty=True, detach=True, mounts=mounts)

        for logLine in logs:
            print(logLine)

    def run(self, command):
        cmdLogs = self.container.exec_run(command, stdout=True, stderr=True, stdin=False, tty=True, detach=False, demux=True)
        print(cmdLogs)
        return cmdLogs

    def stop(self):
        self.container.stop()
        self.container.remove()
