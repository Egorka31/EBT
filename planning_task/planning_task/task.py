from .object import Object
from .predicate import Predicate
from .state import State
from .action import Action
from parsing import Parser


class Task(object):

    def __init__(self, domain_name, problem_name, objects, predicates, actions, init, goal):
        self.domain_name = domain_name
        self.problem_name = problem_name
        self._objects = dict((obj, Object(obj)) for obj in objects)
        self._predicates = dict((name, Predicate(name, args)) for (name, args) in predicates)
        self._actions = {
            Action(
                name=action[0],
                parameters=action[1][1],
                precondition=[(self._predicates[name], args, result) for (name, args, result) in action[2][1]],
                effect=action[3][1]
            ) for action in actions
        }
        self.init = {(Predicate(name, args), args) for (name, args) in init}
        self.goal = goal
        self.state = State.from_init(
            objects=self.objects,
            predicates=self.predicates,
            actions=self._actions,
            init_set=self.init
        )

    @staticmethod
    def from_parser(p: Parser):
        return Task(
            domain_name=p.domain_name,
            problem_name=p.problem_name,
            objects=p.objects,
            predicates=p.predicates,
            actions=p.actions,
            init=p.init,
            goal=p.goal
        )

    @property
    def objects(self):
        return list(self._objects.values())

    @property
    def predicates(self):
        return list(self._predicates.values())

    @property
    def actions(self):
        return list(self._actions)
