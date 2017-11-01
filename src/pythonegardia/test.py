import egardiadevice
#valid values for YOURVERSION: GATE-01, GATE-02
e = egardiadevice.EgardiaDevice("YOURIP",80,"YOURUSERNAME","YOURPASSWORD","","YOURVERSION")
print(e.getstate())
print(e._sensors)

