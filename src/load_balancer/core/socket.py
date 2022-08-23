import socket
import logging
import select
import queue

from core.threading import ThreadHandler
from core.socket_reader import SocketReader
from core.socket_balancer import SocketBalancer
from core.socket_forward import FORWARD_POLICIES
from core.socket_scaling import SCALE_POLICIES
logger = logging.getLogger('Socket')

# Class for setting up socket for accepting client requests.
class SpinachSocket:
    __terminated = False
    def __init__(self, addr, routes=['route001', 'route002', 'route003'], forward_policy=FORWARD_POLICIES['File'], scale_policy=SCALE_POLICIES['Random']):
        __balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        __balancer_socket.bind(addr)
        #__balancer_socket.listen()
        #__balancer_socket.setblocking(False)
        __balancer_socket.listen(1)

        self.__balancer_socket = __balancer_socket
        self.__routes = routes
        self.__forward_policy = forward_policy
        self.__scale_policy = scale_policy

        self.__threader = ThreadHandler()

    def __handle_conn(self, conn):
        logger.debug(conn)
        reader = SocketReader(conn)
        (content, content_valid) = reader.handle()
        if (content_valid):
            logger.debug("\nContent: %s", content.strip())
            balancer = SocketBalancer(self.__routes, self.__scale_policy, self.__forward_policy, content)
            logger.info("Rerouting to destination: %s", balancer)

            del content
            del content_valid
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
        