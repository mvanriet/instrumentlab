#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

from ..base.dmm.dmm_setup import DmmSetup
from ..base.dmm import BasicDmm, DmmConstants as DMC
from ..base.attribute import Attribute

class Truevolt344xx_Setup(DmmSetup):
    ''' 

    '''

    def __init__(self, parent, **kwargs):
        super().__init__(parent)

    @Attribute
    def mode(self) -> DMC.mode:
        """Get the mode of the DMM."""
        with self.link as lnk:
            cmd = lnk.query("CONF?").strip('"\r\n')
            if cmd.startswith("VOLT:AC"):
                return DMC.mode.VOLT_AC
            elif cmd.startswith("VOLT"):
                return DMC.mode.VOLT_DC
            elif cmd.startswith("CURR:AC"):
                return DMC.mode.CURR_AC
            elif cmd.startswith("CURR"):
                return DMC.mode.CURR_DC
            else:
                raise ValueError(f"Unknown mode command : '{cmd}'")

    @mode.setter
    def mode(self, value: DMC.mode):
        """Set the mode of the DMM.
        """
        if isinstance(value, str):
            try:
                value = DMC.mode[value.strip().upper()]
            except KeyError:
                raise ValueError(f"Invalid string for mode : '{value}'")

        match value:
            case DMC.mode.VOLT_DC:
                cmd = "CONF:VOLT:DC"
            case DMC.mode.VOLT_AC:
                cmd = "CONF:VOLT:AC"
            case DMC.mode.CURR_DC:
                cmd = "CONF:CURR:DC"
            case DMC.mode.CURR_AC:
                cmd = "CONF:CURR:AC"
            case _:
                raise ValueError(f"Invalid value for mode : '{value}'")
            
        with self.link as lnk:
            lnk.write(cmd)        
