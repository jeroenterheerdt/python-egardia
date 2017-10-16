# python-egardia
Python library to interface with Egardia / Woonveilig alarm. Tested with GATE-01 version of Egardia / Woonveilig. Other versions might work, but unsure. Includes components to work with Home Assistant (see below) as well as generic interfaces.

```bash
usage: egardiaserver.py [-h] [-port PORT] [-host HOST] [-password PASSWORD]
                        [-haport HAPORT] [-ssl SSL] [-numretry NUMRETRY]
                        [-waittime WAITTIME]

Run the EgardiaServer

optional arguments:
  -h, --help          show this help message and exit
  -port PORT          the port number to run the server on (defaults to 52010)
  -host HOST          the host of the Home Assistant server (defaults to
                      localhost)
  -password PASSWORD  the password for Home Assistant (default none)
  -haport HAPORT      the port number for the Home Assistant server (defaults
                      to 8123)
  -ssl SSL            connect to Home Assistant through a secure channel
                      (defaults to False)
  -numretry NUMRETRY  maximum number of retries connecting to Home Assistant
                      (defaults to 10)
  -waittime WAITTIME  number of seconds to wait before connection to Home
                      Assistant for the first time to give Home Assistant time
                      to start (defaults to 120)
```
