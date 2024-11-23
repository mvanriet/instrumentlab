#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0


from ..subsystem import SubSystem
from ..attribute import Attribute

class OscilloscopeChannel(SubSystem):
    ''' Interface class to return actual voltage and current.
    '''
    
    def __init__(self, inst, index):
        super().__init__(inst)
        self._inst = inst
        self._index = index

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    @Attribute
    def enabled(self):
        return self._get_enabled()

    @enabled.setter
    def enabled(self, value):
        self._set_enabled(value)

    @Attribute
    def scale(self):
        return self._get_scale()
    
    @scale.setter
    def scale(self, value):
        self._set_scale(value)

    @Attribute
    def offset(self):
        return self._get_offset()

    @offset.setter
    def offset(self, value):
        self._set_offset(value)

    @Attribute
    def coupling(self):
        return self._get_coupling()

    @coupling.setter
    def coupling(self, value):
        self._set_coupling(value)

    @Attribute
    def bandwidth(self):
        return self._get_bandwidth()

    @bandwidth.setter
    def bandwidth(self, value):
        self._set_bandwidth(value)

    @Attribute
    def impedance(self):
        return self._get_impedance()

    @impedance.setter
    def impedance(self, value):
        self._set_impedance(value)

    # abstract methods below; to be implemented in derived class
    
    def _get_enabled(self):
        raise NotImplementedError()
    def _set_enabled(self, value:bool):
        raise NotImplementedError()

    def _get_scale(self):
        raise NotImplementedError()
    def _set_scale(self, value:float):
        raise NotImplementedError()

    def _get_offset(self):
        raise NotImplementedError()
    def _set_offset(self, value:float):
        raise NotImplementedError()

    def _get_coupling(self):
        raise NotImplementedError()
    def _set_coupling(self, value:bool):
        raise NotImplementedError()

    def _get_bandwidth(self):
        raise NotImplementedError()
    def _set_bandwidth(self, value:int):
        raise NotImplementedError()

    def _get_impedance(self):
        raise NotImplementedError()
    def _set_impedance(self, value:int):
        raise NotImplementedError()


