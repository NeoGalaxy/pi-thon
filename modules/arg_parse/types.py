"""
Définis des types pour le parseur
"""

class NonNegInt(int):
    """A none negative int"""
    def __new__(cls, *args, **kargs):
        number = int.__new__(cls, *args, **kargs)
        if number < 0 :
            raise ValueError('This should not be a negative number.')
        return number

class PositiveInt(NonNegInt):
    """A none negative int"""
    def __new__(cls, *args, **kargs):
        number = NonNegInt.__new__(cls, *args, **kargs)
        if number == 0 :
            raise ValueError('This should be a positive number.')
        return number

class NonNegFloat(float):
    """A none negative float"""
    def __new__(cls, *args, **kargs):
        number = float.__new__(cls, *args, **kargs)
        if number < 0 :
            raise ValueError('This should not be a negative number.')
        return number

class PositiveFloat(NonNegFloat):
    """A none negative float"""
    def __new__(cls, *args, **kargs):
        number = NonNegFloat.__new__(cls, *args, **kargs)
        if number == 0 :
            raise ValueError('This should be a positive number.')
        return number
