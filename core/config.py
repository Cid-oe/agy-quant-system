import os
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SystemConfig:
    environment: str
    log_level: str
    db_uri: str
    plugins: List[str]
    custom: Dict[str, Any]

class ConfigLoader:
    @staticmethod
    def load(path: str = "config.json") -> SystemConfig:
        return SystemConfig(
            environment=os.getenv("AGY_ENV", "production"),
            log_level=os.getenv("AGY_LOG_LEVEL", "INFO"),
            db_uri=os.getenv("AGY_DB_URI", "sqlite:///:memory:"),
            plugins=["plugins.slack_notifier"],
            custom={"max_queue_size": 10000}
        )
