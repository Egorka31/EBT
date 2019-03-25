from .basic import *
from .requirements import require_def


object_declaration = lp + Suppress(':objects') + typed_list(name) + rp
init = lp + Suppress(':init') + Group(ZeroOrMore(literal(name))) + rp
goal = lp + Suppress(':goal') + Group(pre_gd) + rp

problem = lp + Suppress('define') + lp + Suppress('problem') + name + rp + lp + Suppress(':domain') + name + rp + \
          Group(Optional(require_def)) + Group(Optional(object_declaration)) + init + goal + rp
problem.setParseAction(Parser.parse_problem)
