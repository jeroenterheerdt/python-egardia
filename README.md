# python-egardia
Python library to interface with Egardia / Woonveilig alarm. Tested with **WV-1716**, **GATE-01**, **GATE-02** and **GATE-03** version of Egardia / Woonveilig. Other versions might work, but unsure. Includes components to work with Home Assistant (see below) as well as generic interfaces.

Egardiadevice is the representation of the alarm control panel and the Egardiaserver can be used to handle alarm status changes including triggering. Test files are included for both device and server. 

```bash
usage: egardiaserver.py [-h] [-P PORT]

Run the EgardiaServer

optional arguments:
  -h, --help            show this help message and exit
  -P PORT, --port PORT  the port number to run the server on (defaults to 52010)
```
