from .types import TypedObject


class Term(TypedObject):

    def __new__(cls, name: str, p_type=None):
        return super(__class__, cls).__new__(cls, name, p_type)

    def __str__(self):
        return f'{self.name} - {str(self.type)}'


class Variable(Term):

    def __new__(cls, name: str, p_type=None):
        return super(__class__, cls).__new__(cls, name, p_type)

    def __str__(self):
        return f'?{self.name} - {str(self.type)}'
