#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

from ..base.load.basic_dcload import BasicDcLoad

class EL9000_DT(BasicDcLoad):
    ''' Base class to derive instruments from with a given voltage/current range.
    '''

    def __init__(self, name, limits, **kwargs):
        super().__init__(name, terminator="lf", **kwargs)

        from ..links import Visa
        self._link = Visa(self)
        self.limits = limits

    def lock(self):
        with self.link as lnk:
            lnk.write("SYST:LOCK ON")

    def unlock(self):
        with self.link as lnk:
            lnk.write("SYST:LOCK OFF")

    def _set_enabled(self, value:bool):
        with self.link as lnk:
            lnk.write("INP ON;" if value else "INP OFF;")

    def _get_enabled(self):
        with self.link as lnk:
            status = lnk.query("INPUT?")
        return True if "ON" in status else False

    def _set_all(self, voltage:float=None, current:float=None, power:float=None):
        ''' Set the current and/or voltage and/or power in 1 command.
            When given as a number, current is in A, voltage in V and power in W.
            Text strings like 'MIN' and 'MAX' are also possible.
        '''
        cmd = ""
        if current is not None:
            if not isinstance(current, str):
                current = "%.3fA" % current
            cmd += "CURR %s;" % current
        if voltage is not None:
            if not isinstance(voltage, str):
                voltage = "%.3fV" % voltage
            cmd += "VOLT %s;" % voltage
        if power is not None:
            if not isinstance(power, str):
                power = "%.3fW" % power
            cmd += "POW %s;" % power

        if len(cmd)>0:
            with self.link as lnk:
                lnk.write(cmd)

    def _get_all(self):
        ''' Get setpoint for voltage, current and power as a tuple.
        '''
        with self.link as lnk:
            reply = lnk.query("VOLT?;CURR?;POW?")
        results = reply.split(";")                       # should be like "0.00 V; 0.00 A; 0.0 W"          
        
        if len(results) != 3:                            # check the length
            raise ValueError("Unexpected reply from load.")
        
        volt = None
        current = None
        power = None
        
        if results[0].endswith('V'):                     # try and convert voltage
            try:
                volt = float(results[0][:-1])
            except ValueError:
                pass
             
        if results[1].endswith('A'):                     # try and convert current
            try:
                current = float(results[1][:-1])
            except ValueError:
                pass

        if results[2].endswith('W'):                     # try and convert power 
            try:
                power = float(results[2][:-1])
            except ValueError:
                pass
            
        if None in ( volt, current, power ):
            raise ValueError("Load didn't return a valid value.")
            
        return ( volt, current, power )


    def _read_all(self):
        ''' Get actual voltage, current and power as a tuple.
        '''
        with self.link as lnk:
            reply = lnk.query("MEAS:SCAL:ARR?")
        results = reply.split(",")                       # should be like "0.00 V, 0.00 A, 0.0 W"          
        
        if len(results) != 3:                            # check the length
            raise ValueError("Unexpected reply from load.")
        
        volt = None
        current = None
        power = None
        
        if results[0].endswith('V'):                     # try and convert voltage
            try:
                volt = float(results[0][:-1])
            except ValueError:
                pass
             
        if results[1].endswith('A'):                     # try and convert current
            try:
                current = float(results[1][:-1])
            except ValueError:
                pass

        if results[2].endswith('W'):                     # try and convert power 
            try:
                power = float(results[2][:-1])
            except ValueError:
                pass
            
        if None in ( volt, current, power ):
            raise ValueError("Load didn't return a valid value.")
            
        return ( volt, current, power )

##################################################################################################

def EL9080_45DT(name, **kwargs) -> EL9000_DT:
    ''' EL9080-45DT 45V 80A DC load.
    '''
    return EL9000_DT(name, (45, 80), **kwargs)

