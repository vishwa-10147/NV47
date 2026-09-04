import json
from pathlib import Path
from dataclasses import asdict
from app.core.events import Event


class EventLogger:
    def __init__(self, log_dir: str = "app/logs") -> None:
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

    def read_logs(self, limit: int = 10) -> list[str]:
        if not self.log_file.exists():
            return []
        
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                return lines[-limit:]
        except Exception as e:
            print(f"Failed to read logs: {e}")
            return []
