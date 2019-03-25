import abc


class BaseObject(abc.ABC):
    __slots__ = '__dict__'

    def __new__(cls):
        self = super(__class__, cls).__new__(cls)
        return self

    @abc.abstractmethod
    def __hash__(self):
        raise NotImplementedError


class PDDLObject(BaseObject):
    def __new__(cls):
        self = super(__class__, cls).__new__(cls)
        return self

    @abc.abstractmethod
    def __repr__(self):
        raise NotImplementedError


class NamedObject(PDDLObject):
    __slots__ = '_name'

    def __new__(cls, name: str):
        self = super(__class__, cls).__new__(cls)

        if not isinstance(name, str):
            raise TypeError('name should be str')

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


class BaseMany(PDDLObject):
    __slots__ = ('_class', '_instances')

    def __new__(cls, *instances, instances_class=None):
        self = super(__class__, cls).__new__(cls)

        self._class = instances_class

        if not self._class:
            self._class = instances[0].__class_

        for instance in instances:
            if instance.__class__ is not self._class:
                raise TypeError('all instances should be the same class')

        self._instances = instances

        return self

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __getitem__(self, item):
        return self._instances[item]

    def __len__(self):
        return len(self._instances)

    def __hash__(self):
        return hash((self.__class__, len(self._instances)))

    def __repr__(self):
        return f'<{self.__class__.__name__}: {len(self._instances)}>'
