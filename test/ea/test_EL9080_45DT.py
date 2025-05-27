
import sys, os
# sys.path.append( os.path.abspath(os.path.join( os.path.dirname(__file__), '../..')))

for path in sys.path:
    print(path)

import happyscript
from instrumentlab.ea import EL9080_45DT

def cmd_line(txt:str):
    with dcload.link as lnk:
        if txt.endswith('?'):
            print( str(lnk.query(txt)) )
        else:
            lnk.write(txt)

mngr = happyscript.ScriptManager()
mngr.on_cmd_line = cmd_line

mngr.add_scripts("dcload" )

dcload = EL9080_45DT("dcload", pyvisa="ASRL51::INSTR")
mngr.add_objects(dcload)

mngr.run()

dcload.link.close()
