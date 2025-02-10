#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0


from ..instrument import Instrument
from ..subsystem import SubSystem
from ..attribute import Attribute

class SimplePsuReadout(SubSystem):
    ''' Interface class to return actual voltage and current.
    '''
    
    def __init__(self, inst:'SimplePsu'):
        super().__init__(inst)
        self._inst = inst
    
    
    voltage = Attribute()
    current = Attribute()


class SimplePsu(Instrument):
    ''' Interface class for the basic operations :
        * get and set current and voltage
        * enable/disable output + convenience functions
        * return actual output values
    '''
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.read = SimplePsuReadout(self)
    
    enabled = Attribute()

    def enable(self):
        ''' Convencience function to enable the output.'''
        self.enabled = True

    def disable(self):
        ''' Convenience function to disable the output.'''
        self.enabled = False

    voltage = Attribute()
    current = Attribute()
