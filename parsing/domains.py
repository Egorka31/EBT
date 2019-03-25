from .basic import *
from .requirements import require_def
from .actions import action_def
from .parser import Parser, Variable

atomic_formula_skeleton = lp + predicate + Group(typed_list(variable, Variable)) + rp
atomic_formula_skeleton.setParseAction(Parser.parse_afs)

predicates_def = lp + Suppress(':predicates') + OneOrMore(atomic_formula_skeleton) + rp

constants_def = lp + Suppress(':constants') + typed_list(name) + rp

types_def = lp + Suppress(':types') + typed_list(name) + rp

structure_def = action_def

domain = lp + Suppress('define') + lp + Suppress('domain') + name + rp + \
         Group(Optional(require_def)) + Group(Optional(types_def)) + Group(Optional(constants_def)) + \
         Group(Optional(predicates_def)) + Group(ZeroOrMore(structure_def)) + rp
domain.setParseAction(Parser.parse_domain)
