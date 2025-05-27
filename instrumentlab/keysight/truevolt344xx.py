#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

from ..base.dmm import BasicDmm, DmmConstants as dmc
from .truevolt344xx_setup import Truevolt344xx_Setup

class Truevolt344xx(BasicDmm):
    ''' Base class for the following Keysight Truevolt DMMs:
        - 34460A
        - 34461A
        - 34465A
        - 34470A
    '''

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        from ..links import Visa
        self._link = Visa(self)

        self.setup = Truevolt344xx_Setup(self)
    
    def _read(self) -> float:
        with self._link as lnk:
            result = lnk.query("READ?")
            try:
                return float(result)
            except:
                self.log.error(f"'{result}' is not a valid floating point number")
                return -1
    
