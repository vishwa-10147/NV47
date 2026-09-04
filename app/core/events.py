from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Event:
    event_type: str
    message: str
    data: Any = None
    timestamp: str = ""

    def __post_init__(self) -> None:
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat(timespec="seconds")