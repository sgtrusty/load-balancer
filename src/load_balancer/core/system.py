import sys
import signal
import logging

from core.balancer import SpinachBalancer

balancer_socket = None

# TODO: vertical scaling
# TODO: multithreading:
    # TODO: object pooling for outgoing queries (i.e core.forward > FileManager > write)
    # TODO: _selector_outgoing can be scaled up with pool (for outgoing)

# Signal handler for graceful exiting.
def signal_handler(sig, frame):
    print('Interrupt received, shutting down ...')
    sys.exit(0)

#def init(addr, policy_class):
def init(addr):
    global balancer_socket
    # Configuring logger
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S')
    logger = logging.getLogger('Core')
    
    # Register our signal handler for shutting down.
    logger.info('Binding kill signal handler')
    signal.signal(signal.SIGINT, signal_handler)

    # Set up socket for accepting client requests.
    logger.info('Running Spinach Socket on '+addr[0]+':'+str(addr[1]))
    balancer_socket = SpinachBalancer(addr)
    balancer_socket.persist()