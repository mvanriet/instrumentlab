#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

class Attribute:
    ''' Like a property for a class, but with extra functionality.
        Can only be used on classes that inherit from AttributeProvider.
        Calls the method _cache_value on the object to remember the value that was last read or written.
        Also looks for the getter and setter functions in the base classes if not defined in the class itself.
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

    def __get__(self, obj:'AttributeProvider', objtype=None):
        ''' Calls the getter function for this property.

            If the setter function is not defined in the class, it looks in the base classes.
            If no setter function is found, a NotImplementedError exception is raised.
            Note that this is quite exotic, because typically a getter is always defined.

            The value is cached using the _cache_value() method of the AttributeProvider base class.
        '''
        if obj is None:
            return self

        if self.fget is None:
            for cls in type(obj).__bases__:
                if self.__name__ in cls.__dict__ and isinstance(cls.__dict__[self.__name__], Attribute):
                    self.fget = cls.__dict__[self.__name__].fget
                    break

            if self.fget is None:
                raise NotImplementedError( f'Getter for {type(obj).__name__!r}.{self.__name__!r} not implemented!' )

        value = self.fget(obj)
        obj._cache_value(self.__name__, value)
        return value

    def __set__(self, obj:'AttributeProvider', value):
        ''' Calls the setter function for this property.

            If the setter function is not defined in the class, it looks in the base classes.
            If no setter function is found, a NotImplementedError exception is raised.

            The value is cached using the _cache_value() method of the AttributeProvider base class.
        '''
        if self.fset is None:
            for cls in type(obj).__bases__:
                if self.__name__ in cls.__dict__ and isinstance(cls.__dict__[self.__name__], Attribute):
                    self.fset = cls.__dict__[self.__name__].fset
                    break

            if self.fset is None:
                raise NotImplementedError( f'Setter for {type(obj).__name__!r}.{self.__name__!r} not implemented!' )

        obj._cache_value(self.__name__, value)          # remember the value that was written
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise NotImplementedError( f'Deleter for {type(obj).__name__!r}.{self.__name__!r} not implemented!' )
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)
    

class AttributeRef():
    ''' Reference to a property/Attribute of a class.
        Is returned when using [] on an AttributeProvider object with the property name.
        Use methods get() and set() to get/set the property value.
        peek() reads the cached value if present, otherwise the actual value is read.
        poke() writes a value only if it is different from the cached value.
    '''

    def __init__(self, obj:'AttributeProvider', propname):
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
    ''' Base class for classes that have properties of type Attribute.
        It provides the caching mechanism and peek() and poke() methods.
        It implements the [] operator to return an AttributeRef object.
    '''
    def __init__(self):
        self.__attribute_cache = dict()               # for caching Attribute values

    def __getitem__(self, propname):
        if not propname in self.__attribute_cache:
            raise AttributeError(f"Attribute '{propname}' not found.")
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
