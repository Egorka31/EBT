from .base import PDDLObject, BaseMany
from .predicates import Predicate
from .error import GoalDescriptionException


class AtomicFormula(PDDLObject):
    __slots__ = ('_predicate', '_state')

    def __new__(cls, predicate: Predicate, state: bool):
        self = super(__class__, cls).__new__(cls)

        if not isinstance(predicate, Predicate):
            raise TypeError(f'bad operand type for {self.__class__.__name__}(): {predicate.__class__.__name__}')

        if not isinstance(state, bool):
            raise TypeError(f'bad operand type for {self.__class__.__name__}(): {state.__class__.__name__}')

        self._predicate = predicate
        self._state = state

        return self

    def __eq__(self, other):
        return self.predicate == other.predicate and self.state == other.state

    def __repr__(self):
        return f'<{self.__class__.__name__} {str(self._predicate)}, state: {self._state}>'

    def __hash__(self):
        return hash((self._predicate, self._state))

    @property
    def predicate(self):
        return self._predicate

    @property
    def state(self):
        return self._state


class GoalDescription(BaseMany):

    def __new__(cls, *atomic_formulas):
        try:
            if len(atomic_formulas) == 1:
                if isinstance(atomic_formulas[0], GoalDescription):
                    return atomic_formulas[0]

            self = super(__class__, cls).__new__(cls, atomic_formulas, instances_class=AtomicFormula)
        except TypeError:
            raise GoalDescriptionException(f'all objects should be AtomicFormula instances')
        else:
            return self
