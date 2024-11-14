'''___         _                          _   _    _ _
  |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |  (_) |__   InstrumentLib
   | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__| | '_ \  korad/KAxxxxP.by
  |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____|_|_.__/  (C) 2024  Marc Van Riet et al.

  Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0
'''

import time
import serial

from ..base.link.link_base import LinkBase


class KoradSlowSerial(LinkBase):
    ''' Handler for communication with Korad power supplies using the serial port.
        See https://sigrok.org/wiki/Korad_KAxxxxP_series#Protocol for details.

        Delays have been determined experimentally to avoid communication errors.
    '''

    WRITE_DELAY_S = 0.055                # minimum time between two writes
    READ_WAIT_S = 0.1                    # minimum time to wait before aborting a read

    def __init__(self, instrument):
        ''' Opens connection over serial port.
        '''
        super().__init__(instrument)
        
        self.port = None
        self.last_write = time.time()

    def open(self):
        ''' Opens serial port if necessary
        '''
        if self.port is not None:                               # skip if port already open
            return

        cfg = self.config
        if "comport" in cfg:
            portname = cfg.get("comport")
        else:
            raise Exception(f"Comport not found in settings for {self.name}")
        
        baudrate = cfg.getint("baudrate", fallback = 9600)

        self.log.debug(f"Opening COM port {portname} at {baudrate} baud")

        try:                                                    # open port with 20ms read timeout
            self.port = serial.Serial(portname, baudrate, timeout=0.02)
        except serial.serialutil.SerialException:
            self.log.error("Could not open COM port %s", self.portname)
            self.port = None

        return

    def close(self):
        ''' Closes serial thread and connection.
        '''
        if self.port is None:                                   # skip if port not open
            return

        self.port.close()
        self.port = None

    def write(self, data):
        ''' Writes binary data to the port.
            Time is tracked to make sure that two writes are not too fast after one another.
        '''
        assert self.port is not None, "Serial port must be opened first"

        data = data.strip().encode()

        dt = time.time() - self.last_write

        if dt < self.WRITE_DELAY_S:                     # check if we didn't write too fast
            dt = self.WRITE_DELAY_S - dt                # the extra time we need to wait
            if dt < 0.005:
                time.sleep(0.005)                       # wait at least 5ms
            else:
                time.sleep(dt)                          # otherwise just wait the extra time

        self.port.write(data)                           # write data
        self.port.flush()
        # remember time of last write
        self.last_write = time.time()

    def read(self, numbytes=8):
        ''' Reads data, up to a number of bytes.
        '''
        rd_start = time.time()                          # remember when we start reading

        buf = bytearray()                               # buffer with result

        while True:
            in_byte = self.port.read(1)                 # read a byte

            if len(in_byte) == 0:                               # no data any more
                if time.time() - rd_start > self.READ_WAIT_S:   # and we've waited long enough
                    print("read timeout")
                    break                                       # then it's OK to stop
                else:
                    continue

            buf += bytearray(in_byte)                   # add received byte to buffer

            if len(buf) >= numbytes:                    # stop if enough bytes read
                break

        if len(buf) == 0:                               # no data received -> return None
            return None

        if len(buf) == 1:                               # single byte = status -> return as integer
            return int(buf[0])

        return buf.decode("utf-8")                      # >1 byte = text reply -> return as string

    def write_read(self, cmd, numbytes=99):
        ''' Sends command, wait 1/10th of a second, and then checks the reply.
            Stupid way to do because I couldn't get a queue or semaphore to work.
        '''
        self.port.reset_input_buffer()
        self.write(cmd)                                    # send command
        return self.read(numbytes)

    def query_float(self, cmd):
        ''' Sends a command that expects a floating point number as reply.
            Returns the floating point number.
            
            Korad always replies with exactly 5 characters for a number, either xx.xx or x.xxx.
            Reply can contain a leftover character from a previous command (firmware bug).
            Therefore only characters '.' and '1'-'9' are accepted.
            Any illegal character is assumed to be from a previous reply.
        '''
        if not '?' in cmd:
            raise ValueError("Korad query command must contain question mark.")
    
        self.write(cmd)
    
        rd_start = time.time()                          # remember when we start reading

        buf = bytearray()                               # buffer with result

        while len(buf)<5:                               # read at most 5 bytes
            
            in_byte = self.port.read(1)                 # read a byte

            if len(in_byte) == 0:                               # no data any more
                if time.time() - rd_start > self.READ_WAIT_S:   # and we've waited long enough
                    break                                       # then it's OK to stop
                else:
                    continue                                    # go wait for next character

            the_byte = in_byte[0]
            if the_byte!=46 and (the_byte<48 or the_byte>57):   # not a valid character
                buf = bytearray()                               # reset receive buffer
                continue

            buf += bytearray(in_byte)                   # add received byte to buffer

        # print(f"<<{buf.decode('utf-8')}<<")

        if len(buf)!=5:                                 # something wrong : reply must always be 5 bytes
            raise ValueError("Power supply didn't reply with 5 bytes.")

        try:
            fvalue = float(buf.decode("utf-8"))         # try to convert reply to floating point
        except (ValueError, TypeError):
            fvalue = -1
            
        if fvalue<0:
            raise ValueError("Power supply didn't return a valid value.")

        return fvalue
