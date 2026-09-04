from dataclasses import dataclass


@dataclass
class PermissionResult:
    allowed: bool
    reason: str


class PermissionManager:
    SAFE_ACTIONS = {
        "system_info",
        "open_application",
        "list_files",
        "read_file",
        "list_processes",
        "search_and_learn",
        "get_active_window",
        "list_visible_windows",
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