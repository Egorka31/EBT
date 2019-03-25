from pyparsing import *
from task import Variable, Term, Type
from .parser import Parser


name = Word(alphanums + '-')

lp = Literal('(').suppress()
rp = Literal(')').suppress()

variable = (Suppress('?') + name).setParseAction(Parser.parse_class(Variable))
predicate = name.copy()

primitive_type = name.copy()
p_type = primitive_type ^ (lp + Suppress('either') + OneOrMore(primitive_type) + rp)
p_type.setParseAction(Parser.parse_class(Type))


def empty_or(x):
    return (lp + rp) ^ x


def atomic_formula(x):
    _atomic_formula = lp + predicate + Group(ZeroOrMore(x)) + rp
    _atomic_formula.setParseAction(Parser.parse_afs)
    return _atomic_formula


def typed_list(x, typed_class=None):
    _typed_list = Forward()

    atom_typed_list = OneOrMore(x.copy().setParseAction()) + Suppress('-') + p_type

    if typed_class:
        atom_typed_list.setParseAction(Parser.parse_atom_typed_by_class(typed_class))

    _typed_list << (ZeroOrMore(x) ^ (atom_typed_list + _typed_list))

    return _typed_list


def literal(t):
    return atomic_formula(t).addParseAction(Parser.parse_atomic_formula(True)) ^ \
           (lp + Suppress('not') + atomic_formula(t) + rp).setParseAction(Parser.parse_atomic_formula(False))


term = name.copy().setParseAction(Parser.parse_class(Term)) ^ variable
gd = literal(term)
pre_gd = Forward()
pre_gd << (gd ^ (lp + Suppress('and') + ZeroOrMore(pre_gd) + rp))
