
from abc import ABCMeta
from typing import TypeVar, Generic, Dict, Optional, Type, List

from commons.patterns import Factory

T = TypeVar('T')  # Just a generic typed variable.
K = TypeVar('K')  # Just a generic typed variable.


class ResourceKey(Generic[K]):
    """
    This class gives shape to all future keys of resources
    """

    def __init__(self, cls: Type[K], qualifier: str = ""):
        self._cls = cls
        self.qualifier = qualifier

    @property
    def cls(self) -> K:
        return self._cls

    @property
    def class_name(self) -> str:
        return self._cls.__name__

    def to_string(self) -> str:
        return "{0}_{1}".format(self._cls.__name__, self.qualifier)


class Resource(Generic[T, K]):
    """
    This class represents a resource (in an IOC context), a resource can be any injectable object.
    For example: a list of email accounts can be a resource of type array with qualifier "email_accounts".
    For example: a database repository can be a resource of type Repository with qualifier "my_repository".

    So basically, the IOC container holds a dictionary of Resources (and its subclasses)
    """
    __metadata__ = ABCMeta

    def __init__(self, key: ResourceKey[K], value: Optional[T], dependencies: List = None):
        self._key = key
        self._value = value

        if dependencies is None:
            # If this resource has no dependencies, init it to empty dict:
            self._dependencies = []
        else:
            self._dependencies = dependencies

    @property
    def key(self):
        """ Gets the key of the resource """
        return self._key

    @property
    def value(self):
        """ Gets the value of the resource """
        return self._value


class SingletonResource(Resource[T, K]):
    """
    This pattern involves a single class which is responsible to create an object while making sure that only single
    object gets created. This class provides a way to access its only object which can be accessed directly without
    need to instantiate the object of the class.

    This resource takes a factory that can create the actual underlying component (the _value), when someone asks
    for the value of this resource it will lazy load the underlying component and assure that each call will return the same
    object (e.g singleton)
    """

    def __init__(self, key: ResourceKey[K], cls: Type[T], factory: Factory, dependencies: List = None):
        super().__init__(key, None, dependencies)
        self._factory = factory
        self._cls = cls

    @property
    def value(self):
        if self._value is None:
            # If the resource is not initialized, use the factory to init it:
            self._value = self._factory.create()

        return self._value


class FactoryResource(Resource[T, K]):
    """
    Works like the SingletonResource, but will return a new instance for each .value call
    """

    def __init__(self, key: ResourceKey[K], cls: Type[T], factory: Factory, dependencies: List = None):
        super().__init__(key, None, dependencies)
        self._factory = factory
        self._cls = cls

    @property
    def value(self):
        return self._factory.create()
