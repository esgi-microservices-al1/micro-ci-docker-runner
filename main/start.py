import os

from src.broker.message import *
from src.consul.consul import ConsulService
from src.service.Runner import *
from src.service.ApiService import *

if __name__ == "__main__":
    api_thread = ApiService()
    api_thread.start()

    consul = ConsulService(port=int(os.getenv('CONSUL_PORT')),
                           host=os.getenv('CONSUL_HOST'),
                           service_id=os.getenv('CONSUL_SERVICE_ID'),
                           token=os.getenv('CONSUL_TOKEN'),
                           tags=['traefik.enable=true',
                                 'traefik.frontend.entryPoints=http',
                                 'traefik.frontend.rule=PathPrefixStrip:/al1.runner-ci/'],
                           address=os.getenv('API_HOST'),
                           service_name=os.getenv('CONSUL_SERVICE_NAME'))

    consul.register(url=f'http://{os.getenv("API_HOST")}:{os.getenv("API_PORT")}/check')

    msg = Message()
    msg.liveReceive()
    # msg.connection.close()
