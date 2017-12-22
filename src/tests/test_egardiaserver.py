"""Make a test client to test the EgardiaServer."""
import argparse
import socket


def connect(host, port, data):
    """Connect to EgardiaServer."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((host, port))
        sock.sendall(data.encode('utf-8'))

        # Receive data from the server and shut down
        received = sock.recv(1024)
        received = received.decode('utf8')
        return received
    except OSError:
        print("Error on socket: ", host, port)
    finally:
        sock.close()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run the test client")
    parser.add_argument(
        '-P', '--port', default='52010', type=int,
        help="The port number to connect on (defaults to 52010)")
    args = parser.parse_args()
    port = args.port
    host = 'localhost'
    data = "[status: armed]"
    received = connect(host, port, data)
    print("Sent:     {}".format(data))
    print("Received: {}".format(received))


if __name__ == '__main__':
    main()
