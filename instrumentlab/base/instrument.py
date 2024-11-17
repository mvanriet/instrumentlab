#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0


import logging
from .attribute import AttributeProvider

class Instrument(AttributeProvider):
    ''' Base class for all instruments
    '''
    
    def __init__(self, name, **kwargs):
        super().__init__()

        self._name = name
        self._config = kwargs                       # TODO: make configparser object
        
        self._log = logging.getLogger("inst.%s" % name)
        self._link = None

    @property
    def config(self):
        ''' Returns the section of a ConfigParser with settings for this instrument.
        '''
        return self._config
    
