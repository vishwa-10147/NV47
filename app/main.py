from app.core.kernel import NV001Kernel


def main() -> None:
    import sys
    
    if "--gui" in sys.argv:
        from app.ui.desktop import start_gui
        start_gui()
        return

    kernel = NV001Kernel()
    kernel.start()

    print()
    print("NV001 command interface")
    print("Type 'help' for commands.")
    print("Run with '--gui' for the visual interface.")
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