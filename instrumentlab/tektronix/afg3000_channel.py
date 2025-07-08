#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0


from ..base.fgen.fgen_channel import FgenChannel
from ..base.fgen.fgen_constants import FgenConstants as FGC
from ..base.attribute import Attribute
from .afg3000_channel_voltage import Afg3000ChannelVoltage

class Afg3000Channel(FgenChannel):
    
    def __init__(self, inst, index):
        super().__init__(inst, index)

        self.voltage = Afg3000ChannelVoltage(inst, index)

    @Attribute
    def enabled(self):
        return super().enabled
        
    @enabled.setter
    def enabled(self, value):
        state = "ON" if value else "OFF"
        with self._link as lnk:
            lnk.write(f"OUTP{self.index}:STAT {state}" )

    @Attribute
    def frequency(self):
        raise NotImplementedError()
        
    @frequency.setter
    def frequency(self, value):
        with self._link as lnk:
            lnk.write(f"SOUR{self.index}:FREQ:FIX {value:d}" )
