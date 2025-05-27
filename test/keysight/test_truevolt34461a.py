
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join( os.path.dirname(__file__), '../..')))


def cmd_line(txt:str):
    with sig._link as lnk:
        if txt.endswith('?'):
            print( str(lnk.query(txt)) )
        else:
            lnk.write(txt)

import happyscript
from instrumentlab.keysight import Truevolt34461A

mngr = happyscript.ScriptManager()
mngr.on_cmd_line = cmd_line

mngr.add_scripts("scripts" )

sig = Truevolt34461A("sig", pyvisa="TCPIP::172.20.10.19::INSTR")
#sig = Truevolt34461A("sig", pyvisa="USB::0x2A8D::0x1401::MY53221797::INSTR")
mngr.add_objects(sig = sig)



mngr.run()

sig.link.close()
