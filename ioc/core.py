
from typing import TypeVar

from commons.errors import QualifierNotFound
from ioc.factories import ComponentResource
from ioc.resources import Resource, ResourceKey

T = TypeVar('T')


class ResourceContainer:
    """
    One of the biggest issues in software systems today is managing the dependencies between objects. If my
    ProcessOrdersService class is using the OrdersDAL and CustomersDAL classes, it has dependencies on them and,
    through them, each of their dependencies. Unmanaged, those dependencies can get out of control without you even
    noticing. If you have ever changed a constructor signature and realized that you have just broken your code in 19
    places, or ever tried to instantiate an object only to find that it needs the environment just so because of a
    dependency three levels down, you know the pain that I am describing. Inversion of Control and Dependency
    Injection are two related ways to break apart dependencies in your applications. They are explained in detail by
    Martin Fowler in his article Inversion of Control Containers and the Dependency Injection Pattern,
    but a few lines are in order. Inversion of Control (IoC) means that objects do not create other objects on which
    they rely to do their work. Instead, they get the objects that they need from an outside source (for example,
    an xml configuration file). Dependency Injection (DI) means that this is done without the object intervention,
    usually by a framework component that passes constructor parameters and set properties.

    The Resource Container holds all of our managed components.
    """
    _resources = dict()

    @staticmethod
    def add_resource(resource: Resource):

        # If not exists, create new entry:
        if resource.key.class_name not in ResourceContainer._resources:
            ResourceContainer._resources[resource.key.class_name] = dict()

        # Add the resource qualifier entry:
        ResourceContainer._resources[resource.key.class_name][resource.key.qualifier] = resource

    @staticmethod
    def get_resource(key: ResourceKey) -> Resource:

        # Check if the class is registered in the first level dict:
        if key.class_name in ResourceContainer._resources:

            # Check if the qualifier exists:
            if key.qualifier in ResourceContainer._resources[key.class_name]:

                # Found it, lets return it to the caller:
                return ResourceContainer._resources[key.class_name][key.qualifier]

            else:  # Qualifier not found
                raise QualifierNotFound(
                    "Cannot find qualifier {0} for class {1}.".format(key.qualifier, key.class_name))
        else:  # Class not found
            raise QualifierNotFound("Cannot found component of class {0}.".format(key.class_name))

    @staticmethod
    def resolve_resource(key: ResourceKey[T]) -> T:
        return ResourceContainer.get_resource(key).value

    @staticmethod
    def clear_all():

        # For each key in the first level:
        for key1 in ResourceContainer._resources:
            # For each key in the second level:
            for key2 in ResourceContainer._resources[key1]:
                try:
                    del ResourceContainer._resources[key1][key2]
                except:
                    pass
            try:
                del ResourceContainer._resources[key1]
            except:
                pass

        ResourceContainer._resources = dict()


class Ioc:
    @staticmethod
    def component(qualifier: str = "", resources=[]):
        def class_wrapper(cls):
            def args_wrapper(*args, **kwargs):
                component = ComponentResource(ResourceKey(cls, qualifier), resources)
                ResourceContainer.add_resource(component)
                pass

            return args_wrapper
        return class_wrapper
