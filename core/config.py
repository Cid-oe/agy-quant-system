import os
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class SystemConfig:
    environment: str = "paper"      # Default: paper. Never production without explicit config.
    log_level: str = "INFO"
    db_uri: str = "sqlite:///:memory:"
    plugins: List[str] = field(default_factory=list)
    custom: Dict[str, Any] = field(default_factory=dict)

class ConfigLoader:
    @staticmethod
    def load(path: str = "config.json") -> SystemConfig:
        if os.path.exists(path):
            with open(path, "r") as f:
                return SystemConfig(**json.load(f))
        return SystemConfig()
