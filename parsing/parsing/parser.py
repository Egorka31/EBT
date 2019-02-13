import re


def match_pattern(pattern: str, expression: str):
    match = re.match(re.compile(pattern), expression)

    if not match:
        raise Exception(f'Can not resolve expression: {expression}')

    return tuple(match.groups())


def split_by_parentheses(expression):
    result = ['']
    balance = 0
    for s in expression:
        result[-1] += s

        if s == '(':
            balance += 1
        elif s == ')':
            balance -= 1

            if balance == 0:
                result.append('')

    return result[:-1]


class Parser(object):
    NAME_PATTERN_NC = r'[\w?-]+'
    NAME_PATTERN_C = rf'({NAME_PATTERN_NC})'

    ARGUMENT_PATTERN_NC = rf'{NAME_PATTERN_NC}'
    ARGUMENT_PATTERN_C = rf'{NAME_PATTERN_C}'

    ARGUMENTS_PATTERN_NC = rf'(?:\s*{ARGUMENT_PATTERN_NC}\s*)+'

    PREDICATE_PATTERN_NC = rf'\s*\(\s*{NAME_PATTERN_NC}\s*{ARGUMENTS_PATTERN_NC}\)\s*'
    PREDICATE_PATTERN_C = rf'\s*\(\s*({NAME_PATTERN_NC})\s*({ARGUMENTS_PATTERN_NC})\)\s*'

    PREDICATES_PATTERN_NC = rf'\s*\(:predicates\s*(?:\s*{PREDICATE_PATTERN_NC}\s*)+\)\s*'
    PREDICATES_PATTERN_C = rf'\s*\(:predicates\s*((?:\s*{PREDICATE_PATTERN_NC}\s*)+)\)\s*'

    PARAMETERS_PATTERN_NC = rf':parameters\s*\({ARGUMENTS_PATTERN_NC}\)'
    PARAMETERS_PATTERN_C = rf':parameters\s*\(({ARGUMENTS_PATTERN_NC})\)'

    POS_CLAIM_C = rf'({PREDICATE_PATTERN_NC})'
    NEG_CLAIM_NC = rf'\s*\(\s*not\s*{PREDICATE_PATTERN_NC}\s*\)\s*'
    NEG_CLAIM_C = rf'\s*\(\s*not\s*({PREDICATE_PATTERN_NC})\s*\)\s*'
    CLAIM_NC = rf'(?:{PREDICATE_PATTERN_NC}|{NEG_CLAIM_NC})'
    CLAIM_C = rf'({PREDICATE_PATTERN_NC}|{NEG_CLAIM_NC})'

    CONDITION_PATTERN_NC = rf'\s*\(\s*and\s*(?:\s*{CLAIM_NC}\s*)+\)'
    CONDITION_PATTERN_C = rf'\s*\(\s*and\s*((?:\s*{CLAIM_NC}\s*)+)\)'

    PRECONDITION_PATTERN_NC = rf':precondition\s*{CONDITION_PATTERN_NC}'
    PRECONDITION_PATTERN_C = rf':precondition\s*({CONDITION_PATTERN_NC})'

    EFFECT_PATTERN_NC = rf':effect\s*{CONDITION_PATTERN_NC}'
    EFFECT_PATTERN_C = rf':effect\s*({CONDITION_PATTERN_NC})'

    ACTION_PATTERN_NC = rf'\s*\(\s*:action\s+{NAME_PATTERN_NC}\s+{PARAMETERS_PATTERN_NC}\s+' \
        rf'{PRECONDITION_PATTERN_NC}\s+{EFFECT_PATTERN_NC}\)\s*'
    ACTION_PATTERN_C = rf'\s*\(\s*:action\s+{NAME_PATTERN_C}\s+({PARAMETERS_PATTERN_NC})\s+' \
        rf'({PRECONDITION_PATTERN_NC})\s+({EFFECT_PATTERN_NC})\)\s*'

    DOMAIN_PATTERN_NC = rf'\(\s*domain\s*{NAME_PATTERN_NC}\)\s*'
    DOMAIN_PATTERN_C = rf'\(\s*domain\s*{NAME_PATTERN_C}\)'

    DOMAIN_DEFINE_PATTERN_C = rf'\s*\(\s*define\s*({DOMAIN_PATTERN_NC})\s*({PREDICATES_PATTERN_NC})' \
        rf'((?:\s*{ACTION_PATTERN_NC}\s*)+)\)\s*'

    PROBLEM_PATTERN_NC = rf'\(\s*problem\s*{NAME_PATTERN_NC}\)\s*'
    PROBLEM_PATTERN_C = rf'\(\s*problem\s*{NAME_PATTERN_C}\)'

    PROBLEM_DOMAIN_PATTERN_NC = rf'\(\s*:domain\s*{NAME_PATTERN_NC}\)\s*'
    PROBLEM_DOMAIN_PATTERN_C = rf'\(\s*:domain\s*{NAME_PATTERN_C}\)'

    OBJECTS_PATTERN_NC = rf'\s*\(:objects\s*{ARGUMENTS_PATTERN_NC}\s*\)\s*'
    OBJECTS_PATTERN_C = rf'\s*\(:objects\s*({ARGUMENTS_PATTERN_NC})\)\s*'

    INIT_PATTERN_NC = rf'\s*\(:init\s*(?:\s*{PREDICATE_PATTERN_NC}\s*)+\)\s*'
    INIT_PATTERN_C = rf'\s*\(:init\s*((?:\s*{PREDICATE_PATTERN_NC}\s*)+)\)\s*'

    GOAL_PATTERN_NC = rf'\s*\(\s*:goal\s*{CONDITION_PATTERN_NC}\s*\)\s*'
    GOAL_PATTERN_C = rf'\s*\(\s*:goal\s*({CONDITION_PATTERN_NC})\s*\)\s*'

    PROBLEM_DEFINE_PATTERN_C = rf'\s*\(\s*define\s*({PROBLEM_PATTERN_NC})\s*({PROBLEM_DOMAIN_PATTERN_NC})\s*' \
        rf'({OBJECTS_PATTERN_NC})\s*({INIT_PATTERN_NC})\s*({GOAL_PATTERN_NC})'

    def __init__(self, domain, problem):
        self._domain = domain
        self._problem = problem

        self.domain_name = None
        self.problem_name = None
        self.problem_domain_name = None
        self.predicates = None
        self.actions = None
        self.objects = None
        self.init = None
        self.goal = None

    def parse(self):
        self._parse_domain()
        self._parse_problem()

    def _parse_domain(self):
        domain_section, predicates_section, action_section = match_pattern(Parser.DOMAIN_DEFINE_PATTERN_C, self._domain)

        self._parse_domain_section(domain_section)
        self._parse_predicate_section(predicates_section)
        self._parse_action_section(action_section)

    def _parse_domain_section(self, expression):
        self.domain_name = match_pattern(Parser.DOMAIN_PATTERN_C, expression)[0]

    def _parse_predicate_section(self, expression):
        predicates = split_by_parentheses(match_pattern(Parser.PREDICATES_PATTERN_C, expression)[0])
        self.predicates = tuple(self._parse_predicate(predicate) for predicate in predicates)

    def _parse_predicate(self, expression):
        name, args = match_pattern(Parser.PREDICATE_PATTERN_C, expression)
        return name, self._parse_args(args)

    def _parse_args(self, args):
        args = args.split()
        return tuple(self._parse_arg(arg) for arg in args)

    def _parse_arg(self, expression):
        return match_pattern(Parser.ARGUMENT_PATTERN_C, expression)[0]

    def _parse_action_section(self, expression):
        actions = split_by_parentheses(expression)
        self.actions = tuple(self._parse_action(action) for action in actions)

    def _parse_action(self, expression):
        name, parameters, precondition, effect = match_pattern(Parser.ACTION_PATTERN_C, expression)
        return (
            name,
            self._parse_parameters(parameters),
            self._parse_precondition(precondition),
            self._parse_effect(effect)
        )

    def _parse_parameters(self, expression):
        args = match_pattern(Parser.PARAMETERS_PATTERN_C, expression)[0]
        return 'parameters', self._parse_args(args)

    def _parse_precondition(self, expression):
        condition = match_pattern(Parser.PRECONDITION_PATTERN_C, expression)[0]
        return 'precondition', self._parse_condition(condition)

    def _parse_effect(self, expression):
        effect = match_pattern(Parser.EFFECT_PATTERN_C, expression)[0]
        return 'effect', self._parse_condition(effect)

    def _parse_condition(self, expression):
        claims = split_by_parentheses(match_pattern(Parser.CONDITION_PATTERN_C, expression)[0])
        return tuple(self._parse_claim(claim) for claim in claims)

    def _parse_claim(self, expression):
        if re.match(re.compile(Parser.NEG_CLAIM_C), expression):
            name, args = self._parse_predicate(match_pattern(Parser.NEG_CLAIM_C, expression)[0])
            return name, args, False

        if re.match(re.compile(Parser.POS_CLAIM_C), expression):
            name, args = self._parse_predicate(match_pattern(Parser.POS_CLAIM_C, expression)[0])
            return name, args, True

        raise Exception(f'Can not resolve claim {expression}')

    def _parse_problem(self):
        problem_section, domain_section, object_section, init_section, goal_section \
            = match_pattern(Parser.PROBLEM_DEFINE_PATTERN_C, self._problem)

        self._parse_problem_section(problem_section)
        self._parse_problem_domain_section(domain_section)
        self._parse_object_section(object_section)
        self._parse_init_section(init_section)
        self._parse_goal_section(goal_section)

    def _parse_problem_section(self, expression):
        self.problem_name = match_pattern(Parser.PROBLEM_PATTERN_C, expression)[0]

    def _parse_problem_domain_section(self, expression):
        self.problem_domain_name = match_pattern(Parser.PROBLEM_DOMAIN_PATTERN_C, expression)[0]

    def _parse_object_section(self, expression):
        objs = match_pattern(Parser.OBJECTS_PATTERN_C, expression)[0]
        self.objects = tuple(objs.split())

    def _parse_init_section(self, expression):
        predicates = split_by_parentheses(match_pattern(Parser.INIT_PATTERN_C, expression)[0])
        self.init = tuple(self._parse_predicate(predicate) for predicate in predicates)

    def _parse_goal_section(self, expression):
        condition = match_pattern(Parser.GOAL_PATTERN_C, expression)[0]
        self.goal = self._parse_condition(condition)
