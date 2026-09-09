import asyncio
from core.config import ConfigLoader, SystemConfig
from core.logging import SystemLogger
from core.events import EventBus
from core.registry import ProviderRegistry
from core.plugins import PluginLoader

async def bootstrap():
    config = ConfigLoader.load()
    logger = SystemLogger(config)
    bus = EventBus(logger)
    registry = ProviderRegistry()
    
    registry.register(SystemConfig, config)
    registry.register(SystemLogger, logger)
    registry.register(EventBus, bus)
    
    plugin_loader = PluginLoader(registry, bus, logger)
    plugin_loader.load_all(config.plugins)
    
    bus_task = asyncio.create_task(bus.start())
    logger.info("agy_infrastructure_online", status="ready")
    
    await asyncio.gather(bus_task)

if __name__ == "__main__":
    try:
        asyncio.run(bootstrap())
    except KeyboardInterrupt:
        print("Shutting down AGY system...")
