import importlib
from typing import List, Protocol
from .registry import ProviderRegistry
from .events import EventBus
from .logging import SystemLogger

class PluginProtocol(Protocol):
    def initialize(self, registry: ProviderRegistry, bus: EventBus) -> None: ...

class PluginLoader:
    def __init__(self, registry: ProviderRegistry, bus: EventBus, logger: SystemLogger):
        self.registry = registry
        self.bus = bus
        self.logger = logger

    def load_all(self, plugin_paths: List[str]):
        for path in plugin_paths:
            try:
                module = importlib.import_module(path)
                plugin: PluginProtocol = getattr(module, "Plugin")()
                plugin.initialize(self.registry, self.bus)
                self.logger.info("plugin_loaded", plugin=path)
            except Exception as e:
                self.logger.error("plugin_load_failed", e, plugin=path)
