
import sys, os
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(__file__), '../..')))


import instrumentlab.agilent as agilent


sco = agilent.DSO54830B("scope", pyvisa="TCPIP::172.20.11.144::5025::SOCKET")

with sco._link as lnk:
    print(lnk)

print(sco.get_id())

sco._link.close()

