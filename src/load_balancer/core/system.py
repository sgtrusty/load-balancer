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

import sys
import signal
import logging

from core.balancer import SpinachBalancer

balancer_socket = None

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
    logger.info('Running Spinach Socket on '+addr[0]+':'+str(addr[1]))
    balancer_socket = SpinachBalancer(addr)
    balancer_socket.persist()