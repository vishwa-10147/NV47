from collections.abc import Callable
from typing import Any


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(
        self,
        name: str,
        description: str,
        function: Callable[..., Any],
    ) -> None:
        self._tools[name] = {
            "description": description,
            "function": function,
        }

    def list_tools(self) -> dict[str, str]:
        return {
            name: tool["description"]
            for name, tool in self._tools.items()
        }

    def has_tool(self, name: str) -> bool:
        return name in self._tools

    def execute(self, name: str, **kwargs: Any) -> Any:
        if not self.has_tool(name):
            raise ValueError(f"Tool not found: {name}")

        tool_function = self._tools[name]["function"]
        return tool_function(**kwargs)