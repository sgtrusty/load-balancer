import logging
import selectors
import json

from core.forward import ForwardHandler
from core.scaling import ScalingHandler
from core.reader import ReadingHandler
from core.policies import POLICIES

logger = logging.getLogger('Mapper')

class SocketMapper:
    def __init__(self, policies, routes, selector):
        self.__selector = selector
        self.__policies = policies
        self.__routes = routes
        
        scale_policy = self.__policies[POLICIES.SCALE]
        scaler = ScalingHandler(scale_policy, self.__routes)
        self.__meta = scaler.update()
        
        self.map = {}

    def create_upstream(self):
        scale_policy = self.__policies[POLICIES.SCALE]
        scaler = ScalingHandler(scale_policy, self.__routes)
        self.__meta = scaler.update(self.__meta)
        route = scaler.route()
        logger.debug("Rerouting to destination: %s", route)

        # generate_forwarder
        forward_policy = self.__policies[POLICIES.FORWARD]
        forwarder = ForwardHandler(forward_policy, route)
        # TODO: Querying the metrics is not part of this test!
        #if(forwarder.hasSocket()):
            #.register(forwarder.getSocket(), selectors.EVENT_READ, read_upstream)
        return forwarder

    def add(self, client_sock):
        client_sock.setblocking(False)
        self.__selector.register(client_sock, selectors.EVENT_READ, self.read_client)
        upstream_sock = self.create_upstream()
        self.map[client_sock] = upstream_sock

    def delete(self, sock):
        logger.debug("Disposing connection...")
        self.__selector.unregister(sock)
        sock.close()
        if sock in self.map:
            self.map.pop(sock)
    
    def get_upstream_sock(self, sock):
        return self.map.get(sock)

    def get_all_socks(self):
        """ Flatten all sockets into a list"""
        return list(sum(self.map.items(), ()))

    def get_sock(self, sock):
        for client, upstream in self.map.items():
            if upstream == sock:
                return client
            if client == sock:
                return upstream
        return None

    def read_client(self, conn, mask):
        # generate_reader
        logger.debug(conn)
        reader_policy = self.__policies[POLICIES.READER]
        reader = ReadingHandler(reader_policy, conn)
        (content, content_valid) = reader.handle()
        if (content_valid):
            logger.debug("Receiving content:\n%s", content.strip())
            upstream = self.get_upstream_sock(conn)
            response = upstream.deliver(content)
            # TODO: Querying the metrics is not part of this test!
            if(upstream.hasResponse):
                conn.send(json.dumps(response).encode('utf-8'))
        else:
            logger.warning("Wrong chunks length received: %s", content)
        self.delete(conn)

    def read_upstream(self, conn, mask):
        # TODO: Querying the metrics is not part of this test!
        # if len(data) == 0: # No messages in socket, we can close down the socket
        #     self.delete(conn)
        # else:
        #     self.get_sock(conn).send(data)
        pass