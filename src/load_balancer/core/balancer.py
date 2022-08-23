'''
 # SpinachSocket - a metric load balancer with multi-threading
 # Copyright (C) 2022  Santiago González <https://github.com/sgtrusty>
 #             ~ Assembled through trust in coffee. ~
 #
 # This program is free software; you can redistribute it and/or modify
 # it under the terms of the CC BY-NC-ND 4.0 as published by
 # the Creative Commons; either version 2 of the License, or
 # (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # CC BY-NC-ND 4.0 for more details.
 #
 # You should have received a copy of the CC BY-NC-ND 4.0 along
 # with this program; if not, write to the  Creative Commons Corp.,
 # PO Box 1866, Mountain View, CA 94042.
 #
'''

import socket
import logging
import asyncio

from multiprocessing import Queue

from core.mapper import SocketMapper
from core.policies import DEFAULT_POLICIES
logger = logging.getLogger('Socket')


# Class for setting up socket for accepting client requests.
class SpinachBalancer:
    __MAGIC_NUMBER = 50
    __meta = {}
    __terminated = False
    # TODO: Move 'routes' to json/toml/yaml type 'default_routes' file
    def __init__(self, addr, routes=['route001', 'route002', 'route003'], policies=DEFAULT_POLICIES):
        self.__routes = routes
        self.__policies = policies
        self.__balancer_socket = self.create_socket(addr)

        self.__total_connections = Queue()
        list(map(self.__total_connections.put, [True for _ in range(self.__MAGIC_NUMBER)]))

    async def handle_client(self, reader, writer):
        mapper = SocketMapper(self.__policies, self.__routes, reader, writer)
        await mapper.read_client()
        writer.close()

    def create_socket(self, addr):
        loop = asyncio.get_event_loop()
        loop.create_task(asyncio.start_server(self.handle_client, addr[0], addr[1]))
        loop.run_forever()
        return loop

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        logger.info('Accepted connection from client address %s:%s', *addr)
        
