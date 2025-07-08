#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0


from ..subsystem import SubSystem
from ..attribute import Attribute

class FgenChannel(SubSystem):
    ''' Channel for a function generator.
    '''
    
    def __init__(self, inst, index):
        super().__init__(inst)
        self._inst = inst
        self._index = index

    @property
    def _link(self):
        return self._inst._link

    @property
    def index(self) -> int:
        return self._index
    
    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    @Attribute
    def enabled(self):
        raise NotImplementedError()
        
    @enabled.setter
    def enabled(self, value):
        raise NotImplementedError()

 