from app.core.events import Event
from app.core.tasks import Task
from app.core.tool_registry import ToolRegistry
from app.tools.system_info import get_system_info


class NV001Kernel:
    def __init__(self) -> None:
        self.running = False
        self.tasks: list[Task] = []
        self.tools = ToolRegistry()

        self.register_tools()

    def register_tools(self) -> None:
        self.tools.register(
            name="system_info",
            description="Collects information about the current computer",
            function=get_system_info,
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
                result = self.tools.execute("system_info")
                task.mark_completed(result)

                self.emit_event(
                    Event(
                        event_type="TASK_COMPLETED",
                        message=f"Task {task.task_id} completed",
                        data=result,
                    )
                )

                for key, value in result.items():
                    print(f"{key}: {value}")

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