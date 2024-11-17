#  ___         _                          _   _    _ _
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |  (_) |__   InstrumentLib
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__| | '_ \  instrument_base.by
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____|_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

class Attribute:
    ''' Like a property for a class, but with extra functionality.
        Intended to be used with classes derived from Instrument_Base
        Calls the method _cache_value on the object to remember the value that
        was last read or written.
    '''

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __set_name__(self, owner, name):
        self.__name__ = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError( f'No setter for {type(obj).__name__!r}.{self.__name__!r}' )
        value = self.fget(obj)
        obj._cache_value(self.__name__, value)
        return value

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError
        obj._cache_value(self.__name__, value)
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)
    

class AttributeRef():
    ''' Reference to a property/Attribute of a class.
        Is returned when using [] on an object with the property name.
        Use methods get() and set() to get/set the property value.
        When used in combination with InstrumentBase, also supports methods peek() and poke()
        to access values using caching to avoid unnecesasay commands to the instrument.
    '''

    def __init__(self, obj:'SubSystem', propname):
        # if not hasattr(obj, propname):                    # this does a get !!!
        #     raise KeyError(f"Class '{type(obj).__name__}' has no property '{propname}'")
        self.obj = obj
        self.propname = propname

    def set(self, value):
        setattr( self.obj, self.propname, value)

    def get(self):
        return getattr( self.obj, self.propname)
    
    def peek(self):
        return self.obj.peek(self.propname)
    
    def poke(self, value):
        return self.obj.poke(self.propname, value)
    

class AttributeProvider():
    ''' Base class for subsystems of an instrument.
    '''
    def __init__(self):
        self.__attribute_cache = dict()               # for caching Attribute values

    def __getitem__(self, propname):
        return AttributeRef(self, propname)

    def _cache_value(self, name, value):
        ''' Called by setter/getter of an Attribute.  The cached value is used by
            peek() and poke() to avoid unnecessary read and writes to the instrument.
        '''
        self.__attribute_cache[name] = value

    def peek(self, name):
        ''' Return the cached value of an Attribute.
            If no value is cached yet, the actual value of the Attributed is requested.
        '''
        if name in self.__attribute_cache:
            return self.__attribute_cache[name]
        else:
            return getattr(self, name)
    
    def poke(self, name, value):
        ''' Write a value to an Attribute using caching.
            It is ignored if the new value is the same as the cached value.
        '''
        cache_value = self.__attribute_cache.get(name)
        if cache_value is None or cache_value!=value:
            setattr(self, name, value)
