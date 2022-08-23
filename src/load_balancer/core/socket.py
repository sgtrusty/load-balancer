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
import select
import queue
from enum import Enum

from core.threading import ThreadHandler
from core.socket_forward import FORWARD_POLICIES, SocketForwardHandler
from core.socket_scaling import SCALE_POLICIES
from core.socket_reader import READER_POLICIES
logger = logging.getLogger('Socket')

# socket_policies
class POLICIES(Enum):
    NONE = 0

    FORWARD = 1
    SCALE = 2
    READER = 3

    LAST = 3
    INVALID = 16


DEFAULT_POLICIES = {
    POLICIES.FORWARD: FORWARD_POLICIES['File'],
    POLICIES.SCALE: SCALE_POLICIES['LeastConnections'],
    POLICIES.READER: READER_POLICIES['Generic']
}

# Class for setting up socket for accepting client requests.
class SpinachSocket:
    __meta = {}
    __terminated = False
    # TODO: Move 'routes' to json/toml/yaml type 'default_routes' file
    def __init__(self, addr, routes=['route001', 'route002', 'route003'], policies=DEFAULT_POLICIES):
        self.__routes = routes
        self.__policies = policies

        # setup_meta
        self.__meta = self.__policies[POLICIES.SCALE](self.__routes).update()

        __balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        __balancer_socket.bind(addr)
        #__balancer_socket.listen()
        #__balancer_socket.setblocking(False)
        __balancer_socket.listen(1)

        self.__balancer_socket = __balancer_socket

        self.__threader = ThreadHandler()

    def __handle_conn(self, conn):
        logger.debug(conn)
        # generate_reader
        reader = self.__policies[POLICIES.READER](conn)
        (content, content_valid) = reader.handle()
        if (content_valid):
            logger.debug("\nContent: %s", content.strip())
            
            # socket_generators
            # generate_scaler
            scale_policy = self.__policies[POLICIES.SCALE]
            scaler = scale_policy(self.__routes)
            self.__meta = scaler.update(self.__meta)
            route = scaler.route()

            # generate_forwarder
            forward_policy = self.__policies[POLICIES.FORWARD]
            forwarder = SocketForwardHandler(forward_policy)
            forwarder.forward(route, content)

            logger.info("Rerouting to destination: %s", route)
        else:
            logger.warning("Wrong chunks length received: %s", content)
        conn.close()

    def persist(self):
        while(not self.__terminated):
            try:
                conn, addr = self.__balancer_socket.accept()
                logger.info('Accepted connection from client address %s:%i', addr[0], addr[1])
                self.__threader.submit(self.__handle_conn, conn)
            except socket.timeout:
                logger.info('Balancer timed out! Recalculating performance metrics ...\n')

    def terminate(self):
        self.__threader.terminate()
        self.__terminated = True
        