#  ___         _                          _   _    _ _
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |  (_) |__   InstrumentLib
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__| | '_ \  instrument_base.by
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____|_|_.__/  (C) 2024  Marc Van Riet et al.
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
    
    @Attribute
    def voltage(self):
        return self._inst.read_voltage()

    @Attribute
    def current(self):
        return self._inst.read_current()


class SimplePsu(Instrument):
    ''' Interface class for the basic operations :
        * get and set current and voltage
        * enable/disable output + convenience functions
        * return actual output values
    '''
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.read = SimplePsuReadout(self)
    
    @Attribute
    def enabled(self):
        return self.get_enabled()

    @enabled.setter
    def enabled(self, value):
        self.set_enabled(value)   

    def enable(self):
        ''' Convencience function to enable the output.'''
        self.set_enabled(True)

    def disable(self):
        ''' Convenience function to disable the output.'''
        self.set_enabled(False)

    @Attribute
    def voltage(self):
        return self.get_voltage()

    @voltage.setter
    def voltage(self, value):
        self.set_voltage(value)   
    
    @Attribute
    def current(self):
        return self.get_current()

    @current.setter
    def current(self, value):
        self.set_current(value)

    # abstract methods below; to be implemented in derived class

    def set_enabled(self, value:bool):
        raise NotImplementedError()

    def get_enabled(self) -> bool:
        raise NotImplementedError()
    
    def set_voltage(self, value:float):
        raise NotImplementedError()

    def get_voltage(self) -> float:
        raise NotImplementedError()

    def read_voltage(self) -> float:
        raise NotImplementedError()

    def set_current(self, value:float):
        raise NotImplementedError()

    def get_current(self) -> float:
        raise NotImplementedError()

    def read_current(self) -> float:
        raise NotImplementedError()
