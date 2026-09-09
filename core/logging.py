import json
import logging
from .config import SystemConfig

class SystemLogger:
    def __init__(self, config: SystemConfig):
        self.level = getattr(logging, config.log_level.upper(), logging.INFO)
        logging.basicConfig(level=self.level, format="%(message)s")
        self.logger = logging.getLogger("AGY-Core")

    def info(self, event: str, **kwargs):
        self._log(logging.INFO, event, kwargs)

    def error(self, event: str, error: Exception, **kwargs):
        kwargs["error"] = str(error)
        self._log(logging.ERROR, event, kwargs)

    def _log(self, level: int, event: str, metadata: dict):
        log_entry = json.dumps({"event": event, "metadata": metadata})
        self.logger.log(level, log_entry)
