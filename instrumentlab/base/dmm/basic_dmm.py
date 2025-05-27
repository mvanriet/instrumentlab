#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0


from ..instrument import Instrument


class BasicDmm(Instrument):
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def read(self):
        ''' Read the present value from the DMM.
        '''
        return self._read()
    
    # abstract methods below; to be implemented in derived class

    def _read(self) -> float:
        raise NotImplementedError()
    

