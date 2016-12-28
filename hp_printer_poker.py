"""
A script to try to keep an HP printer from going to sleep
"""

import logging
import socket
import time
import traceback


#-------------------------------------------------------------------------------
# CONFIGURATION
#-------------------------------------------------------------------------------
IP_ADDRESS = '192.168.10.100'
PORTS = [80, 443, 515, 631, 8080, 8291]
CONNECTION_TIMEOUT_SECONDS = 3
CONNECTION_DURATION_SECONDS = 3
INTERVAL_SECONDS = 5


#-------------------------------------------------------------------------------
# LOGGING
#-------------------------------------------------------------------------------
LOGGER = logging.getLogger('hp_printer_poker')
LOGGER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(CONSOLE_HANDLER)


#-------------------------------------------------------------------------------
# HELPERS
#-------------------------------------------------------------------------------
def _connect(port):
    """
    Connect to the printer and return a socket
    """
    LOGGER.debug('connecting to %s:%d', IP_ADDRESS, port)
    return socket.create_connection((IP_ADDRESS, port), CONNECTION_TIMEOUT_SECONDS)


def _poke(sock):
    """
    Send something and keep a connection with the printer
    """
    LOGGER.debug('poking printer')
    sock.sendall('stay awake'.encode('utf-8'))
    time.sleep(CONNECTION_DURATION_SECONDS)


def _disconnect(sock):
    """
    Close the connection to the printer
    """
    sock.close()


def _sleep():
    """
    Sleeps for the configured interval
    """
    LOGGER.info('sleeping for %d seconds', INTERVAL_SECONDS)
    time.sleep(INTERVAL_SECONDS)


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
            try:
                sock = _connect(port)
                _poke(sock)
                _disconnect(sock)
            except Exception:
                LOGGER.warning('exception poking printer on %s:%d', IP_ADDRESS, port)
                traceback.print_exc()

            _sleep()


if __name__ == '__main__':
    main()
