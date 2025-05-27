#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

import time

from ..instrument import Instrument
from ..subsystem import SubSystem
from ..attribute import Attribute

# Don't do get or read again if faster than this interval.  We always read voltage, current
# and power at once.  Separate read.voltage / ... can then return the latest value that
# was received.  0.5ms is smaller than the typical time it takes to do a query over USB or
# Ethernet, but larger than the time for things like printing or logging a single value.
NO_REDO_INTERVAL_S = 0.0005       #  (=0.5 ms) 

class BasicDcLoadReadout(SubSystem):
    ''' Interface class to return actual voltage, current and power.
    '''
    
    def __init__(self, inst:'BasicDcLoad'):
        super().__init__(inst)
        self._inst = inst
    
    @Attribute
    def voltage(self):
        voltage, _, _ = self._inst.read_all()
        return voltage

    @Attribute
    def current(self):
        _, current, _ = self._inst.read_all()
        return current

    @Attribute
    def power(self):
        _, _, power = self._inst.read_all()
        return power


class BasicDcLoad(Instrument):
    ''' Interface class for the basic operations :
        * get and set current, voltage and power
        * enable/disable output + convenience functions
        * return actual values
    '''
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.read = BasicDcLoadReadout(self)
        self._last_read = 0
        self._last_read_values = (0, 0, 0)
        self._last_get = 0
        self._last_get_values = (0, 0, 0)
    
    def enable(self):
        ''' Convencience function to enable the output.'''
        self._set_enabled(True)

    def disable(self):
        ''' Convenience function to disable the output.'''
        self._set_enabled(False)

    # 'enabled' property and virtual methods

    @Attribute
    def enabled(self) -> bool:
        return self._get_enabled()
    
    @enabled.setter
    def enabled(self, value:bool):
        self._set_enabled(value)

    def _set_enabled(self, value:bool):
        raise NotImplementedError()

    def _get_enabled(self) -> bool:
        raise NotImplementedError()

    # virtual method for set_all is clears caching timers for get_all and read_all

    def set_all(self, voltage:float=None, current:float=None, power:float=None):
        self._last_get = 0
        self._last_read = 0
        self._set_all(voltage, current, power)
    
    def _set_all(self, voltage:float, current:float, power:float):
        raise NotImplementedError()

    # virtual method for get_all does caching
    # use 'get' for the setpoint values

    def get_all(self) -> tuple[float, float, float]:
        if time.time()-self._last_get > NO_REDO_INTERVAL_S:
            self._last_get_values = self._get_all()
            self._last_get = time.time()
        return self._last_get_values
        
    def _get_all(self) -> tuple[float, float, float]:
        raise NotImplementedError()

    # virtual method for read_all does caching
    # use 'read' for the real-time readings from the device

    def read_all(self) -> tuple[float, float, float]:
        if time.time()-self._last_read > NO_REDO_INTERVAL_S:
            self._last_read_values = self._read_all()
            self._last_read = time.time()
        return self._last_read_values

    def _read_all(self) -> tuple[float, float, float]:
        raise NotImplementedError()

    # properties for voltage, current and power use the set/get_all methods

    @Attribute
    def voltage(self) -> float:
        voltage, _, _ = self.get_all()
        return voltage

    @voltage.setter
    def voltage(self, value:float):
        self.set_all(voltage=value)

    @Attribute
    def current(self) -> float:
        _, current, _ = self.get_all()
        return current

    @current.setter
    def current(self, value:float):
        self.set_all(current=value)

    @Attribute
    def power(self) -> float:
        _, _, power = self.get_all()
        return power

    @power.setter
    def power(self, value:float):
        self.set_all(power=value)

