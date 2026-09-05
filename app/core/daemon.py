import threading
import time
from typing import Callable, List

class ScheduledTask:
    def __init__(self, interval_seconds: int, action: Callable, name: str):
        self.interval_seconds = interval_seconds
        self.action = action
        self.name = name
        self.last_run = 0

class BackgroundDaemon:
    """Runs continuously in the background to execute scheduled or event-driven tasks."""
    def __init__(self, kernel):
        self.kernel = kernel
        self.running = False
        self.tasks: List[ScheduledTask] = []
        self.thread = None

    def add_task(self, interval_seconds: int, command: str, name: str = None):
        if not name:
            name = f"AutoTask '{command}'"
            
        def action():
            print(f"\n[Daemon] Waking up to execute: {name}")
            # Inject into the kernel's normal flow seamlessly
            task = self.kernel.create_task(command)
            self.kernel.execute_task(task)
            
            # Send update to Web UI if active
            self._notify_web_ui(task)
            
        self.tasks.append(ScheduledTask(interval_seconds, action, name))
        print(f"[Daemon] Registered task '{name}' to run every {interval_seconds}s.")

    def _notify_web_ui(self, task):
        # We push updates to the memory queue so the web dashboard sees the background action
        if hasattr(self.kernel, 'semantic_memory') and self.kernel.semantic_memory:
            pass # Already saved by kernel execute_task
            
    def start(self):
        if self.running: return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print("[Daemon] Background watcher started. Awaiting scheduled events...")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("[Daemon] Background watcher stopped.")

    def _run_loop(self):
        while self.running:
            current_time = time.time()
            for task in self.tasks:
                if current_time - task.last_run >= task.interval_seconds:
                    task.action()
                    task.last_run = current_time
            time.sleep(1) # Sleep to prevent CPU thrashing
