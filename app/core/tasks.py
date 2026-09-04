from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional
from uuid import uuid4


@dataclass
class Task:
    command: str
    task_id: str = field(default_factory=lambda: str(uuid4())[:8])
    status: str = "created"
    result: Any = None
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )
    dependencies: List[str] = field(default_factory=list)
    retries: int = 0
    max_retries: int = 3
    timeout_seconds: Optional[int] = None
    verified: bool = False

    def mark_running(self) -> None:
        self.status = "running"

    def mark_completed(self, result: Any) -> None:
        self.status = "completed"
        self.result = result

    def mark_failed(self, result: Any) -> None:
        self.status = "failed"
        self.result = result

    def can_retry(self) -> bool:
        return self.retries < self.max_retries

    def increment_retry(self) -> None:
        self.retries += 1
        self.status = "created"

    def verify(self, success: bool) -> None:
        self.verified = success