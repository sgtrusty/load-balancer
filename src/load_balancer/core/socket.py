import socket
import logging

from core.socket_reader import SocketReader
from core.socket_forward import SocketForwardHandler, FORWARD_POLICIES
logger = logging.getLogger('Socket')

# Define a constant timeout in seconds for the balancer to redo its performance calculations.
BALANCER_TIMEOUT = 120

# Class for setting up socket for accepting client requests.
class SocketBalancer:
    def __init__(self, addr, forward_policy=FORWARD_POLICIES['File']):
        balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        balancer_socket.bind(addr)
        #balancer_socket.listen()
        #balancer_socket.setblocking(False)
        balancer_socket.listen(1)
        #balancer_socket.settimeout(BALANCER_TIMEOUT)
        self.balancer_socket = balancer_socket
        self.reader = SocketReader()
        self.forwarder = SocketForwardHandler(forward_policy)

    def balance_load(self, selected_route, content):
        logger.debug("\nDestination: %s\nContent: %s", selected_route, content.strip())
        self.forwarder.forward(selected_route, content)

    def persist(self):
        try:
            logger.info('\n-- Waiting for incoming client connection --\n')
            conn, addr = self.balancer_socket.accept()
            logger.info('Accepted connection from client address: %s:%i', addr[0], addr[1])

            selected_route = "NONE"

            logger.debug(conn)
            (content, content_valid) = self.reader.handle(conn)
            if (content_valid):
                self.balance_load(selected_route, content)

                del content
                del content_valid
            else:
                logger.warning("Wrong chunks length received: %s", content)
            
            conn.close()
        except socket.timeout:
            logger.info('Balancer timed out! Recalculating performance metrics ...\n')