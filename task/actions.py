from .base import NamedObject, BaseObject, PDDLObject


class ActionObject(BaseObject):
    def __new__(cls):
        return super(__class__, cls).__new__(cls)

    def __hash__(self):
        raise NotImplementedError


class ActionTerm(ActionObject):
    __slots__ = ('_action_functor', '_terms')

    def __new__(cls, action_functor: str, terms: tuple = ()):
        self = super(__class__, cls).__new__(cls)

        if isinstance(action_functor, ActionDef):
            return ActionTerm(action_functor.action_functor, action_functor.parameters)

        if type(action_functor) is not str:
            if type(terms) is list:
                terms = tuple(terms)
            else:
                raise TypeError('action_functor should be str.')

        self._action_functor = action_functor
        self._terms = terms

        return self

    def __str__(self):
        return self.action_functor

    def __repr__(self):
        terms = ' '.join(list(map(str, self._terms)))
        if terms:
            return f'<{self.__class__.__name__} {self._action_functor} {terms}>'
        else:
            return f'<{self.__class__.__name__} {self._action_functor}>'

    def __hash__(self):
        return hash((self._action_functor, len(self._terms)))

    def __eq__(self, other):
        return self._action_functor == other.action_functor and len(self._terms) == len(other.terms)

    @property
    def action_functor(self):
        return self._action_functor

    @property
    def terms(self):
        return self._terms


class ActionSpec(ActionObject):
    def __new__(cls):
        return super(__class__, cls).__new__(cls)

    def __hash__(self):
        raise NotImplementedError


class Series(ActionSpec):
    __slots__ = '_action_specs'

    def __new__(cls, *action_specs):
        self = super(__class__, cls).__new__(cls)

        for action_spec in action_specs:
            if not isinstance(action_spec, ActionObject):
                raise TypeError('all action specs should be ActionSpec instances.')

        self._action_specs = action_specs

        return self

    def __eq__(self, other):
        return self._action_specs == other.action_specs

    def __hash__(self):
        return hash(self._action_specs)

    @property
    def action_specs(self):
        return self._action_specs


class ActionDefBody(ActionObject):
    __slots__ = ('_precondition', '_expansion', '_effect')

    def __new__(cls, precondition=None, expansion=None, effect=None):
        self = super(__class__, cls).__new__(cls)
        self._precondition = precondition
        self._expansion = expansion
        self._effect = effect

        return self

    def __eq__(self, other):
        return self._precondition == other.precondition and \
               self._expansion == other.expansion and \
               self._effect == other.effect

    def __hash__(self):
        return hash((self._precondition, self._expansion, self._effect))

    @property
    def precondition(self):
        return self._precondition

    @property
    def expansion(self):
        return self._expansion

    @property
    def effect(self):
        return self._effect


class ActionDef(PDDLObject):
    __slots__ = ('_action_functor', '_parameters', '_action_def_body')

    def __new__(cls, action_functor: str, parameters: tuple, action_def_body: ActionDefBody):
        self = super(__class__, cls).__new__(cls)
        self._action_functor = action_functor
        self._parameters = parameters
        self._action_def_body = action_def_body

        return self

    def is_primitive(self):
        return self.action_def_body.expansion is None

    def __eq__(self, other):
        if type(other) is not ActionDef:
            return NotImplemented

        return self._action_functor == other.action_functor and \
            self._parameters == other.parameters and \
            self._action_def_body == other.action_def_body

    def __repr__(self):
        return f'<{self.__class__.__name__} {self._action_functor} params: {len(self._parameters)}>'

    def __hash__(self):
        return hash((self._action_functor, self._parameters, self._action_functor))

    @property
    def action_functor(self):
        return self._action_functor

    @property
    def parameters(self):
        return self._parameters

    @property
    def action_def_body(self):
        return self._action_def_body


class Method(ActionDef):
    __slots__ = '_name',

    def __new__(cls, action_functor: str, name=None, parameters=(), action_def_body=ActionDefBody()):
        self = super(__class__, cls).__new__(cls, action_functor, parameters, action_def_body)
        self._name = name
        return self

    @property
    def name(self):
        return self._name
