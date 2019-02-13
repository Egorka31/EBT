class Nameable(object):
    __slots__ = ('_name', '__dict__')

    def __new__(cls, name):
        self = super(__class__, cls).__new__(cls)
        self._name = name
        return self

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self._name}>'

    def __hash__(self):
        return hash(self._name)

    @property
    def name(self):
        return self._name


class Parameterizable(Nameable):

    __slots__ = ('_parameters', '_par_dict')

    def __new__(cls, name, parameters: tuple):
        self = super(__class__, cls).__new__(cls, name)
        self._parameters = parameters
        self._par_dict = dict(zip(parameters, range(len(parameters))))
        return self

    def parameter_index(self, parameter):
        return self._par_dict.get(parameter)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f'<{self.__class__.__name__} ({self._name}, {self._parameters})>'

    @property
    def parameters_number(self):
        return len(self._parameters)
