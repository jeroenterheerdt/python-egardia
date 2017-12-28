"""Test the EgardiaDevice class."""
import argparse
import egardiadevice as e

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run the test for EgardiaDevice")
    parser.add_argument(
        'host', type=str,
        help="The IP of Egardia system")
    parser.add_argument(
        'port', default=80, type=int,
        help="The portnumber of Egardia system (default 80)")
    parser.add_argument(
        'username', type=str,
        help="The username for Egardia system")
    parser.add_argument(
        'password', type=str,
        help="The password for Egardia system")
    parser.add_argument(
        'version', type=str,
        help="The version of Egardia system (GATE-01, GATE-02 or GATE-03)"
    )
    args = parser.parse_args()
    port = args.port
    host = args.host
    username = args.username
    password = args.password
    version = args.version
    eg = e.EgardiaDevice(host, port, username, password, "", version)
    print("getstate output ",eg.getstate())
    print("getsensors output ",eg.getsensors())

if __name__ == '__main__':
    main()
