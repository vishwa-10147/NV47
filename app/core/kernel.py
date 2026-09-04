from app.core.events import Event
from app.core.logger import EventLogger
from app.core.tasks import Task
from app.core.tool_registry import ToolRegistry
from app.core.permissions import PermissionManager
from app.core.reasoning import ReasoningEngine
from app.memory.store import MemoryStore
from app.tools.system_info import get_system_info
from app.tools.open_application import open_application
from app.tools.file_tools import list_files, read_file
from app.tools.process_tools import list_processes
from app.tools.web_tools import search_and_learn



class NV001Kernel:
    def __init__(self) -> None:
        self.running = False
        self.tasks: list[Task] = []
        self.tools = ToolRegistry()
        self.permissions = PermissionManager()
        self.logger = EventLogger()
        self.reasoning = ReasoningEngine()
        self.memory = MemoryStore()

        self.register_tools()

    def register_tools(self) -> None:
        self.tools.register(
            name="system_info",
            description="Collects information about the current computer",
            function=get_system_info,
        )
        self.tools.register(
            name="open_application",
            description="Opens an approved Windows application",
            function=open_application,
        )
        self.tools.register(
            name="list_files",
            description="Lists files inside the NV001 project directory",
            function=list_files,
        )

        self.tools.register(
            name="read_file",
            description="Reads a UTF-8 text file inside the NV001 project directory",
            function=read_file,
        )
        self.tools.register(
            name="list_processes",
            description="Lists currently running processes on the system",
            function=list_processes,
        )
        self.tools.register(
            name="search_and_learn",
            description="Searches the web for a given query and stores extracted knowledge",
            function=search_and_learn,
        )
        
    def start(self) -> None:
        self.running = True

        self.emit_event(
            Event(
                event_type="SYSTEM_STARTED",
                message="NV001 kernel started",
            )
        )

    def stop(self) -> None:
        self.running = False

        self.emit_event(
            Event(
                event_type="SYSTEM_STOPPED",
                message="NV001 kernel stopped",
            )
        )

    def emit_event(self, event: Event) -> None:
        print(
            f"[{event.timestamp}] "
            f"{event.event_type}: "
            f"{event.message}"
        )
        self.logger.log(event)

    def create_task(self, command: str) -> Task:
        task = Task(command=command)
        self.tasks.append(task)

        self.emit_event(
            Event(
                event_type="TASK_CREATED",
                message=f"Task {task.task_id} created",
                data={
                    "task_id": task.task_id,
                    "command": command,
                },
            )
        )

        return task
    def execute_task(self, task: Task) -> None:
        for dep_id in task.dependencies:
            dep_task = next((t for t in self.tasks if t.task_id == dep_id), None)
            if dep_task and dep_task.status != "completed":
                print(f"Task {task.task_id} deferred: waiting on dependency {dep_id}")
                return

        task.mark_running()

        self.emit_event(
            Event(
                event_type="TASK_STARTED",
                message=f"Task {task.task_id} started",
            )
        )

        try:
            if task.command in ("system info", "system_info"):
                action = "system_info"
                result = self.run_tool(
                    task=task,
                    action=action,
                )

            elif task.command.startswith("open ") or task.command == "open_application":
                if task.command == "open_application":
                    # For a real implementation, we'd pull arguments from the Task directly,
                    # but for now we default to notepad if arguments are missing in this branch
                    application = "notepad"
                else:
                    application = task.command.removeprefix("open ").strip()
                action = "open_application"

                result = self.run_tool(
                    task=task,
                    action=action,
                    application=application,
                )

            elif task.command in ("list files", "list_files"):
                action = "list_files"
            
                result = self.run_tool(
                    task=task,
                    action=action,
                )
            
            elif task.command.startswith("read file ") or task.command == "read_file":
                if task.command == "read_file":
                    relative_path = "README.md"
                else:
                    relative_path = task.command.removeprefix("read file ").strip()
                action = "read_file"
            
                result = self.run_tool(
                    task=task,
                    action=action,
                    relative_path=relative_path,
                )

            elif task.command in ("list processes", "list_processes"):
                action = "list_processes"
                result = self.run_tool(
                    task=task,
                    action=action,
                )

            elif task.command.startswith("search "):
                query = task.command.removeprefix("search ").strip()
                action = "search_and_learn"
                result = self.run_tool(
                    task=task,
                    action=action,
                    query=query,
                )

            else:
                task.mark_failed("Unknown command")

                self.emit_event(
                    Event(
                        event_type="TASK_FAILED",
                        message=f"Task {task.task_id} failed",
                        data="Unknown command",
                    )
                )

                print("Unknown command.")
                print("Type 'help' to see available commands.")
                return

            if result.get("success", True):
                task.mark_completed(result)

                self.emit_event(
                    Event(
                        event_type="TASK_COMPLETED",
                        message=f"Task {task.task_id} completed",
                        data=result,
                    )
                )
            else:
                task.mark_failed(result)

                self.emit_event(
                    Event(
                        event_type="TASK_FAILED",
                        message=f"Task {task.task_id} failed",
                        data=result,
                    )
                )

            print(result)

        except Exception as error:
            task.mark_failed(str(error))

            self.emit_event(
                Event(
                    event_type="TASK_FAILED",
                    message=f"Task {task.task_id} failed",
                    data=str(error),
                )
            )

            print(f"Task failed: {error}")

        if task.status == "failed" and task.can_retry():
            print(f"Retrying task {task.task_id} ({task.retries + 1}/{task.max_retries})...")
            task.increment_retry()
            self.execute_task(task)
        elif task.status in ("completed", "failed"):
            self.memory.save_task_history(
                task_id=task.task_id,
                command=task.command,
                status=task.status,
                result=task.result
            )
    

    def execute_command(self, command: str) -> None:
        command = command.strip().lower()

        if command == "help":
            print("Available commands:")
            print("  system info")
            print("  open notepad")
            print("  open calculator")
            print("  list files")
            print("  read file README.md")
            print("  list processes")
            print("  search <query>")
            print("  tools")
            print("  tasks")
            print("  history")
            print("  show logs")
            print("  help")
            print("  exit")

        elif command == "tools":
            self.show_tools()

        elif command == "tasks":
            self.show_tasks()
            
        elif command == "history":
            self.show_history()

        elif command in ("logs", "show logs"):
            self.show_logs()

        elif command == "exit":
            self.stop()

        elif command.startswith("goal "):
            goal_text = command.removeprefix("goal ").strip()
            tool_request = self.reasoning.process_goal(goal_text)
            
            if tool_request:
                print(f"Goal understood. Recommended action: {tool_request.action}")
                task = self.create_task(command)
                task.command = tool_request.action # override with structured action temporarily
                self.execute_task(task)
            else:
                print("Could not map goal to a known safe tool request.")

        elif command:
            task = self.create_task(command)
            self.execute_task(task)

    def show_tools(self) -> None:
        print("Registered tools:")

        for name, description in self.tools.list_tools().items():
            print(f"  {name}: {description}")

    def show_tasks(self) -> None:
        if not self.tasks:
            print("No tasks have been created.")
            return

        for task in self.tasks:
            print(
                f"{task.task_id} | "
                f"{task.command} | "
                f"{task.status}"
            )

    def show_logs(self) -> None:
        logs = self.logger.read_logs()
        if not logs:
            print("No logs found.")
            return
        
        print("Recent logs:")
        for log in logs:
            print(log.strip())
            
    def show_history(self) -> None:
        history = self.memory.get_recent_history()
        if not history:
            print("No task history found.")
            return
            
        print("Recent Task History:")
        for record in history:
            print(f"[{record['timestamp']}] Task {record['task_id']} | {record['command']} | Status: {record['status']}")
    def run_tool(
        self,
        task: Task,
        action: str,
        **kwargs,
    ) -> dict:
        permission = self.permissions.check(action)

        self.emit_event(
            Event(
                event_type="PERMISSION_CHECK",
                message=permission.reason,
                data={
                    "action": action,
                    "allowed": permission.allowed,
                },
            )
        )

        if not permission.allowed:
            return {
                "success": False,
                "message": permission.reason,
            }

        self.emit_event(
            Event(
                event_type="TOOL_EXECUTION",
                message=f"Executing tool: {action}",
                data=kwargs,
            )
        )

        if action == "system_info":
            return {
                "success": True,
                "data": self.tools.execute("system_info"),
            }

        if action == "open_application":
            return self.tools.execute(
                "open_application",
                **kwargs,
            )

        if action == "list_files":
            return self.tools.execute("list_files")

        if action == "read_file":
            return self.tools.execute(
                "read_file",
                **kwargs,
            )

        if action == "list_processes":
            return self.tools.execute("list_processes")

        if action == "search_and_learn":
            return self.tools.execute(
                "search_and_learn",
                **kwargs,
            )

        return {
            "success": False,
            "message": f"Unsupported action: {action}",
        }