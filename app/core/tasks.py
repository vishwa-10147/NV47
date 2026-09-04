from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass
class Task:
    command: str
    task_id: str = field(default_factory=lambda: str(uuid4())[:8])
    status: str = "created"
    result: Any = None
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(
            timespec="seconds"
        )
    )

    def mark_running(self) -> None:
        self.status = "running"

    def mark_completed(self, result: Any) -> None:
        self.status = "completed"
        self.result = result

    def mark_failed(self, result: Any) -> None:
        self.status = "failed"
        self.result = result