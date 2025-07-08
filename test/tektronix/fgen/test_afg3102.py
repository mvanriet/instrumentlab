
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join( os.path.dirname(__file__), '../..')))


def cmd_line(txt:str):
    with afg3102._link as lnk:
        if txt.endswith('?'):
            print( str(lnk.query(txt)) )
        else:
            lnk.write(txt)

import happyscript
from instrumentlab.tektronix import AFG3102 

mngr = happyscript.ScriptManager()
mngr.on_cmd_line = cmd_line

mngr.add_scripts("scripts" )

afg3102 = AFG3102("fgen", pyvisa="TCPIP::172.20.11.60::INSTR")
mngr.add_objects(fgen = afg3102)



mngr.run()

afg3102.link.close()
