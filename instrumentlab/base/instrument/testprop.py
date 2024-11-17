
class testprop:
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

        print(":init:", self)

    def __set_name__(self, owner, name):
        # print("__set_name__", owner, name)
        self.__name__ = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            print("__get_noobj__", self)
            return self
        if self.fget is None:
            raise AttributeError
        value = self.fget(obj)
        print("__get__", self.__name__, value)
        obj._cache_value(self.__name__, value)
        return value

    def __set__(self, obj, value):
        print("__set__", self.__name__, value)
        if self.fset is None:
            raise AttributeError
        obj._cache_value(self.__name__, value)
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError
        self.fdel(obj)

    def getter(self, fget):
        print(":getter:",self)
        # print(fget)
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        print(":setter:",self)
        # print(fset)
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        print(":deleter:",self)
        return type(self)(self.fget, self.fset, fdel, self.__doc__)
    