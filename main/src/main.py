import docker
import os
client = docker.from_env()
fname = '/opt/project/DockerTest'
path = os.path.dirname(fname)
image, logs = client.images.build(path=path, dockerfile='DockerTest')
container = client.containers.run(image=image.id, tty=True, detach=True)

for logLine in logs:
    print(logLine)

cmdLogs = container.exec_run("touch test", stdout=True, stderr=True, stdin=False, tty=True, detach=False)
cmdLogs1 = container.exec_run("ls", stdout=True, stderr=True, stdin=False, tty=True, detach=False, demux=True)

print(cmdLogs)
print(cmdLogs1)

container.stop()
container.remove()

