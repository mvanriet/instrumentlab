#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

from ..base.fgen import BasicFgen
# from ..base.fgen.fgen_constants import FgenConstants as fgc

from .afg3000_channel import Afg3000Channel

class Afg3000(BasicFgen):
    ''' Base class for Tektronix AFG3000 series function generators.
    '''

    def __init__(self, name, **kwargs):
        super().__init__(name, num_channels=2, **kwargs)

        from ..links import Visa
        self._link = Visa(self)

        self.channels = [ Afg3000Channel(self, idx+1) for idx in range(2) ]
        self.CH1 = self.channels[0]
        self.CH2 = self.channels[1]

    def get_id(self):
        ''' Return ID of scope
        '''
        with self._link as lnk:
            return lnk.query("*IDN?")
        