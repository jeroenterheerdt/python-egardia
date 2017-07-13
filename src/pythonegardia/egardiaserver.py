"""
Egardia / Woonveilig server that passes along alarms
"""
import socket
import logging

_LOGGER = logging.getLogger(__name__)

class EgardiaServer(object):
    """
    Egardia server passing along alarms
    """
    def __init__(self, port):
        self._port = port
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(('', port))
        listen_socket.listen(1)
        _LOGGER.info("EgardiaServer listening on port "+str(port))
        self._status = ""
        while True:
            client_connection, client_address = listen_socket.accept()
            request = client_connection.recv(1024)
            http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""
            client_connection.sendall(http_response.encode('utf8'))
            client_connection.close()
    
            #PARSE THE REQUEST
            requestdecoded = request.decode('utf8')
            if requestdecoded.startswith("["):
                newstatus = requestdecoded[requestdecoded.index(' ')+1:]
                newstatus = newstatus[:len(newstatus)-1]
                if newstatus != self._status:
                    self._status = newstatus

    def state(self):
        """Return _status"""
        return self._status

