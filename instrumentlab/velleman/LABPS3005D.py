'''___         _                          _   _    _ _
  |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |  (_) |__   InstrumentLib
   | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__| | '_ \  velleman/LABPS3005D.by
  |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____|_|_.__/  (C) 2024  Marc Van Riet et al.

  Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0
'''

from ..korad.KAxxxxP import KA3005P

class LABPS3005D(KA3005P):
    ''' LABPS3005D is identical to Korad KA5003.

        Note that the LABPS3005DN is not identical.  See LABPS3005DN.py
    '''

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
