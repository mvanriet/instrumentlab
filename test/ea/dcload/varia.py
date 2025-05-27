
import time
from instrumentlab.ea import EL9080_45DT

def show_reading(dcload:EL9080_45DT):
    ''' @public
    '''
    volt, current, power = dcload.read_all()
    print( f"{volt}  {current}  {power}" )

def show_settings(dcload:EL9080_45DT):
    ''' @public
    '''
    print( f"{dcload.voltage}  {dcload.current}  {dcload.power}" )

def show_readings2(dcload:EL9080_45DT):
    ''' @public
    '''
    print( f"{dcload.read.voltage}  {dcload.read.current}  {dcload.read.power}" )

def lock(dcload:EL9080_45DT):
    ''' @public
    '''
    dcload.lock()

def unlock(dcload:EL9080_45DT):
    ''' @public
    '''
    dcload.unlock()

def enable(dcload:EL9080_45DT):
    ''' @public
    '''
    dcload.enable()

def disable(dcload:EL9080_45DT):
    ''' @public
    '''
    dcload.disable()


