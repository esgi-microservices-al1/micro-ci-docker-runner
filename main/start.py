import os

from src.broker.message import *
from src.consul.consul import ConsulService

if __name__ == "__main__":
    consul = ConsulService(port=int(os.getenv('CONSUL_PORT')),
                           host=os.getenv('CONSUL_HOST'),
                           service_id=os.getenv('CONSUL_SERVICE_ID'),
                           token=os.getenv('CONSUL_TOKEN'),
                           tags=['traefik.enable=true',
                                 'traefik.frontend.entryPoints=http',
                                 'traefik.frontend.rule=PathPrefixStrip:/al1.runner-ci/'],
                           service_name=os.getenv('CONSUL_SERVICE_NAME'))

    consul.register()
    consul.check_process()
    # consul.deregister_check('8')
    # consul.deregister_service('123456')

    msg = Message()
    msg.liveReceive()
    # msg.connection.close()
