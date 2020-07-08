import os
import sched
import time
from threading import Thread

import consul
from dataclasses import dataclass, field
from typing import Text, List
from consul import Consul, Check

s = sched.scheduler(time.time, time.sleep)
TIMEOUT = 30


@dataclass
class ConsulService:
    port: int
    host: str
    service_id: str
    token: str
    tags: List[Text]
    address: str
    timeout: int = field(default=100)
    http_interval: str = field(default='40s')
    consul: Consul = field(init=False)
    service_name: str = field(default='al1.docker.runner')

    def __post_init__(self) -> None:
        self.consul = consul.Consul(port=self.port, host=self.host, token=self.token, scheme='http', verify=False)

    def register(self, url, timeout: int = TIMEOUT) -> None:
        self.consul.agent.service.register(self.service_name,
                                           tags=self.tags,
                                           service_id=self.service_id,
                                           address=self.address,
                                           port=8156,
                                           # timeout=self.timeout,
                                           check=Check.http(url=url,
                                                            interval=self.http_interval))

    def deregister_check(self, check_id: str) -> None:
        self.consul.agent.check.deregister(check_id)

    def deregister_service(self, check_id: str) -> None:
        self.consul.agent.service.deregister(check_id)
