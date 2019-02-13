from itertools import product
from .frozen_dict import FrozenDict


class State(object):

    __slots__ = ('_objects', '_predicates', '_predicate_dict', '_actions')

    def __new__(cls, objects, predicates, actions, predicate_dict=None):
        self = super(__class__, cls).__new__(cls)

        self._objects = frozenset(objects)
        self._predicates = frozenset(predicates)
        self._predicate_dict = predicate_dict

        if not self._predicate_dict:
            self._predicate_dict = FrozenDict(
                (
                    p,
                    FrozenDict((obj, False)for obj in set(product(self._objects, repeat=p.parameters_number)))
                ) for p in self._predicates
            )

        return self

    def validate_predicate(self, predicate, attributes):
        if predicate not in self._predicate_dict.keys():
            raise Exception(f'There is not predicate {predicate}')

        if attributes not in self._predicate_dict.get(predicate).keys():
            raise Exception(f'Predicate {predicate} can not get attributes {attributes}')

    @staticmethod
    def from_init(objects, predicates, actions, init_set):
        init_predicate_dict = dict((p, dict((obj, False)
                                            for obj in set(product(objects, repeat=p.parameters_number))))
                                   for p in predicates)

        for (predicate, attributes) in init_set:
            if predicate in init_predicate_dict and attributes in init_predicate_dict[predicate]:
                init_predicate_dict[predicate][attributes] = True

        return State(objects, predicates, actions, predicate_dict=FrozenDict(init_predicate_dict))

    def _change_results(self, changes: set):
        new_predicate_dict = self._predicate_dict.to_dict()

        for (predicate, attributes, result) in changes:
            self.validate_predicate(predicate, attributes)
            new_predicate_dict[predicate][attributes] = result

        self._predicate_dict = FrozenDict(new_predicate_dict)

    def get_result(self, predicate, attributes):
        self.validate_predicate(predicate, attributes)
        return self._predicate_dict.get(predicate).get(attributes)

    def is_action_enabled(self, action, attributes):
        for (predicate, parameters, result) in action.precondition:
            if self.get_result(
                    predicate, tuple(map(lambda p: attributes[action.parameter_index(p)], parameters))
            ) != result:
                return False
        return True

    def apply_action(self, action, attributes):
        if self.is_action_enabled(action, attributes):
            self._apply_action(action, attributes)
        else:
            raise Exception('Can not apply action due to precondition non-compliance')

    def _apply_action(self, action, attributes):
        for (predicate, parameters, result) in action.effect:
            self._change_results({(
                predicate, tuple(map(lambda p: attributes[action.parameter_index(p)], parameters)), result
            )})

    @property
    def objects(self):
        return self._objects

    @property
    def predicates(self):
        return self._predicates

    @property
    def predicate_dict(self):
        return self._predicate_dict
