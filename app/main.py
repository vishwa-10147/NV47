from app.core.kernel import NV001Kernel


def main() -> None:
    kernel = NV001Kernel()
    kernel.start()

    print()
    print("NV001 command interface")
    print("Type 'help' for commands.")
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