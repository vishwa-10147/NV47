from app.core.events import Event, EventLogger
from app.core.tasks import Task
from app.core.tool_registry import ToolRegistry
from app.tools.system_info import get_system_info
from app.core.permissions import PermissionManager
from app.tools.open_application import open_application
from app.tools.file_tools import list_files, read_file



class NV001Kernel:
    def __init__(self) -> None:
        self.running = False
        self.tasks: list[Task] = []
        self.tools = ToolRegistry()
        self.permissions = PermissionManager()
        self.logger = EventLogger()

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
        task.mark_running()

        self.emit_event(
            Event(
                event_type="TASK_STARTED",
                message=f"Task {task.task_id} started",
            )
        )

        try:
            if task.command == "system info":
                action = "system_info"
                result = self.run_tool(
                    task=task,
                    action=action,
                )

            elif task.command.startswith("open "):
                application = task.command.removeprefix("open ").strip()
                action = "open_application"

                result = self.run_tool(
                    task=task,
                    action=action,
                    application=application,
                )

            elif task.command == "list files":
                action = "list_files"
            
                result = self.run_tool(
                    task=task,
                    action=action,
                )
            
            elif task.command.startswith("read file "):
                relative_path = task.command.removeprefix("read file ").strip()
                action = "read_file"
            
                result = self.run_tool(
                    task=task,
                    action=action,
                    relative_path=relative_path,
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
    

    def execute_command(self, command: str) -> None:
        command = command.strip().lower()

        if command == "help":
            print("Available commands:")
            print("  system info")
            print("  open notepad")
            print("  open calculator")
            print("  list files")
            print("  read file README.md")
            print("  tools")
            print("  tasks")
            print("  help")
            print("  exit")

        elif command == "tools":
            self.show_tools()

        elif command == "tasks":
            self.show_tasks()

        elif command == "exit":
            self.stop()

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

        return {
            "success": False,
            "message": f"Unsupported action: {action}",
        }