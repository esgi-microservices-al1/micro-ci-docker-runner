import os
from main.src.broker.connection import Connection
from main.src.broker.message import *
from main.src.service.Runner import Runner


if __name__ == "__main__":
    msg = Message()
    msg.liveReceive()
    # msg.connection.close()
