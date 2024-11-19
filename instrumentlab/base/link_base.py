#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

import threading
from .instrument import Instrument
from .config import Config

class LinkBase():
    
    def __init__(self, instrument : Instrument, **kwargs):
        '''
        '''
        self._inst = instrument
        self.log = instrument._log                                      # take logger object from instrument
        self._config = Config.get_config(instrument._name, **kwargs)    # take settings from ini-file and add kwargs

        self._lock = threading.Lock()                       # semaphore for access to this link

    ######## open and close ###################################################
                        
    def open(self):
        ''' Open the port if necessary.  Does nothing if port is already open.
        '''
        pass
    
    def close(self):
        pass

    def __del__(self):
        ''' Close all connections (if necessary) when connection is destroyed
            (typically when the program is terminated).
        '''
        self.close()

    ######## getting and releasing access #####################################

    def acquire(self):
        ''' Acquires semaphore for using the connection.
            Then return an object with all the interface methods using get_link().
        '''
        self._lock.acquire()
        self.open()
        return self

    def release(self):
        ''' Releases the semaphore for using the connection.
            Must be called after every acquire()
        '''
        self._lock.release()

    def __enter__(self):
        ''' Automatic acquire/release of semaphore using context manager
        '''
        return self.acquire()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        ''' Automatic acquire/release of semaphore using context manager.
        '''
        self.release()
        return False


    
        

