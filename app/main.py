from app.core.kernel import NV001Kernel


def main() -> None:
    import sys
    
    if "--gui" in sys.argv:
        from app.gui.main import start_gui
        start_gui()
        return
        
    if "--web" in sys.argv:
        from app.ui.web_server import start_web_server
        start_web_server()
        return

    kernel = NV001Kernel()
    kernel.start()

    print()
    print("NV001 command interface")
    print("Type 'help' for commands.")
    print("Run with '--gui' for the Desktop GUI (PySide6).")
    print("Run with '--web' for the Advanced Modern Web Dashboard.")
    print()

    while kernel.running:
        try:
            command = input("NV001 > ")
            kernel.execute_command(command)
        except KeyboardInterrupt:
            print()
            kernel.stop()
        except Exception as error:
            print(f"Runtime error: {error}")


if __name__ == "__main__":
    main()