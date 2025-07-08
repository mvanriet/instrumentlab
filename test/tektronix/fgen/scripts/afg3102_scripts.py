
from instrumentlab.base.dmm import DmmConstants as dmc
import time

def read(sig):
    ''' @public
    '''
    print(sig.read())
    
def reset(sig):
    ''' @public
    '''
    with sig._link as lnk:
        lnk.write("*RST")

def unlock(ea):
    ''' @public
    '''
    print("ERROR: Je moet gewoon op de blauwe knop drukken (shift+local)")
    ea.unlock()


# def configure(sig, gui):
#     ''' @public
#     '''
#     options = [e.name for e in dmc.mode]

#     result = gui.ask_choice("select multimeter mode ?", options )
#     if result:
#         sig.configure(dmc.mode[options[result]],0.1)

def set_mode_volt_dc(sig):
    ''' @public
    '''
    sig.setup.mode = dmc.mode.VOLT_DC

def set_mode_curr_dc(sig):
    ''' @public
    '''
    sig.setup.mode = dmc.mode.CURR_DC
