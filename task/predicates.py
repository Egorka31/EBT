from .base import NamedObject


class Predicate(NamedObject):
    __slots__ = '_terms'

    def __new__(cls, name: str, terms: list):
        self = super(__class__, cls).__new__(cls, name)

        self._terms = terms

        return self

    def __hash__(self):
        return hash((self._name, self._terms))

    @property
    def terms(self):
        return self._terms

    def __str__(self):
        terms = ' '.join(map(str, self._terms))
        return rf"{self._name} {terms}"

    def __repr__(self):
        return rf"<{self.__class__.__name__} {str(self)}>"
