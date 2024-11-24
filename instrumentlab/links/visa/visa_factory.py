#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

from ...base.config import Config
from ...base.instrument import Instrument

def Visa(inst:'Instrument'):
    ''' Return a link to a Visa instrument.
        Typically, pyvisa is used.  However, other implementations could be possible.
    '''

    config = Config.get_config(inst._name)              # get the settings for the instrument

    if "pyvisa" in config:                              # we need to use pyvisa
        from .pyvisa_link import PyVisaLink
        return PyVisaLink(inst)                         # return the wrapper for pyvisa
    
    return ConnectionRefusedError( 
        f"No configuration settings found for Visa connection to {inst._name}")
    
