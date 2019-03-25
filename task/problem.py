from .base import NamedObject


class Problem(NamedObject):
    __slots__ = ('_domain','_require_def', '_object_declaration', '_init', '_goal')

    def __new__(
            cls, name: str,
            domain=None,
            require_def=None,
            object_declaration=None,
            init=None,
            goal=None
    ):
        self = super(__class__, cls).__new__(cls, name)
        self._domain = domain
        self._require_def = require_def,
        self._object_declaration = object_declaration,
        self._init = init
        self._goal = goal

        return self

    @property
    def domain(self):
        return self._domain

    @property
    def require_def(self):
        return self._require_def

    @property
    def object_declaration(self):
        return self._object_declaration

    @property
    def init(self):
        return self._init

    @property
    def goal(self):
        return self._goal


