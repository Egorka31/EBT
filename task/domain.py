from .base import NamedObject
from .actions import ActionTerm
from .frozen_dict import FrozenDict


class Domain(NamedObject):
    __slots__ = ('_require_def', '_types_def', '_constants', '_predicates_def', '_action_defs', '_action_term_dict')

    def __new__(
            cls, name: str,
            require_def=None,
            types_def=None,
            constants=None,
            predicates_def=None,
            action_defs=None
    ):
        self = super(__class__, cls).__new__(cls, name)
        self._require_def = require_def,
        self._types_def = types_def,
        self._constants = constants
        self._predicates_def = predicates_def,
        self._action_defs = action_defs

        return self

    @property
    def require_def(self):
        return self._require_def

    @property
    def types_def(self):
        return self._types_def

    @property
    def constants(self):
        return self._constants

    @property
    def predicates_def(self):
        return self._predicates_def

    @property
    def action_defs(self):
        return self._action_defs
