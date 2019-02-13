from .base import Nameable


class Object(Nameable):

    def __new__(cls, name):
        self = super(__class__, cls).__new__(cls, name)
        return self
