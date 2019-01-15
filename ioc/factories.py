
from typing import TypeVar

from commons.patterns import Factory
from commons.reflection import get_constructor_arguments
from ioc.core import ResourceContainer
from ioc.resources import ResourceKey, SingletonResource

T = TypeVar('T')
K = TypeVar('K')

class ComponentResource(SingletonResource[T, K]):
    """
    A Component Resource is a singleton resource that the IOC container
    will provide the factory to create it based on the class constructor.

    This sets the following limitation: each one of the constructor arguments of the target class should be
    known to the IOC container (in other words, each one of them should be registered as a resource)
    """

    def __init__(self, key: ResourceKey[K], dependencies):

        # We will use the ComponentFactory:
        factory = ComponentFactory(key.cls, key.qualifier, dependencies)

        deps_dict = factory.get_dependencies()
        deps_arr = []

        for key in deps_dict:
            deps_arr.append(deps_dict[key])

        super().__init__(key, key.cls, factory, deps_arr)


class ComponentFactory(Factory[T]):
    """
    This Factory can take any class that follow the ComponentResource rules
    and initialize it from the IOC container
    """

    def __init__(self, cls, qualifier: str, mappings: dict):
        self._cls = cls
        self._qualifier = qualifier
        self._mapping = mappings

    def get_dependencies(self):
        # First get the class's constructor:
        type_of_args = get_constructor_arguments(self._cls)

        arguments = dict()

        for key in type_of_args:
            if key in self._mapping:
                rk = ResourceKey(type_of_args[key], self._mapping[key])
            else:
                rk = ResourceKey(type_of_args[key], "")
            arguments[key] = rk

        return arguments

    def create(self) -> T:

        deps = self.get_dependencies()

        instance_of_args = dict()

        for key in deps:
            instance_of_args[key] = ResourceContainer.resolve_resource(deps[key])

        return self._cls(**instance_of_args)