from src.broker.message import *


if __name__ == "__main__":
    msg = Message()
    msg.liveReceive()
    # msg.connection.close()
