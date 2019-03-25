from .basic import *
from .parser import Parser
from task import Variable

action_functor = name.copy()

action_term = lp + action_functor + Group(ZeroOrMore(term)) + rp
action_term.setParseAction(Parser.parse_action_term)

action_spec = Forward()
action_spec << (action_term ^ (lp + Suppress('series') +
                               ZeroOrMore(action_spec) + rp).setParseAction(Parser.parse_series))

p_effect = literal(term)
effect = p_effect ^ (lp + Suppress('and') + ZeroOrMore(p_effect) + rp)

action_symbol = name
action_def_body = Group(Optional(Suppress(':precondition') + empty_or(pre_gd))) + \
                  Group(Optional(Suppress(':expansion') + action_spec)) + \
                  Group(Optional(Suppress(':effect') + empty_or(effect)))
action_def_body.setParseAction(Parser.parse_action_def_body)

action_def = lp + Suppress(':action') + action_symbol + \
             Suppress(':parameters') + lp + Group(typed_list(variable, Variable)) + rp + \
             action_def_body + rp
action_def.setParseAction(Parser.parse_action_def)


method_def = lp + Suppress(':method') + action_functor + Group(Optional(Suppress(':name') + name)) + \
             Suppress(':parameters') + lp + Group(typed_list(variable, Variable)) + rp + \
             action_def_body + rp
method_def.setParseAction(Parser.parse_method_def)
