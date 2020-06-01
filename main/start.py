import os
from main.src.broker.connection import Connection
from main.src.broker.message import *
from main.src.service.Runner import Runner


if __name__ == "__main__" :
    # runner = Runner()
    #
    # runner.run("touch test", False)
    # runner.run("ls", True)
    #
    # runner.stop()

    co = Connection(host=os.getenv('BROKER_HOST'), port=int(os.getenv('BROKER_PORT')), queue=os.getenv('BROKER_QUEUE'))
    liveReceive(co)
    co.close()
