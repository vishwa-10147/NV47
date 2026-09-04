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


class OllamaAdapter(ModelAdapter):
    """Integrates with a local Ollama instance for true offline LLM reasoning."""
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"

    def generate_response(self, prompt: str, context: str) -> str:
        import urllib.request
        import json
        payload = {
            "model": self.model_name,
            "prompt": f"Context: {context}\n\nUser: {prompt}\nResponse:",
            "stream": False
        }
        
        req = urllib.request.Request(self.api_url, data=json.dumps(payload).encode('utf-8'), 
                                     headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                return result.get("response", "")
        except Exception as e:
            return f"[Ollama Error] Ensure Ollama is running locally. {e}"

    def generate_tool_request(self, prompt: str, context: str) -> Optional[ToolRequest]:
        import urllib.request
        import json
        
        system_prompt = """You are NV001, an autonomous software intelligence.
Your goal is to parse the user's intent and output a strict JSON object representing a ToolRequest.
Available tools:
- system_info: arguments: {}
- list_processes: arguments: {}
- list_files: arguments: {}
- read_file: arguments: {"relative_path": "str"}
- open_application: arguments: {"application": "str"}
- search_and_learn: arguments: {"query": "str"}
- get_active_window: arguments: {}
- list_visible_windows: arguments: {}

Output ONLY valid JSON like: {"action": "system_info", "arguments": {}}
Do not wrap in markdown or add explanations.
"""
        payload = {
            "model": self.model_name,
            "system": system_prompt,
            "prompt": f"Context/Failures: {context}\n\nUser: {prompt}",
            "stream": False,
            "format": "json"
        }
        
        req = urllib.request.Request(self.api_url, data=json.dumps(payload).encode('utf-8'), 
                                     headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode())
                response_text = result.get("response", "").strip()
                
                parsed = json.loads(response_text)
                if "action" in parsed:
                    return ToolRequest(action=parsed["action"], arguments=parsed.get("arguments", {}))
        except Exception as e:
            print(f"[Ollama Error] Failed to generate valid tool request: {e}")
            
        return None


class ReasoningEngine:
    def __init__(self) -> None:
        self.adapters: Dict[str, ModelAdapter] = {
            "deterministic": DeterministicModel(),
            "ollama": OllamaAdapter(model_name="llama3")
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
