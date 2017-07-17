"""
Egardia / Woonveilig server that passes along alarms
"""
import socket
import argparse
import sys
import logging
import homeassistant.remote as remote

_LOGGER = logging.getLogger(__name__)


class EgardiaServer(object):
    """
    Egardia server passing along alarms
    """
    def __init__(self, port, hasshost, password):
        self._port = port
        self._hasshost = hasshost
        self._password = password
        self._api = remote.API(self._hasshost, self._password)
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            listen_socket.bind(('', port))
            listen_socket.listen(1)
        except:
            print("Permission error, make sure to run this as root or " +
                  "in sudo mode")
            sys.exit(2)
        _LOGGER.info("EgardiaServer listening on port "+str(port))
        self._status = ""
        while True:
            client_connection, client_address = listen_socket.accept()
            request = client_connection.recv(1024)

            http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""
            requestdecoded = request.decode('utf8')
            if requestdecoded.startswith("["):
                newstatus = requestdecoded[requestdecoded.index(' ')+1:]
                newstatus = newstatus[:len(newstatus)-1]
                if newstatus != self._status:
                    self._status = newstatus
                    payload = {"status": self._status}
                    try:
                        remote.fire_event(self._api,
                                          'egardia_system_status',
                                          data=payload)
                    except:
                        raise

            client_connection.sendall(http_response.encode('utf8'))
            client_connection.close()


def main(argv):
    parser = argparse.ArgumentParser(description='Run the EgardiaServer')
    parser.add_argument('-port', help='the port number to run the server ' +
                        'on (defaults to 85)', default='85')
    parser.add_argument('-host', help='the host of the Home Assistant ' +
                        'server (defaults to localhost)',
                        default='127.0.0.1')
    parser.add_argument('-password', help='the password for Home Assistant ' +
                        '(default none)', default='')
    args = parser.parse_args()
    port = args.port
    host = args.host
    password = args.password
    EgardiaServer(int(port), host, password)

if __name__ == "__main__":
    main(sys.argv[1:])
