import inspect
from collections import OrderedDict


def get_constructor(cls):
    return inspect.signature(cls.__init__)


# noinspection PyProtectedMember
def get_constructor_arguments(cls):

    constructor = get_constructor(cls)

    arguments = OrderedDict()  # Should be a positional array
    for arg in constructor.parameters:
        if arg is not "self":
            arguments[arg] = constructor.parameters[arg]._annotation

    return arguments
