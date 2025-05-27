#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0


import logging
from .attribute import AttributeProvider
from .config import Config

class Instrument(AttributeProvider):
    ''' Base class for all instruments
    '''
    
    def __init__(self, name, **kwargs):
        super().__init__()

        self._name = name
        self._config = Config.get_config(name, **kwargs)              # take settings from ini-file and kwargs
        
        self._log = logging.getLogger("inst.%s" % name)
        self._link = None

    @property
    def link(self):
        ''' The link to the instrument.
        '''
        return self._link

    # def get_config(self):
    #     ''' Returns the section of a ConfigParser with settings for this instrument.
    #     '''
    #     return self._config
    
