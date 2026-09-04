from dataclasses import dataclass


@dataclass
class PermissionResult:
    allowed: bool
    reason: str


class PermissionManager:
    SAFE_ACTIONS = {
        "system_info",
        "open_application",
    }

    def check(self, action: str) -> PermissionResult:
        if action in self.SAFE_ACTIONS:
            return PermissionResult(
                allowed=True,
                reason="Action is classified as safe",
            )

        return PermissionResult(
            allowed=False,
            reason="Action is not currently permitted",
        )