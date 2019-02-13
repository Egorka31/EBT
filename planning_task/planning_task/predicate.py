from .base import Parameterizable


class Predicate(Parameterizable):

    def __new__(cls, name, parameters):
        self = super(__class__, cls).__new__(cls, name, parameters)
        return self
