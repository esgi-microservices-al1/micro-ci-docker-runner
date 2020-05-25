import docker
import os


class Runner:
    def __init__(self):
        client = docker.from_env()
        fname = '/opt/project/DockerTest'
        path = os.path.dirname(fname)
        image, logs = client.images.build(path=path, dockerfile='DockerTest')
        self.container = client.containers.run(image=image.id, tty=True, detach=True)

        for logLine in logs:
            print(logLine)

    def run(self, command, demux):
        if demux:
            cmdLogs = self.container.exec_run(command, stdout=True, stderr=True, stdin=False, tty=True, detach=False, demux=True)
        else:
            cmdLogs = self.container.exec_run(command, stdout=True, stderr=True, stdin=False, tty=True, detach=False)
        print(cmdLogs)

    def stop(self):
        self.container.stop()
        self.container.remove()
