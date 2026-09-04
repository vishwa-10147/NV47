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
        
        if "system" in prompt_lower or "info" in prompt_lower:
            return ToolRequest(action="system_info", arguments={})
        
        if "process" in prompt_lower:
            return ToolRequest(action="list_processes", arguments={})
            
        if "file" in prompt_lower and "list" in prompt_lower:
            return ToolRequest(action="list_files", arguments={})
            
        if "notepad" in prompt_lower or "calculator" in prompt_lower:
            app = "notepad" if "notepad" in prompt_lower else "calculator"
            return ToolRequest(action="open_application", arguments={"application": app})

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
