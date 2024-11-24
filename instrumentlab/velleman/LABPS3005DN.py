#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

from ..base.psu.simple_psu import SimplePsu
from ..korad.korad_slow_serial import KoradSlowSerial

class LABPS3005DN(SimplePsu):
    ''' This is based on the interface for the Korad KAxxxx power supplies.
        Unfortunately, the commands are slightly different.
        The handling of the serial data seems to be the same, so the Korad serial interface can be used

        Note that the LABPS3005D is identical to the Korad KA5003, but the 'DN' is not.
    '''

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.link = KoradSlowSerial(self, baudrate=9600)
    
    def _set_enabled(self, value:bool):
        with self.link as lnk:
            lnk.write("OUTPUT1\\n" if value else "OUTPUT0\\n")

    def _get_enabled(self) -> bool:
        raise NotImplementedError()

    def _set_current(self, value:float):
        value = max(0,min(value,5))

        with self.link as lnk:
            lnk.write(f"ISET1:{value:05.3f}\\n")

    def _get_current(self) -> float:
        with self.link as lnk:
            return lnk.query_float("ISET1?\\n")

    def _read_current(self) -> float:
        with self.link as lnk:
            return lnk.query_float("IOUT1?\\n")

    def _set_voltage(self, value:float):
        value = max(0,min(value,30))
            
        with self.link as lnk:
            lnk.write(f"VSET1:{value:05.2f}\\n")

    def _get_voltage(self) -> float:
        with self.link as lnk:
            return lnk.query_float("VSET1?\\n")

    def _read_voltage(self) -> float:
        with self.link as lnk:
            return lnk.query_float("VOUT1?\\n")
