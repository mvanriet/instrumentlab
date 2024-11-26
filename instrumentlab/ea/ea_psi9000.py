#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

from ..base.psu.simple_psu import SimplePsu

class PSI9750_06DT_Simple(SimplePsu):
    ''' Base class to derive instruments from with a given voltage/current range.
    '''

    def __init__(self, name, **kwargs):
        super().__init__(name, terminator="lf", **kwargs)

        from ..links import Visa
        self.link = Visa(self)

    def to_float(self, txt):
        parts = txt.split()
        if len(parts)==0:
            raise ValueError(f"Received unexpected reply '{txt}'")
        try:
            return float(parts[0])
        except:
            raise ValueError(f"Reply '{txt}' doesn't contain a number")

    def lock(self):
        with self.link as lnk:
            lnk.write("SYST:LOCK ON")

    def unlock(self):
        with self.link as lnk:
            lnk.write("SYST:LOCK OFF")

    def _set_enabled(self, value:bool):
        with self.link as lnk:
            lnk.write("OUTP 1" if value else "OUTP 0")

    def _get_enabled(self):
        with self.link as lnk:
            status = lnk.query("OUTP?")
            return True if status=="ON" else False

    def _set_current(self, value:float):
        with self.link as lnk:
            lnk.write(f"CURR {value:0.3f}")

    def _get_current(self) -> float:
        with self.link as lnk:
            return self.to_float(lnk.query("CURR?"))

    def _read_current(self) -> float:
        with self.link as lnk:
            return self.to_float(lnk.query("MEAS:CURRENT?"))

    def _set_voltage(self, value:float):
        with self.link as lnk:
            lnk.write(f"VOLT {value:0.1f}")

    def _get_voltage(self) -> float:
        with self.link as lnk:
            return self.to_float(lnk.query("VOLT?"))

    def _read_voltage(self) -> float:
        with self.link as lnk:
            return self.to_float(lnk.query("MEAS:VOLT?"))

