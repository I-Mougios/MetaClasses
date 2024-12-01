# decorators.py
from typing import Callable, Any, Dict, TypeVar
from types import MappingProxyType

__all__ = ['Dispatcher']

T = TypeVar('T')

class Dispatcher:
    """
    A class to manage function dispatching based on the first argument passed.
    
    Attributes:
        default_function (Callable): The default function to call if no mapping matches.
        registry (Dict[Any, Callable]): A dictionary mapping values to specific functions.
    """
    def __init__(self, default_function: Callable[..., Any]):
        """
        Initialize the dispatcher with a default function.
        
        Args:
            default_function (Callable[..., T]): The default function to call when no mapping is found.
        """
        self.default_function = default_function
        self.registry: Dict[Any, Callable[..., Any]] = {}
        self.__doc__ = default_function.__doc__
        self.__name__ = default_function.__name__
       

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Dispatch to the appropriate function based on the first argument.
        
        Args:
            *args: Positional arguments to pass to the selected function.
            **kwargs: Keyword arguments to pass to the selected function.
        
        Returns:
            The result of the dispatched function.
        """
        if not args:
            raise ValueError("At least one positional argument is required for dispatching.")
        key = args[0]
        function_to_call = self.registry.get(key, self.default_function)
        return function_to_call(*args, **kwargs)

    def register(self, key: Any) -> Callable[[Callable[..., T]], Callable[..., T]]:
        """
        Decorator factory to register a function to handle a specific key.
        
        Args:
            key (Any): The key to associate with the function.
        
        Returns:
            A decorator function that registers the provided function and return the same function as it is.
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            self.registry[key] = func
            return func
        return decorator

    def get_registry(self) -> MappingProxyType:
        """
        Get an immutable view of the current function registry.
        
        Returns:
            MappingProxyType: An immutable mapping of registered keys to functions.
        """
        return MappingProxyType(self.registry)

    def get_function(self, key: Any) -> Callable[..., T]:
        """
        Retrieve the function mapped to a specific key, or the default function.
        
        Args:
            key (Any): The key to look up.
        
        Returns:
            Callable[..., Any]: The function associated with the key, or the default function.
        """
        return self.registry.get(key, self.default_function)


def instantiate_dispatcher():
    @Dispatcher
    def default(*args):
        '''This is the docstring of the default function'''
        return 'This is the default value'

    @default.register('a')
    def a(*args):
        return 'This is the function when the first argument is "a"'

    @default.register('b')
    def b(*args):
        return 'This is the function when the first argument is "b"'
    
    return default

if __name__ == '__main__':
    default = instantiate_dispatcher()
    print(default('a'), default('b'), default('x'), sep='--', end='\n'*2)
    f = default.get_function('a')
    print(f(), end='\n'*2)
    print(default.__doc__, end='\n'*2)
    print(default.__name__, end='\n'*2)
    
    
