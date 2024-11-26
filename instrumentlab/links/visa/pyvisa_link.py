#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

from ...base.link_base import LinkBase
from ...base.instrument import Instrument

pyvisa_rm = None

class PyVisaLink(LinkBase):
    ''' 
    '''

    def __init__(self, instrument:'Instrument', **kwargs):
        ''' Opens connection over serial port.
        '''
        super().__init__(instrument, **kwargs)
        
        self._pyvisa_conn = None


    def acquire(self):
        ''' the context manager should return the pyvisa connection itself,
            not this wrapper class.
        '''
        super().acquire()
        return self._pyvisa_conn

    def open(self):
        ''' Opens pyvisa connection if necessary
        '''
        if self._pyvisa_conn is not None:
            return

        if not "pyvisa" in self._config:                                # check if the connection string is found
            raise Exception(f"visa address not found in settings for {self._inst._name}")

        global pyvisa_rm
        if pyvisa_rm is None:                                       # instantiate resource manager if necessary
            import pyvisa
            pyvisa_rm = pyvisa.ResourceManager()
        
        self._pyvisa_conn = pyvisa_rm.open_resource(self._config["pyvisa"])    # open the instrument
        
        if "baudrate" in self._config:
            self._pyvisa_conn.baud_rate = self._config.getint("baudrate")
        if "flowcontrol" in self._config:
            self._pyvisa_conn.flow_control = self._config.getint("flowcontrol")
        if "terminator" in self._config:
            eol = self._config.get("terminator", "crlf").lower()
            if eol=="cr":
                self._pyvisa_conn.read_termination='\r'
                self._pyvisa_conn.write_termination='\r'
            elif eol=="lf":
                self._pyvisa_conn.read_termination='\n'
                self._pyvisa_conn.write_termination='\n'
            elif eol=="crlf":
                self._pyvisa_conn.read_termination='\r\n'
                self._pyvisa_conn.write_termination='\r\n'
            else:
                raise Exception(f"value {eol} for visa_eol is invalid, excpect cr, lf or crlf")

    def close(self):
        ''' Closes connection to instrument
        '''
        if self._pyvisa_conn is None:
            return
        
        self._pyvisa_conn.close()
        self._pyvisa_conn = None

