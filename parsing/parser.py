from task import *
from .error import *


class Parser(object):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(__class__, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._requirements = set()

    def require(self, requirement: str):
        self._requirements |= {requirement}

    @staticmethod
    def parse_domain(tokens):
        try:
            name, require_def, types_def, constants, predicates_def, action_defs = tokens
        except Exception as e:
            raise ParsingException(f'can not resolve {tokens} while parsing domain.')

        return Domain(name, require_def, types_def, constants, predicates_def, action_defs)

    @staticmethod
    def parse_problem(tokens):
        try:
            name, domain, require_def, object_declaration, init, goal = tokens
        except Exception as e:
            raise ParsingException(f'can not resolve {tokens} while parsing problem.')

        return Problem(name, domain, require_def, object_declaration, init, goal)

    @staticmethod
    def parse_atom_typed_by_class(typed_class):
        Parser().require('typing')

        def parse_atom_typed(tokens):
            objs = tokens[:-1]
            p_type = tokens[-1]
            return [typed_class(obj, p_type) for obj in objs]
        return parse_atom_typed

    @staticmethod
    def parse_afs(tokens):
        try:
            name, terms = tokens
        except Exception as e:
            raise ParsingException(f'can not resolve {tokens} while parsing afs.')

        return Predicate(name, terms)

    @staticmethod
    def parse_atomic_formula(state: bool):
        def parse_af(tokens):
            try:
                (predicate,) = tokens
            except Exception:
                raise ParsingException(f'can not resolve {tokens} while parsing atomic formula.')

            return AtomicFormula(predicate, state)
        return parse_af

    @staticmethod
    def parse_class(cls: type):
        def parse_class(tokens):
            try:
                obj = cls(*tokens)
            except Exception:
                raise ParsingException(f'can not resolve {tokens} while parsing {cls.__name__}.')

            return obj
        return parse_class

    @staticmethod
    def parse_action_def(tokens):
        try:
            action_functor, parameters, action_def_body = tokens
        except Exception:
            raise ParsingException(f'can not resolve {tokens} while parsing action-def.')

        return ActionDef(action_functor, parameters, action_def_body)

    @staticmethod
    def parse_action_term(tokens):
        try:
            action_functor, terms = tokens
        except Exception:
            raise ParsingException(f'can not resolve {tokens} while parsing action-def.')

        return ActionTerm(action_functor, terms.asList())

    @staticmethod
    def parse_series(tokens):
        action_specs = tokens
        return Series(*action_specs)

    @staticmethod
    def parse_action_def_body(tokens):
        try:
            precondition, expansion, effect = tokens
        except Exception:
            raise ParsingException(f'can not resolve {tokens} while parsing action-def.')
        if expansion:
            return ActionDefBody(precondition.asList(), expansion[0], effect.asList())
        else:
            return ActionDefBody(precondition=precondition.asList(), effect=effect.asList())

    @staticmethod
    def parse_method_def(tokens):
        try:
            action_functor, name, parameters, action_def_body = tokens
        except Exception:
            raise ParsingException(f'can not resolve {tokens} while parsing action-def.')
        if name:
            return Method(action_functor, name[0], parameters.asList(), action_def_body)
        else:
            return Method(
                action_functor=action_functor,
                parameters=parameters.asList(),
                action_def_body=action_def_body
            )
