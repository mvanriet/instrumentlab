#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

import configparser 
import os
    
class Config():
    
    config = None
    
    @classmethod
    def read(cls, filename:str, optional=False):
        
        if not filename.endswith(".ini"):
            raise ValueError(f"Filename {filename} must end with .ini")

        filename = os.path.abspath(filename)
        
        if not os.path.isfile(filename):
            if not optional:
                raise FileNotFoundError((f"Filename {filename} not found"))
        else:
            if cls.config is None:
                cls.config = configparser.ConfigParser()
                cls.config.read(filename)
            else:
                new_config = configparser.ConfigParser()
                new_config.read(filename)

                #TODO: add sections from this config file to the config that is already read
                raise NotImplementedError("reading multiple config files not yet supported")
        
    @classmethod
    def get_config(cls, name:str, **kwargs) -> configparser.SectionProxy:
        ''' Returns settings for the given section in the ini-files.
            
            The arguments supplied as kwargs is also included, as if they were defined in
            the ini-file itself.  If there are duplicates, the ini-file values have priority.
            
            Everything is returned as a new ConfigParser section containing all values.
        '''
        
        if cls.config is None:                                  # create empty configparser if nothing has ever been read
            cls.config = configparser.ConfigParser()

        if not cls.config.has_section(name):                    # make empty section if nothing for this name yet
            cls.config[name] = dict()

        section = cls.config[name]                              # get the section for this name

        for key,value in kwargs.items():                        # add parameters provided to constructor
            if key not in section:                              # but only if they don't exist yet
                section[key] = str(value)

        return section                                          # now return only the section for this name

