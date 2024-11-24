#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

import numpy as np

from ...base.oscilloscope.oscilloscope_channel import OscilloscopeChannel
from ...base.oscilloscope.oscillocope_constants import OscilloscopeConstants as OCT

class InfiniiumChannel(OscilloscopeChannel):
    
    
    def __init__(self, inst, index):
        
        super().__init__(inst, index)

    @property
    def channel(self) -> int:
        return self._index+1

    def _get_enabled(self):
        raise NotImplementedError()
    
    def _set_enabled(self, visible:bool):
        with self._link as lnk:
            if visible:
                lnk.write("CHAN%d:DISP ON" % self.channel )
            else:
                lnk.write("CHAN%d:DISP OFF" % self.channel )        

    def _get_scale(self):
        raise NotImplementedError()
    
    def _set_scale(self, voltage:float):
        with self._link as lnk:
            lnk.write(":CHAN%d:SCAL %G" % (self.channel, voltage) )

    def _get_offset(self):
        raise NotImplementedError()
    
    def _set_offset(self, offset:float):
        with self._link as lnk:
            lnk.write(":CHAN%d:OFFS %G" % (self.channel, offset) )

    def _get_coupling(self):
        raise NotImplementedError()
    
    def _set_coupling(self, value):
        if value==OCT.coupling.AC:
            with self._link as lnk:
                lnk.write(":CHAN%d:PROB:COUP AC" % self.channel )
        elif value==OCT.coupling.DC:
            with self._link as lnk:
                lnk.write(":CHAN%d:PROB:COUP DC" % self.channel )
        else:
            raise ValueError(f"{value} is not valid for Infiniium channel coupling mode.")

    def _get_bandwidth(self):
        raise NotImplementedError()
    def _set_bandwidth(self, value:int):
        raise NotImplementedError()

    def _get_impedance(self):
        raise NotImplementedError()
    def _set_impedance(self, value:int):
        raise NotImplementedError()


