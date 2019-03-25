from .base import NamedObject, BaseMany
from .error import TypesException


class PrimitiveType(NamedObject):

    def __new__(cls, name=None):

        if name:
            if isinstance(name, PrimitiveType):
                return name

            self = super(__class__, cls).__new__(cls, name)
        else:
            self = super(__class__, cls).__new__(cls, 'object')

        return self


class Type(BaseMany):

    def __new__(cls, *types):
        try:
            if not types:
                return Type(PrimitiveType())
            if len(types) == 1:
                if isinstance(types[0], Type):
                    return types[0]

            self = super(__class__, cls).__new__(cls, *map(PrimitiveType, types), instances_class=PrimitiveType)
        except TypeError:
            raise TypesException(f'all objects should be PrimitiveType instances')
        else:
            return self

    def __repr__(self):
        if len(self) == 1:
            return f'<{self.__class__.__name__}: {self[0].name}>'
        else:
            types = ' '.join(map(lambda t: t.name, self._instances))
            return f'<{self.__class__.__name__}: (either {types})>'

    def __str__(self):
        if len(self) == 1:
            return self[0].name
        else:
            types = ' '.join(map(lambda t: t.name, self._instances))
            return f'(either {types})'


class TypesDef(BaseMany):

    def __new__(cls, *types):
        try:
            self = super(__class__, cls).__new__(cls, *types, instances_class=Type)
        except TypeError:
            raise TypesException(f'all objects should be Type instances')
        else:
            return self


class TypedObject(NamedObject):
    __slots__ = '_type'

    def __new__(cls, name: str, p_type=None):
        self = super(__class__, cls).__new__(cls, name)
        self._type = Type(p_type)

        return self

    def __str__(self):
        return f'{self.name} - {str(self.type)}'

    def __repr__(self):
        return f'<{self.__class__.__name__}: {str(self)}>'

    @property
    def type(self):
        return self._type

