#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

from ..base.dmm import BasicDmm, DmmConstants as dmc
from .sdm30xx_setup import SDM30xx_Setup

class SDM3055(BasicDmm):
    ''' 

    '''

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        from ..links import Visa
        self._link = Visa(self)

        self.setup = SDM30xx_Setup(self)
    
    def _read(self) -> float:
        with self._link as lnk:
            result = lnk.query("READ?")
            try:
                return float(result)
            except:
                self.log.error(f"'{result}' is not a valid floating point number")
                return -1
    

    # def __numeric_range_option(self, range_=None):
    #     ''' 
    #     '''
    #     if isinstance(range_, (float,int)):
    #         result = ("%f" % range_).rstrip('0').rstrip('.')
    #     else:
    #         match range_:
    #             case dmc.range.MIN:
    #                 result = "MIN"
    #             case dmc.range.MAX:
    #                 result = "MAX"
    #             case _:
    #                 raise ValueError(f"Invalid value for range : '{range_}'")
                
    #     return " " + result

    # def _configure(self, mode : dmc.mode, range_=None, **args):

    #     match mode:
    #         case dmc.mode.VOLT_DC:
    #             cmd = "CONF:VOLT:DC"
    #         case dmc.mode.VOLT_AC:
    #             cmd = "CONF:VOLT:AC"
    #         case dmc.mode.CURR_DC:
    #             cmd = "CONF:CURR:DC"
    #         case dmc.mode.CURR_AC:
    #             cmd = "CONF:CURR:AC"
    #         case _:
    #             raise ValueError(f"Invalid value for mode : '{mode}'")
        
    #     cmd += self.__numeric_range_option(range_)
            
    #     with self._link as lnk:
    #         lnk.write(cmd)
            


