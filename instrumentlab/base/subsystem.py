#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

import logging

# from .instrument import Instrument
from .attribute import AttributeProvider

class SubSystem(AttributeProvider):
    ''' Base class for subsystems of an instrument.
    '''
    def __init__(self, inst:'Instrument'):
        super().__init__()
        self._inst = inst
   
    @property
    def link(self):
        return self._inst.link
    
    @property
    def log(self) -> logging.Logger:
        return self._inst.log
