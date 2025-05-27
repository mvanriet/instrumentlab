#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

import logging

from .attribute import AttributeProvider
from .subsystem import SubSystem

class InstrumentSetup(AttributeProvider):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self._inst = parent._inst if isinstance(parent, SubSystem) else parent
   
    @property
    def link(self):
        return self._inst.link
    
    @property
    def log(self) -> logging.Logger:
        return self.parent.log

    