import argparse
import signal
import logging

#from core.policies import *
from core.system import signal_handler
from core.socket import SocketBalancer

#def init(addr, policy_class):
def init(addr):
    # Configuring logger
    logging.basicConfig(level=logging.WARNING,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S')
    logger = logging.getLogger('Core')
    
    # Register our signal handler for shutting down.
    logger.info('Binding kill signal handler')
    signal.signal(signal.SIGINT, signal_handler)

    # Set up socket for accepting client requests.
    logger.info('Initializing socket with '+addr[0]+':'+str(addr[1]))
    balancer_socket = SocketBalancer(addr)

    # Keep the balancer running forever.
    logger.info('Running Metric Load Balancer')
    while(1):
        balancer_socket.persist()

# Our main function.
def main():
    parser = argparse.ArgumentParser(description='Metric Load Balancer')
    #parser.add_argument('-a', dest='policy', choices=POLICIES)
    parser.add_argument('-i', dest='ip', type=str, help='load balancer ip', default='127.0.0.1')
    parser.add_argument('-p', dest='port', type=int, help='load balancer port', default=5000)
    args = parser.parse_args()
    
    #init(('127.0.0.1', args.port), POLICIES[args.policy])
    init((args.ip, args.port))

if __name__ == '__main__':
    main()