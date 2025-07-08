
import sys, os
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(__file__), '../..')))

import happyscript
import instrumentlab.agilent as agilent

mngr = happyscript.ScriptManager()

mngr.add_scripts("agilent_inf" )

sco = agilent.DSO54830B("scope", pyvisa="TCPIP::172.20.11.144::5025::SOCKET")
mngr.add_objects(sco = sco, ch1 = sco.channels[0])

mngr.run()

sco._link.close()
