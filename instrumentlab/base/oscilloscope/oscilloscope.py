#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0


from ..instrument import Instrument
from ..attribute import Attribute
from .oscilloscope_channel import OscilloscopeChannel



class Oscilloscope(Instrument):
    ''' Interface class for the basic operations :
        * get and set current and voltage
        * enable/disable output + convenience functions
        * return actual output values
    '''
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.channels = [ OscilloscopeChannel(self, 0) ]

    
 