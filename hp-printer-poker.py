import socket
import sys
import time


IP_ADDRESS = '192.168.10.113'
PORTS = [80, 443, 515, 631, 8080, 8291, 9100]
CONNECTION_DURATION_SECONDS = 3
INTERVAL_SECONDS = 5


def main(argv):
    while True:
        print('poking printer')

        for port in PORTS:
            # create a socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
            # connect
            print('connecting to {}:{}'.format(IP_ADDRESS, port))
            sock.connect((IP_ADDRESS, port))

            try:
                # send something
                sock.sendall('stay awake'.encode('utf-8'))
                
                # stay connected
                time.sleep(CONNECTION_DURATION_SECONDS)
            finally:
                # response not needed; close the socket
                sock.close()

        print('sleeping for {} seconds'.format(INTERVAL_SECONDS))
        time.sleep(INTERVAL_SECONDS)


if __name__ == '__main__':
    main(sys.argv[1:])
