from .base import BaseObject
from .domain import Domain
from .actions import ActionTerm, ActionDef, Series
import itertools


class ActionTree(BaseObject):
    __slots__ = ('_action_term', '_sub_actions')

    def __new__(cls, action_term=None, sub_actions=()):
        self = super(__class__, cls).__new__(cls)
        self._action_term = action_term
        self._sub_actions = sub_actions
        return self

    def ground(self):
        if not self._sub_actions:
            return [self.action_term]

        return list(itertools.chain(*[sub.ground() for sub in self._sub_actions]))

    def __repr__(self):
        return f'<{self.__class__.__name__} {self._action_term.action_functor} subs: {len(self._sub_actions)}>'

    @property
    def action_term(self):
        return self._action_term

    @property
    def sub_actions(self):
        return self._sub_actions

    def __hash__(self):
        raise NotImplementedError


class HierarchicalTaskNetwork(object):

    def __init__(self, domain: Domain):
        super(__class__, self).__init__()
        self._domain = domain
        self._action_term_dict = None
        self._action_tree = dict()

    def construct_tree(self):
        self._action_term_dict = dict([
            (ActionTerm(action), action) for action in self._domain.action_defs
        ])
        for action in self._domain.action_defs:
            self.recursive_tree(ActionTerm(action))

    def recursive_tree(self, action_term):
        action_tree = self._action_tree.get(action_term)

        if not action_tree:
            action = self.action_by_term(action_term)
            if action.is_primitive():
                action_tree = ActionTree(action_term)
            else:
                expansion = self._expand_action(action)
                action_tree = ActionTree(
                    action_term,
                    tuple(self.recursive_tree(sub) for sub in expansion)
                )
            self._action_tree[action_term] = action_tree

        return action_tree

    def action_by_term(self, action_term):
        return self._action_term_dict.get(action_term)

    def action_tree(self, action_term):
        return self._action_tree.get(action_term)

    def ground_action(self, action):
        action_term = ActionTerm(action)

        if type(action_term) is not ActionTerm:
            raise TypeError('action_term should be ActionTerm instance.')

        action_tree = self.action_tree(action_term)
        if not action_tree:
            raise ValueError(f"Action term '{action_term}' not found")

        return action_tree.ground()

    @staticmethod
    def _expand_action(action: ActionDef):
        expansion = action.action_def_body.expansion
        if isinstance(expansion, Series):
            return expansion.action_specs
        else:
            # Not implemented for other action specs
            return []

    @property
    def domain(self):
        return self._domain
