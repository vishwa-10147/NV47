from app.core.events import Event
from app.tools.system_info import get_system_info


class NV001Kernel:
    def __init__(self) -> None:
        self.running = False

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

    def execute_command(self, command: str) -> None:
        command = command.strip().lower()

        if command == "system info":
            self.emit_event(
                Event(
                    event_type="TOOL_EXECUTION",
                    message="Collecting system information",
                )
            )

            result = get_system_info()

            self.emit_event(
                Event(
                    event_type="TOOL_RESULT",
                    message="System information collected",
                    data=result,
                )
            )

            for key, value in result.items():
                print(f"{key}: {value}")

        elif command == "help":
            print("Available commands:")
            print("  system info")
            print("  help")
            print("  exit")

        elif command == "exit":
            self.stop()

        else:
            print(f"Unknown command: {command}")
            print("Type 'help' to see available commands.")