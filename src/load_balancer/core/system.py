import sys
import signal
import logging

from core.socket import SpinachSocket

balancer_socket = None

# TODO: vertical scaling
# TODO: select for deadlock/dead connections
# TODO: object pooling for i/o data (FileManager) and close connections asap

# Signal handler for graceful exiting.
def signal_handler(sig, frame):
    print('Interrupt received, shutting down ...')
    balancer_socket.terminate()
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
    logger.info('Initializing socket with '+addr[0]+':'+str(addr[1]))
    balancer_socket = SpinachSocket(addr)

    # Keep the balancer running forever.
    logger.info('Running Metric Load Balancer')
    balancer_socket.persist()