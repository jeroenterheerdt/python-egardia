"""
Egardia / Woonveilig server that passes along alarms
"""
import socket
import argparse
import sys
import logging
import datetime
import homeassistant.remote as remote
import time

_LOGGER = logging.getLogger(__name__)


class EgardiaServer(object):
    """
    Egardia server passing along alarms
    """
    def __init__(self, port, hasshost, password, haport, ssl, retrycount, waittime):
        self._port = port
        self._hasshost = hasshost
        self._password = password
        self._haport = haport
        self._ssl = ssl
        self._retrycount = retrycount
        self._waittime = waittime
        msg = "Sleeping to give Home Assistant a moment to start"
        _LOGGER.info(msg)
        print(msg)
        time.sleep(waittime)
        try:
            validationresult = "init"
            numretries = 0
            while validationresult != "ok" and numretries <= self._retrycount:
                self._api = remote.API(self._hasshost, self._password,
                                       self._haport,self._ssl)
                validationresult = str(remote.validate_api(self._api))
                numretries = numretries+1
                if validationresult != "ok":
                   msg = "Connecting to Home Assistant failed, "
                   msg = msg + "retrying..."
                   _LOGGER.info(msg)
                   print(msg)
                   time.sleep(5)
            if validationresult != "ok":
               msg = "Error connection to Home Assistant: "
               msg = msg + validationresult
               _LOGGER.error(msg)
               print(msg)
               sys.exit(2)
            else:
               msg = "Succesfully connected to Home Assistant"
               print(msg)
               _LOGGER.info(msg)
        except:
            e = sys.exc_info()[0]
            msg = "Error connecting to Home Assistant: "
            msg = msg + e+", please check settings."
            print(msg)
            _LOGGER.error(msg)
            sys.exit(2)
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            listen_socket.bind(('', self._port))
            listen_socket.listen(1)
        except:
            msg = "Permission error, make sure to run "
            msg = msg + "this as root or in sudo mode"
            print(msg)
            _LOGGER.error(msg)
            sys.exit(2)
        msg = "EgardiaServer listening on port "+str(port)
        _LOGGER.info(msg)
        print(msg)
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
                msg = "["+str(datetime.datetime.now())+"] Received new "
                msg = msg + "statuscode from alarm system: "+newstatus
                _LOGGER.info(msg)
                print(msg)
                if newstatus != self._status:
                    self._status = newstatus
                    payload = {"status": self._status}
                    try:
                        remote.fire_event(self._api,
                                          'egardia_system_status',
                                          data=payload)
                        msg = "egardia_system_status event fired with payload: "
                        msg = msg + str(payload)
                        _LOGGER.info(msg)
                        print(msg)
                    except:
                        e = sys.exc_info()[0]
                        msg = "Could not fire event, is your "
                        msg = msg +"HASS server running?"
                        _LOGGER.error(msg)
                        print(msg)
                        _LOGGER.error(e)
                        print(e)
            client_connection.sendall(http_response.encode('utf8'))
            client_connection.close()


def main(argv):
    parser = argparse.ArgumentParser(description='Run the EgardiaServer')
    parser.add_argument('-port', help='the port number to run the server ' +
                        'on (defaults to 52010)', default='52010')
    parser.add_argument('-host', help='the host of the Home Assistant ' +
                        'server (defaults to localhost)',
                        default='127.0.0.1')
    parser.add_argument('-password', help='the password for Home Assistant ' +
                        '(default none)', default='')
    parser.add_argument('-haport', help='the port number for the Home '+
                        'Assistant server (defaults to 8123)',
                        default='8123')
    parser.add_argument('-ssl', help='connect to Home Assistant through '+
                        'a secure channel (defaults to False)',
                        default='False')
    parser.add_argument('-numretry', help='maximum number of retries '+
                        'connecting to Home Assistant (defaults to 10)',
                        default='10')
    parser.add_argument('-waittime',help='number of seconds to wait '+
                        'before connection to Home Assistant for the '+
                        'first time to give Home Assistant time to '+
                        'start (defaults to 120)',
                        default='120')
    args = parser.parse_args()
    port = args.port
    host = args.host
    password = args.password
    haport = args.haport
    ssl = args.ssl
    retrycount = args.numretry
    waittime = args.waittime
    EgardiaServer(int(port), host, password, int(haport), bool(ssl),
                  int(retrycount),int(waittime))

if __name__ == "__main__":
    main(sys.argv[1:])
