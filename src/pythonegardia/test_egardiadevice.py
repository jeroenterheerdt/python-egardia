#!/usr/bin/env/python
"""Test the EgardiaDevice class."""
import time
import sys
import argparse
import random
import egardiadevice as e

if sys.version_info<(3,0,0):
    sys.stderr.write("You need to run this using python version 3 (python3)")
    exit(1)

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
    print("Getting STATE")
    print("getstate output ",eg.getstate())
    print("------------")
    sensors = eg.getsensors()
    print("Getting SENSORS")
    print("getsensors output ",sensors)
    randomsensorID = random.choice(list(sensors.keys()))
    print("Selected random sensor: ",randomsensorID)
    print("getsensor(",randomsensorID,") output ",eg.getsensor(randomsensorID))
    print("------------")
    print("IMPORTANT: continuing passed this point will arm and disarm your alarm!")
    armOK = input("Press y to ARM your alarm ")
    if armOK.lower() == "y":
        eg.alarm_arm_away()
    else:
        sys.exit('User chose not to ARM the alarm')
    print("Sent arm command to alarm, waiting 10 seconds...")
    time.sleep(10)
    print("getstate output (should be ARM) ",eg.getstate())
    disarmOK = input("Press y to DISARM your alarm ")
    if disarmOK.lower() == "y":
        eg.alarm_disarm()
    else:
        sys.exit('User chose not to DISARM the alarm')
    print("Sent disarm command to alarm, waiting 10 seconds...")
    time.sleep(10)
    print("getstate output (should be DISARM) ",eg.getstate())
    homearmOK = input("Press y to HOME ARM your alarm ")
    if homearmOK.lower() == "y":
        eg.alarm_arm_home()
    else:
        sys.exit('User chose not to HOME ARM the alarm')
    print("Sent home arm command to alarm, waiting 10 seconds...")
    time.sleep(10)
    print("getstate output (should be HOME) ",eg.getstate())
    isarmOK = input("Press y to DISARM your alarm ")
    if disarmOK.lower() == "y":
        eg.alarm_disarm()
    else:
        sys.exit('User chose not to DISARM the alarm')
    print("Sent disarm command to alarm, waiting 10 seconds...")
    time.sleep(10)
    print("getstate output (should be DISARM) ",eg.getstate())
    print("Tests completed")
if __name__ == '__main__':
    main()
