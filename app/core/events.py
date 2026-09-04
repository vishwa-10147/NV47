import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
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


class EventLogger:
    def __init__(self, log_dir: str = "logs") -> None:
        self.log_dir = Path(log_dir)
        self.log_file = self.log_dir / "events.jsonl"
        self._setup_logger()

    def _setup_logger(self) -> None:
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Failed to create log directory: {e}")

    def log(self, event: Event) -> None:
        try:
            event_dict = asdict(event)
            log_line = json.dumps(event_dict, default=str)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")
        except Exception as e:
            print(f"Failed to log event to file: {e}")