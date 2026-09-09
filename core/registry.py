from typing import Type, TypeVar, Dict, Any

T = TypeVar('T')

class ProviderRegistry:
    def __init__(self):
        self._providers: Dict[Type, Any] = {}

    def register(self, interface: Type[T], implementation: T):
        self._providers[interface] = implementation

    def resolve(self, interface: Type[T]) -> T:
        implementation = self._providers.get(interface)
        if not implementation:
            raise KeyError(f"No provider registered for {interface.__name__}")
        return implementation
