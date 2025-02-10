#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

from ..base.psu.simple_psu import SimplePsu, SimplePsuReadout
from ..base.attribute import Attribute
from .korad_slow_serial import KoradSlowSerial

class KoradSimpleReadout(SimplePsuReadout):
    ''' Interface class to return actual voltage and current.
    '''
    def __init__(self, inst:'KoradSimplePSU'):
        super().__init__(inst)

    @Attribute
    def voltage(self):
        with self._inst.link as lnk:
            return lnk.query_float("VOUT1?")

    @Attribute
    def current(self):
        with self._inst.link as lnk:
            return lnk.query_float("IOUT1?") 
    

class KoradSimplePSU(SimplePsu):
    ''' Base class to derive instruments from with a given voltage/current range.
    '''

    def __init__(self, name, max_voltage, max_current, **kwargs):
        super().__init__(name, **kwargs)

        self.max_voltage = max_voltage
        self.max_current = max_current

        self.link = KoradSlowSerial(self)
        self.read = KoradSimpleReadout(self)

    @Attribute
    def enabled(self):
        return super().enabled                  # @TODO: implement getter
    
    @enabled.setter
    def enabled(self, value):
        with self.link as lnk:
            lnk.write("OUT1" if value else "OUT0")        

    @Attribute
    def current(self):
        with self.link as lnk:
            return lnk.query_float("ISET1?")
        
    @current.setter
    def current(self, value):
        value = max(0,min(value,self.max_current))

        with self.link as lnk:
            lnk.write(f"ISET1:{value:05.3f}")

    @Attribute
    def voltage(self):
        with self.link as lnk:
            return lnk.query_float("VSET1?")
        
    @voltage.setter
    def voltage(self, value):
        value = max(0,min(value,self.max_voltage))

        with self.link as lnk:
            lnk.write(f"VSET1:{value:05.3f}")


class KA3005P(KoradSimplePSU):

    def __init__(self, name, **kwargs):
        super().__init__(name, 30, 5, **kwargs)

class KA6003P(KoradSimplePSU):

    def __init__(self, name, **kwargs):
        super().__init__(name, 60, 3, **kwargs)

