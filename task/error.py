class TaskException(Exception):
    pass


class VariablesException(TaskException):
    pass


class PredicateException(TaskException):
    pass


class BaseManyException(TaskException):
    pass


class ActionException(TaskException):
    pass


class GoalDescriptionException(TaskException):
    pass


class TypesException(TaskException):
    pass
