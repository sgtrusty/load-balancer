import logging
import selectors
import json

from core.forward import ForwardHandler
from core.scaling import ScalingHandler
from core.reader import ReadingHandler
from core.policies import POLICIES

logger = logging.getLogger('Mapper')

class SocketMapper:
    sock_inc = None
    sock_out = None

    def __init__(self, policies, routes, connections):
        # self.__selector = selector
        self.__policies = policies
        self.__routes = routes
        self.__connections = connections
        
        scale_policy = self.__policies[POLICIES.SCALE]
        scaler = ScalingHandler(scale_policy, self.__routes)
        self.__meta = scaler.update()

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
            #self.__selector.register(forwarder.getSocket(), selectors.EVENT_READ, read_upstream)
        return forwarder

    def add(self, client_sock):
        client_sock.setblocking(False)
        # self.__selector.register(client_sock, selectors.EVENT_READ, self.read_client)
        upstream_sock = self.create_upstream()
        self.sock_inc = client_sock
        self.sock_out = upstream_sock
        self.__connections.get()
        self.read_client(client_sock, None)

    def delete(self):
        logger.debug("Disposing connection...")
        # self.__selector.unregister(self.sock_inc)
        self.sock_inc.close()
        # self.__selector.unregister(self.sock_out)
        # self.sock_out.close()
        self.__connections.put(True)

    def read_client(self, conn, mask):
        # generate_reader
        logger.debug(conn)
        reader_policy = self.__policies[POLICIES.READER]
        reader = ReadingHandler(reader_policy, conn)
        (content, content_valid) = reader.handle()
        if (content_valid):
            logger.debug("Receiving content:\n%s", content.strip())
            upstream = self.sock_out
            response = upstream.deliver(content)
            # TODO: Querying the metrics is not part of this test!
            # if(upstream.hasResponse):
                # conn.send(json.dumps(response).encode('utf-8'))
        else:
            logger.warning("Wrong chunks length received: %s", content)
        self.delete()

    def read_upstream(self, conn, mask):
        # TODO: Querying the metrics is not part of this test!
        # if len(data) == 0: # No messages in socket, we can close down the socket
        #     self.delete(conn)
        # else:
        #     self.sock_inc.send(data)
        pass