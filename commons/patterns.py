
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar, Optional

T = TypeVar('T')
K = TypeVar('K')


class Function(Generic[T, K]):
    """
    An abstract definition of a function. A Function takes an input, does its processing and returns an output.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def apply(self, params: Optional[T]) -> Optional[K]:
        """
        Executes the function's purpose on a certain input.
        :param params: the input of the function.
        :return: the output of the function.
        """
        raise NotImplementedError()


class Factory(Generic[T]):
    """
    In Factory pattern, we create object without exposing the creation logic to the client and refer to newly created
    object using a common interface.
    """
    __metaclass__ = ABCMeta

    def create(self) -> T:
        """ Will return a new instance of the object """
        raise NotImplementedError()


"""
In Strategy pattern, we create objects which represent various strategies and a context object whose behavior 
varies as per its strategy object. The strategy object changes the executing algorithm of the context object. 
"""
Strategy: Function = Function[T, K]
