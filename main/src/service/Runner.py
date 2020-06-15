import docker


class Runner:
    def __init__(self, path):
        client = docker.from_env()
        image, logs = client.images.build(path=path, dockerfile='Dockerfile')
        self.container = client.containers.run(image=image.id, tty=True, detach=True)

        for logLine in logs:
            print(logLine)

    def run(self, command):
        cmdLogs = self.container.exec_run(command, stdout=True, stderr=True, stdin=False, tty=True, detach=False, demux=True)
        print(cmdLogs)
        return cmdLogs

    def stop(self):
        self.container.stop()
        self.container.remove()
