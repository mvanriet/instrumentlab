
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join( os.path.dirname(__file__), '../..')))


def cmd_line(txt:str):
    with sig._link as lnk:
        if txt.endswith('?'):
            print( str(lnk.query(txt)) )
        else:
            lnk.write(txt)

import happyscript
from instrumentlab.siglent import SDM3055

mngr = happyscript.ScriptManager()
mngr.on_cmd_line = cmd_line

mngr.add_scripts("scripts" )

# sig = SDM3055("sig", pyvisa="TCPIP::172.20.10.102::INSTR")
sig = SDM3055("sig", pyvisa="USB::0xF4EC::0x1206::SDM35GBC7R0495::INSTR")
mngr.add_objects(sig = sig)



mngr.run()

sig.link.close()
