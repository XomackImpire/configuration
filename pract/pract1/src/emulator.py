import shlex

class ShellEmulator:

    def __init__(self, vfs):
        self.vfs = vfs
        self.last_error = False

    def execute(self, command_line, output):
        self.last_error = False
        try:
            parts = shlex.split(command_line)
        except ValueError as error:
            self.last_error = True
            output(f"Ошибка разбора команды: {error}")
            return True

        if not parts:
            return True

        command, *args = parts
        if command == "exit":
            if args:
                self.last_error = True
                output("Ошибка: команда exit не принимает аргументы.")
                return True
            output("Завершение работы.")
            return False

        if command in ("ls", "cd"):
            output(f"{command}: {' '.join(args)}" if args else command)
            return True

        self.last_error = True
        output(f"Ошибка: неизвестная команда «{command}».")
        return True