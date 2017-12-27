"""Egardia / Woonveilig server that passes along alarms."""
import argparse
import logging
import socketserver
import sys
import threading

_LOGGER = logging.getLogger(__name__)

DEFAULT_RESPONSE = "HTTP/1.1 200 OK\n\nHello, World!"


class EgardiaServer(socketserver.TCPServer, threading.Thread):
    """Egardia server passing along alarms."""

    def __init__(self, host, port):
        """Prepare server."""
        threading.Thread.__init__(self)
        self._address = (host, port)
        self.callbacks = []
        socketserver.TCPServer.__init__(
            self, self._address, EgardiaServerHandler, bind_and_activate=False)
        self.status = ''

    def bind(self):
        """Bind and listen to address."""
        try:
            self.allow_reuse_address = True
            self.server_bind()
            self.server_activate()
        except OSError:
            self.server_close()
            _LOGGER.exception(
                "Can't bind to address %s", self._address)
            return False

        _LOGGER.info("Server listening on %s", self._address)
        return True

    def register_callback(self, func):
        """Store callback in list.

        The callback should accept a dict as argument. For each request from
        the alarm control panel, all callbacks will be called with a dict
        containing the new status of the alarm.
        """
        self.callbacks.append(func)

    def notify(self, data):
        """Call callbacks with event data."""
        try:
            for func in self.callbacks:
                _LOGGER.debug(
                    "Notify callback with data: %s", data)
                func(data)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Could not notify callback")

    def run(self):
        """Run the server."""
        _LOGGER.info('Starting server %s', self._address)
        self.serve_forever()

    def stop(self):
        """Stop the server."""
        _LOGGER.info('Stopping server %s', self._address)
        self.shutdown()


class EgardiaServerHandler(socketserver.BaseRequestHandler):
    """Egardia server handler passing along alarms."""

    def handle(self):
        """Handle messages to this server."""
        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024).strip()
        data = data.decode('utf8')
        if data.startswith('['):
            new_status = data[data.index(' ') + 1:]
            new_status = new_status[:-1]
            _LOGGER.debug(
                "Received new status code from alarm system: %s", new_status)
            if self.server.status != new_status:
                self.server.status = new_status
                # self.server is the socketserver
                self.server.notify({'status': new_status})
        self.request.sendall(DEFAULT_RESPONSE.encode('utf8'))


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run the EgardiaServer")
    parser.add_argument(
        '-P', '--port', default='52010', type=int,
        help="The port number to run the server on (defaults to 52010)")
    args = parser.parse_args()
    port = args.port
    host = ''
    server = EgardiaServer(host, port)
    bound = server.bind()
    if not bound:
        sys.exit(2)

    def handle_event(event):
        """Handle event."""
        print('event: ', event)

    server.register_callback(handle_event)
    server.start()
    return server


if __name__ == '__main__':
    SERVER = main()
    # SERVER.stop()
