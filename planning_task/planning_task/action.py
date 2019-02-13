from .base import Parameterizable


class Action(Parameterizable):

    __slots__ = ('_precondition', '_effect')

    def __new__(cls, name, parameters, precondition, effect):
        self = super(__class__, cls).__new__(cls, name, parameters)
        self._precondition = precondition
        self._effect = effect
        return self

    @property
    def precondition(self):
        return self._precondition

    @property
    def effect(self):
        return self._effect
