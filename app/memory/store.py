import json
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime

class MemoryStore:
    """Manages long-term and short-term memory persistence for NV001."""
    
    def __init__(self, memory_dir: str = "app/memory/data"):
        self.memory_dir = Path(memory_dir)
        self.history_file = self.memory_dir / "task_history.jsonl"
        self._setup_store()

    def _setup_store(self) -> None:
        try:
            self.memory_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Failed to create memory directory: {e}")

    def save_task_history(self, task_id: str, command: str, status: str, result: Any) -> None:
        try:
            record = {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "task_id": task_id,
                "command": command,
                "status": status,
                "result": result
            }
            log_line = json.dumps(record, default=str)
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")
        except Exception as e:
            print(f"Failed to save task history: {e}")

    def get_recent_history(self, limit: int = 5) -> List[Dict[str, Any]]:
        if not self.history_file.exists():
            return []
        
        try:
            records = []
            with open(self.history_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    records.append(json.loads(line))
            return records
        except Exception as e:
            print(f"Failed to read task history: {e}")
            return []
