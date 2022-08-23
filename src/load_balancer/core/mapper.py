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

import logging
import selectors
import json

from socket import SHUT_RDWR

from core.forward import ForwardHandler
from core.scaling import ScalingHandler
from core.reader import ReadingHandler
from core.policies import POLICIES

logger = logging.getLogger('Mapper')

class SocketMapper:
    def __init__(self, policies, routes, reader, writer):
        self.__policies = policies
        self.__routes = routes
        self.__reader = reader
        self.__writer = writer
        
        scale_policy = self.__policies[POLICIES.SCALE]
        scaler = ScalingHandler(scale_policy, self.__routes)
        self.__meta = scaler.update()
        
        upstream_sock = self.create_upstream()
        self.sock_out = upstream_sock

    def create_upstream(self):
        scale_policy = self.__policies[POLICIES.SCALE]
        scaler = ScalingHandler(scale_policy, self.__routes)
        self.__meta = scaler.update(self.__meta)
        route = scaler.route()
        logger.debug("Rerouting to destination: %s", route)

        # generate_forwarder
        forward_policy = self.__policies[POLICIES.FORWARD]
        forwarder = ForwardHandler(forward_policy, route)
        # NOTE: Querying the metrics is not part of this test!
        #if(forwarder.hasSocket()):
            #self.__selector.register(forwarder.getSocket(), selectors.EVENT_READ, read_upstream)
        return forwarder

    def delete(self):
        logger.debug("Disposing connection...")
        self.__writer.close()

    async def read_client(self):
        # generate_reader
        reader_policy = self.__policies[POLICIES.READER]
        reader = ReadingHandler(reader_policy, self.__reader)
        (content, content_valid) = await reader.handle()
        if (content_valid):
            logger.debug("Receiving content:\n%s", content.strip())
            response = self.sock_out.deliver(content)
            # NOTE: Querying the metrics is not part of this test!
            # if (self.sock_out.hasResponse):
                # self.__writer.send(json.dumps(response).encode('utf-8'))
        else:
            logger.warning("Wrong chunks length received: %s", content)
        self.delete()

    def read_upstream(self, reader, mask):
        # NOTE: Querying the metrics is not part of this test!
        # if len(data) == 0: # No messages in socket, we can close down the socket
        #     return
        # else:
        #     self.__writer.send(data)
        pass