import sys

# Signal handler for graceful exiting.
def signal_handler(sig, frame):
    print('Interrupt received, shutting down ...')
    sys.exit(0)