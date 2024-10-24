import inspect
from typing import Iterable, TypeVar, Callable

R = TypeVar("R")  # Type variable for the return type
I = TypeVar("I")  # Type variable for the item type
D = TypeVar("D")  # Type variable for the default value type

def find(iter: Iterable[I], predicate: Callable[[I], bool], defaultValue: D):
    """ Returns the first value of `iter` that satisfies the `predicate`, or returns `defaultValue` if it was not found. """
    return next((item for item in iter if predicate(item)), defaultValue)

def format_function(function): 
    if not function.__name__=='<lambda>': return function.__name__
    first_line = inspect.getsourcelines(function)[0][0].strip()
    return '... ' + first_line[first_line.index(':')+1:].strip()