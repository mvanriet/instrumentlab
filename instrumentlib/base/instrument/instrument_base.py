#--___---------_--------------------------_---_----_-_---------------------------------------------
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |  (_) |__     InstrumentLib                       |
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__| | '_ \    instrument_base.by                  |
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____|_|_.__/    Copyright 2024  Marc Van Riet e.a.  |
#--------------------------------------------------------------------------------------------------
# Licensed under the Apache License, Version 2.0 (the "License");                                 |
# you may not use this file except in compliance with the License.                                |
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0              |
# Unless required by applicable law or agreed to in writing, software distributed under the       |
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,       |
# either express or implied. See the License for the specific language governing permissions      |
# and limitations under the License.                                                              |
# Original source code and License available at https://github.com/mvanriet/instrumentlib         |
#--------------------------------------------------------------------------------------------------

import logging

class InstrumentBase():
    
    def __init__(self, name, link, config):
        
        self._name = name
        self._link = link
        self._config = config
        
        self.log = logging.getLogger("inst.%s" % name)

    @property
    def link(self):
        return self._link

    @property
    def config(self):
        ''' Returns the section of a ConfigParser with settings for this instrument.
        '''
        return self._config
    
