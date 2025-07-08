#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0


from ..base.subsystem import SubSystem
from ..base.attribute import Attribute

class Afg3000ChannelVoltage(SubSystem):
    
    def __init__(self, inst, index):
        super().__init__(inst)
        self.index = index

    @Attribute
    def amplitude(self):
        raise NotImplementedError()
        
    @amplitude.setter
    def amplitude(self, value):
        voltage = f"{value:.4f}".rstrip('0').rstrip('.')

        with self.link as lnk:
            lnk.write(f"SOUR{self.index}:VOLT:LEV:IMM:AMPL {voltage}" )
