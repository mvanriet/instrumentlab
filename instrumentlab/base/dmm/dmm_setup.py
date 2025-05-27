#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0


from ..instrument_setup import InstrumentSetup
from ..attribute import Attribute

from .dmm_constants import DmmConstants as DMC

class DmmSetup(InstrumentSetup):
    ''' Interface class for configuring a DMM
    '''
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent)

    @Attribute
    def mode(self) -> DMC.mode:
        """Get the current mode of the DMM."""
        raise NotImplementedError("Getting mode is not implemented in this base class.")

    @mode.setter
    def mode(self, value: DMC.mode):
        """Set the mode of the DMM."""
        raise NotImplementedError("Setting mode is not implemented in this base class.")
