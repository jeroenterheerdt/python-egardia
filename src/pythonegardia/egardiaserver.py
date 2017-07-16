"""
Egardia / Woonveilig server that passes along alarms
"""
import socket
import argparse
import sys

class EgardiaServer(object):
    """
    Egardia server passing along alarms
    """
    def __init__(self, port):
        self._port = port
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            listen_socket.bind(('', port))
            listen_socket.listen(1)
        except PermissionError as e:
            print("Permission error, make sure to run this as root or in sudo mode")
            sys.exit(2)
        print("EgardiaServer listening on port "+str(port))
        self._status = ""
        while True:
            client_connection, client_address = listen_socket.accept()
            request = client_connection.recv(1024)
            
            http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""
            #PARSE THE REQUEST
            requestdecoded = request.decode('utf8')
            #print(requestdecoded)
            if requestdecoded.startswith("GET"):
                #Return the current status
                http_response = """\
HTTP/1.1 200 OK

"""+self._status
            elif requestdecoded.startswith("["):
                #Handle Egardia status and store it for future retrieval
                newstatus = requestdecoded[requestdecoded.index(' ')+1:]
                newstatus = newstatus[:len(newstatus)-1]
                if newstatus != self._status:
                    self._status = newstatus
	           
            #print(http_response)
            client_connection.sendall(http_response.encode('utf8'))
            client_connection.close()

def main(argv):
    parser = argparse.ArgumentParser(description = 'Run the EgardiaServer')
    parser.add_argument('-port',help='the port number to run the server on (defaults to 85)', default='85')
    args = parser.parse_args()
    port = args.port
    es = EgardiaServer(int(port))

if __name__=="__main__":
    main(sys.argv[1:])
