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
    timeout: int = field(default=100)
    ttl_timeout: str = field(default='40s')
    consul: Consul = field(init=False)
    service_name: str = field(default='al1.docker.runner')

    def __post_init__(self) -> None:
        self.consul = consul.Consul(port=self.port, host=self.host, token=self.token)

    def register(self) -> None:
        self.consul.agent.service.register(self.service_name,
                                           tags=self.tags,
                                           service_id=self.service_id,
                                           timeout=self.timeout,
                                           check=Check.ttl(self.ttl_timeout))

    def deregister_check(self, check_id: str) -> None:
        self.consul.agent.check.deregister(check_id)

    def deregister_service(self, check_id: str) -> None:
        self.consul.agent.service.deregister(check_id)

    def _check(self) -> None:
        self.consul.agent.check.ttl_pass(f'service:{self.service_id}')

    def _tempo(self, scheduler) -> None:
        self._check()
        s.enter(TIMEOUT, 1, self._tempo, (scheduler,))

    def check_process(self) -> None:
        s.enter(TIMEOUT, 1, self._tempo, (s,))
        t = Thread(target=s.run)
        t.start()
