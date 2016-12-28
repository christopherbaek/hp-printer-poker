"""
A script to try to keep an HP printer from going to sleep
"""

import logging
import socket
import time


#-------------------------------------------------------------------------------
# CONFIGURATION
#-------------------------------------------------------------------------------
IP_ADDRESS = '192.168.10.110'
PORTS = [80, 443, 515, 631, 8080, 8291]
CONNECTION_DURATION_SECONDS = 3
INTERVAL_SECONDS = 5


#-------------------------------------------------------------------------------
# LOGGING
#-------------------------------------------------------------------------------
LOGGER = logging.getLogger('spam_application')
LOGGER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(CONSOLE_HANDLER)


#-------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------
def main():
    """
    MAIN
    """
    while True:
        LOGGER.info('poking printer')

        for port in PORTS:
            # create a socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # connect
            LOGGER.debug('connecting to %s:%d', IP_ADDRESS, port)
            sock.connect((IP_ADDRESS, port))

            try:
                # send something
                sock.sendall('stay awake'.encode('utf-8'))

                # stay connected
                time.sleep(CONNECTION_DURATION_SECONDS)
            finally:
                # response not needed; close the socket
                sock.close()

        LOGGER.info('sleeping for %d seconds', INTERVAL_SECONDS)
        time.sleep(INTERVAL_SECONDS)


if __name__ == '__main__':
    main()
