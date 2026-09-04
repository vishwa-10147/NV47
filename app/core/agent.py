from typing import List
from app.core.tasks import Task
from app.core.reasoning import ToolRequest

class AutonomousAgent:
    """Manages multi-step autonomous execution, planning, and self-reflection."""
    
    def __init__(self, kernel):
        # We pass kernel dynamically to avoid circular imports
        self.kernel = kernel

    def run_autonomous_loop(self, goal: str) -> None:
        print(f"\n[Autonomous Agent] Starting multi-step execution for goal: '{goal}'")
        
        plan = self._generate_plan(goal)
        
        if not plan:
            print("[Autonomous Agent] Could not generate a multi-step plan for this goal.")
            return

        print(f"[Autonomous Agent] Generated plan with {len(plan)} steps.")
        
        for i, request in enumerate(plan):
            step_num = i + 1
            print(f"\n--- Executing Step {step_num}: {request.action} ---")
            
            # Phase 8 Self-Evolving check
            recent_history = self.kernel.memory.get_recent_history(limit=10)
            failed_tasks = [h['command'] for h in recent_history if h['status'] == 'failed']
            
            if request.action in failed_tasks:
                print(f"[Self-Reflection] Aborting step. Action '{request.action}' repeatedly failed in recent memory.")
                print("[Autonomous Agent] Plan halted to prevent cyclic failure.")
                break
            
            # Map request back to kernel compatible command
            command_str = request.action
            if request.action == "open_application":
                command_str = f"open {request.arguments.get('application', 'notepad')}"
            elif request.action == "search_and_learn":
                command_str = f"search {request.arguments.get('query', 'technology')}"
            
            task = self.kernel.create_task(command_str)
            self.kernel.execute_task(task)
            
            if task.status == "failed":
                print(f"[Autonomous Agent] Step {step_num} failed. Halting autonomous execution.")
                break
            
            print(f"[Autonomous Agent] Step {step_num} completed successfully.")
            
        print("\n[Autonomous Agent] Autonomous loop finished.")

    def _generate_plan(self, goal: str) -> List[ToolRequest]:
        goal_lower = goal.lower()
        plan = []
        
        # Hardcoded deterministic plans for Phase 9 testing
        if "research" in goal_lower and "quantum" in goal_lower:
            plan.append(ToolRequest(action="search_and_learn", arguments={"query": "quantum computing"}))
            plan.append(ToolRequest(action="get_active_window", arguments={})) # Verify state
        elif "inspect system" in goal_lower or "diagnostics" in goal_lower:
            plan.append(ToolRequest(action="system_info", arguments={}))
            plan.append(ToolRequest(action="list_processes", arguments={}))
            plan.append(ToolRequest(action="list_visible_windows", arguments={}))
            
        return plan
