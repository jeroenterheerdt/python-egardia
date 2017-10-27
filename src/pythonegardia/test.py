import egardiadevice
e = egardiadevice.EgardiaDevice("YOURIP",80,"YOURUSERNAME","YOURPASSWORD","")
print(e.getstate())
print(e._sensors)

