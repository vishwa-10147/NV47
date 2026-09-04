from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ToolRequest:
    action: str
    arguments: Dict[str, Any]


class ModelAdapter:
    """Base interface for models to ensure replaceable components."""
    def generate_response(self, prompt: str, context: str) -> str:
        raise NotImplementedError
        
    def generate_tool_request(self, prompt: str, context: str) -> Optional[ToolRequest]:
        raise NotImplementedError


class DeterministicModel(ModelAdapter):
    """A deterministic, rule-based model to satisfy testing and offline requirements."""
    def generate_response(self, prompt: str, context: str) -> str:
        return f"Acknowledged: {prompt}"
        
    def generate_tool_request(self, prompt: str, context: str) -> Optional[ToolRequest]:
        prompt_lower = prompt.lower()
        
        # Self-Evolving Check: Read failures from context
        failed_actions = []
        if "Recent failed commands:" in context:
            if "system_info" in context: failed_actions.append("system_info")
            if "list_files" in context: failed_actions.append("list_files")
            if "open_application" in context: failed_actions.append("open_application")
        
        action = None
        args = {}
        
        if "system" in prompt_lower or "info" in prompt_lower:
            action = "system_info"
        elif "process" in prompt_lower:
            action = "list_processes"
        elif "file" in prompt_lower and "list" in prompt_lower:
            action = "list_files"
        elif "notepad" in prompt_lower or "calculator" in prompt_lower:
            app = "notepad" if "notepad" in prompt_lower else "calculator"
            action = "open_application"
            args = {"application": app}
        elif "see" in prompt_lower or "window" in prompt_lower:
            action = "get_active_window"

        if action:
            if action in failed_actions:
                print(f"\n[Self-Reflection] I remember '{action}' failed recently. As a self-evolving system, I should try an alternative strategy, but my rules are currently limited.")
            return ToolRequest(action=action, arguments=args)

        return None


class ReasoningEngine:
    def __init__(self) -> None:
        self.adapters: Dict[str, ModelAdapter] = {
            "deterministic": DeterministicModel()
        }
        self.active_adapter = "deterministic"

    def set_adapter(self, name: str) -> None:
        if name in self.adapters:
            self.active_adapter = name

    def process_goal(self, goal: str, context: str = "") -> Optional[ToolRequest]:
        adapter = self.adapters.get(self.active_adapter)
        if not adapter:
            return None
        return adapter.generate_tool_request(prompt=goal, context=context)
