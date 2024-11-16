

import threading

class LinkBase():
    
    def __init__(self, instrument):
        '''
        '''
        self._inst = instrument
        self.log = instrument.log
        
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


    
        

