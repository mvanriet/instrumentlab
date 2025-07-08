#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

import numpy as np

from ..base.oscilloscope.oscilloscope import Oscilloscope
from ..base.subsystem import SubSystem

class WaveForm:
    
    def __init__(self, scope, channel):
        ''' Gets waveform of the specified channel.
        '''
        self.channel = channel
        self.data = scope.get_numpy_data(channel)
        (self.x0, self.dx, self.y0, self.dy) = scope.get_data_info()
        self.size = self.data.size
        

    def xvalues(self, scale=1):
        ''' Returns numpy array of X-values
        '''
        return np.linspace(self.x0*scale, (self.x0+self.dx*self.size)*scale, self.size)


class AgilentMeasure(SubSystem):
    
    def __init__(self, inst):
        super().__init__(inst)
        
    def fall_time(self, channel):
        cmd = ":MEAS:FALL? CHANNEL%d" % channel
        return self.get_value(cmd)

    def rise_time(self, channel):
        cmd = ":MEAS:RIS? CHANNEL%d" % channel
        return self.get_value(cmd)
    
    def vmax(self, channel):
        cmd = ":MEAS:VMAX? CHANNEL%d" % channel
        return self.get_value(cmd)

    def vmin(self, channel):
        cmd = ":MEAS:VMIN? CHANNEL%d" % channel
        return self.get_value(cmd)
    
    def vbase(self, channel):
        cmd = ":MEAS:VBAS? CHANNEL%d" % channel
        return self.get_value(cmd)
    
    def vtop(self, channel):
        cmd = ":MEAS:VTOP? CHANNEL%d" % channel
        return self.get_value(cmd)
    

class DSO54830B(Oscilloscope):
    
    
    def __init__(self, name, **kwargs):
        
        super().__init__(name, **kwargs)

        from ..links import Visa
        self._link = Visa(self)
        
        self.measure = AgilentMeasure(self)        
        
    def get_id(self):
        ''' Return ID of scope
        '''
        with self._link as lnk:
            return lnk.query("*IDN?")
    
    def set_defaults(self):
        ''' scope to default settings.
        '''
        self.write(":SYSTEM:PRESET")
        
    def set_acquisition_points(self, count):
        ''' Set number of acquisition points.
        '''
        self.write(":ACQ:INT OFF")                 # no sin(x0/x interpolation
        self.write(":ACQ:POIN %d" % count)         # set number of points
        self.write(":ACQ:SRAT AUTO")               # sample rate automatic
        
    def set_acquisition_auto(self):
        ''' Set acquisition points and rate to auto.
        '''
        self.write(":ACQ:INT OFF")
        self.write(":ACQ:POIN AUTO")
        self.write(":ACQ:SRAT AUTO")
        
    def acquire(self, timeout=5):
        ''' Make sure a new waveform is acquired.
        '''
        self.query(":ADER?")                       # clear ADER event
        
        count = 0
        while count < 10*timeout:
            reply = self.query(":ADER?") 
            if reply.startswith("+1"):
                break
        
    def set_timebase(self, time_per_div):
        ''' Sets the time per division for the timebase (horizontal)
        '''
        self.write(":TIM:SCAL %G" % time_per_div)
        
    def get_time_range(self):
        ''' Gets the time range of the window that is displayed.
            Result : left time, right time, full range, position
        '''
#         pos = self.get_value(":TIM:WIND:POS?")
#         rang = self.get_value(":TIM:WIND:RANG?")
        pos = self.get_value(":TIM:POS?")
        rang = self.get_value(":TIM:RANG?")
        
        left = -rang/2 + pos
        right = rang/2 + pos
        return (left, right, rang, pos)
        
        
    def set_trigger(self, channel, position=None, level=None, rising=None, falling=None):
        ''' Sets the trigger.
        '''
        self.write(":TRIG:EDGE:SOURCE CHAN%d" % channel)
        
        if position is not None:
            self.write(":TIM:POS %G" % position)
            
        if rising is not None or falling is not None:
            if rising == True and falling == True:
                self.write(":TRIG:EDGE:SLOP EITH")
            elif rising == True or falling == False:
                self.write(":TRIG:EDGE:SLOP POS")
            else:
                self.write(":TRIG:EDGE:SLOP NEG")

        if level is not None:
            self.write(":TRIG:LEV CHAN%d, %G" % (channel, level) )
        
    def set_vertical(self, channel, voltage, offset = None):
        ''' \public 
            Set voltage/div for channel, and optionally offset.
            Negative offset moves the waveform up.
        '''
        self.write(":CHAN%d:SCAL %G" % (channel, voltage) )
        if offset is None:
            offset = 3*voltage
        self.write(":CHAN%d:OFFS %G" % (channel, offset) )
        
    def show(self, channel, visible=True):
        ''' Show or hide a channel.
        '''
        if visible:
            self.write("CHAN%d:DISP ON" % channel )
        else:
            self.write("CHAN%d:DISP OFF" % channel )
            
    def get_data(self, channel):
        ''' Get data for a channel
        '''
        if isinstance(channel, str):
            self.write(":WAV:SOUR %s" % channel )
        else:
            self.write(":WAV:SOUR CHAN%d" % channel )
        self.write(":WAV:FORM ASC" )
        self.write(":WAV:VIEW ALL" )
        data = self.query_ascii_values(":WAV:DATA?")
        
        return data
    
    def get_numpy_data(self, channel):
        ''' Get data for a channel as a numpy array
        '''
        if isinstance(channel, str):
            self.write(":WAV:SOUR %s" % channel )
        else:
            self.write(":WAV:SOUR CHAN%d" % channel )
        self.write(":WAV:FORM ASC" )
        self.write(":WAV:VIEW ALL" )
        data = self.get_array(":WAV:DATA?")
        return data
    
    def get_data_info(self):
        ''' Get info about waveform data like start point, offset, ...
        '''
        x0 = self.get_value(":WAV:XOR?")
        dx = self.get_value(":WAV:XINC?")
        y0 = self.get_value(":WAV:YOR?")
        dy = self.get_value(":WAV:YINC?")
    
        return (x0, dx, y0, dy)
    
    def get_waveform(self, channel):
        ''' Returns an object with data and info.
        '''
        return WaveForm(self, channel)
    