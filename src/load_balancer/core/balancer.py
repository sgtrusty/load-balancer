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
import selectors
import queue

# from core.threading import ThreadHandler
from core.mapper import SocketMapper
from core.policies import DEFAULT_POLICIES
logger = logging.getLogger('Socket')

# Class for setting up socket for accepting client requests.
class SpinachBalancer:
    __meta = {}
    __terminated = False
    # TODO: Move 'routes' to json/toml/yaml type 'default_routes' file
    def __init__(self, addr, routes=['route001', 'route002', 'route003'], policies=DEFAULT_POLICIES):
        self.__balancer_socket = self.create_socket(addr)
        self.__selector = self.create_selector()
        self.__routes = routes
        self.__policies = policies

    def create_selector(self):
        selector = selectors.DefaultSelector()
        selector.register(self.__balancer_socket, selectors.EVENT_READ, self.accept)
        return selector

    def create_socket(self, addr):
        balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        balancer_socket.bind(addr)
        balancer_socket.listen()
        balancer_socket.setblocking(False)
        #__balancer_socket.listen(1)
        return balancer_socket

    def persist(self):
        # self.__threader = ThreadHandler()

        try:
            while(not self.__terminated):
                events = self.__selector.select(timeout=1)
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)

        except Exception as err:
            logger.error(err)
            raise err

    def terminate(self):
        # destroy balancer_socket
        # destroy mapper
        # self.__threader.terminate()
        self.__terminated = True

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        logger.info('Accepted connection from client address %s:%s', *addr)
        mapper = SocketMapper(self.__policies, self.__routes, self.__selector)
        mapper.add(conn)
        # self.__threader.submit(self.__handle_conn, conn)
        