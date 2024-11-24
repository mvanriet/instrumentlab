#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

import numpy as np

from ...base.oscilloscope.oscilloscope import Oscilloscope
from .infiniium_channel import InfiniiumChannel


class InfiniiumScope(Oscilloscope):
    
    
    def __init__(self, name, **kwargs):
        
        super().__init__(name, **kwargs)

        from ...links import Visa
        self._link = Visa(self)

        # two-channel scope
        self.channels = [ InfiniiumChannel(self, idx) for idx in range(2) ]
                
    def get_id(self):
        ''' Return ID of scope
        '''
        with self._link as lnk:
            return lnk.query("*IDN?")
    
