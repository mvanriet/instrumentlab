
import time

def show_voltages(ea):
    ''' @public
    '''
    start = time.time()
    for _ in range(10):
        print( f"{ea.read.voltage}  {ea.read.current}" )
    print( time.time()-start)
    
def lock(ea):
    ''' @public
    '''
    ea.lock()

def unlock(ea):
    ''' @public
    '''
    ea.unlock()

def enable(ea):
    ''' @public
    '''
    ea.enable()

def disable(ea):
    ''' @public
    '''
    ea.disable()


def toggle(ea, ctrl):
    ''' @public
    '''
    while ctrl.ok():
        ea.voltage = 13
        time.sleep(0.1)
        ea.voltage = 3
        time.sleep(0.5)

        # ea.voltage = i
        # time.sleep(0.1)


