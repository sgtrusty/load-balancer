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

from multiprocessing import Queue
from core.threading import ThreadHandler
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
        self.__selector_incoming = self.create_selector_incoming()
        self.__selector_outgoing = self.create_selector_outgoing()
        self.__queue_incoming = Queue()
        self.__routes = routes
        self.__policies = policies

        self.__total_connections = Queue()
        list(map(self.__total_connections.put, [True for _ in range(50)]))

    def create_selector_incoming(self):
        selector = selectors.DefaultSelector()
        selector.register(self.__balancer_socket, selectors.EVENT_READ, self.accept)
        return selector

    def create_selector_outgoing(self):
        selector = selectors.DefaultSelector()
        return selector

    def create_socket(self, addr):
        balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        balancer_socket.bind(addr)
        balancer_socket.listen()
        balancer_socket.setblocking(False)
        return balancer_socket

    def persist(self):
        self.__threader = ThreadHandler()
        self.__threader.submit(self.thread_selector, self.__selector_incoming)
        self.__threader.submit(self.thread_selector, self.__selector_outgoing)
        self.__threader.submit(self.thread_pool_incoming, self.__policies, self.__routes, self.__selector_outgoing)

    def thread_pool_incoming(self, policies, routes, selector_outgoing):
        while(not self.__terminated):
            try:
                if (not self.__queue_incoming.empty() and not self.__total_connections.empty()):
                    logger.debug('Total Connections size: %d', self.__total_connections.qsize())
                    logger.debug('Processing connection...')
                    new_connection = self.__queue_incoming.get()

                    mapper = SocketMapper(policies, routes, self.__total_connections)
                    mapper.add(new_connection)
            except Exception as err:
                logger.error(err)

    def thread_selector(self, selector):
        try:
            while(not self.__terminated):
                events = selector.select(timeout=1)
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)

        except Exception as err:
            logger.error(err)
            raise err

    def terminate(self):
        self.__terminated = True
        # destroy balancer_socket
        # destroy mapper
        self.__threader.terminate()
        self.__selector_incoming.close()
        self.__selector_outgoing.close()

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        logger.info('Accepted connection from client address %s:%s', *addr)
        self.__queue_incoming.put(conn)
        logger.debug('Queue Incoming size: %d', self.__queue_incoming.qsize())