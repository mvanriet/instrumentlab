
import sys, os
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(__file__), '../..')))


def cmd_line(txt:str):
    with ea.link as lnk:
        if txt.endswith('?'):
            print( str(lnk.query(txt)) )
        else:
            lnk.write(txt)



import happyscript
from instrumentlab.ea import PSI9750_06DT_Simple

mngr = happyscript.ScriptManager()
mngr.on_cmd_line = cmd_line

mngr.add_scripts("scripts" )

ea = PSI9750_06DT_Simple("ea", pyvisa="ASRL248::INSTR")
mngr.add_objects(ea = ea)

mngr.run()

ea.link.close()
