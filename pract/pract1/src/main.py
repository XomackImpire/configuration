import argparse
import getpass
import socket
import sys
import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path

from emulator import ShellEmulator
from vfs import load_vfs


def parse_args():
    parser = argparse.ArgumentParser(
        description="Графический эмулятор командной оболочки"
    )
    parser.add_argument("--vfs", default="vfs/default.xml",
                        help="путь к XML-файлу виртуальной файловой системы")
    parser.add_argument("--prompt", default="vfs$ ",
                        help="приглашение перед вводом команды")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    return parser.parse_args()


class EmulatorGUI:

    def __init__(self, root, emulator, prompt):
        self.root = root
        self.emulator = emulator
        self.prompt = prompt
        self.root.title(
            f"Эмулятор — [{getpass.getuser()}@{socket.gethostname()}]"
        )
        self.root.geometry("800x520")
        self.output = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 10)
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        bottom = tk.Frame(root)
        bottom.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.entry = tk.Entry(bottom, font=("Consolas", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.on_enter)
        tk.Button(bottom, text="Выполнить", command=self.on_enter).pack(
            side=tk.LEFT, padx=(8, 0)
        )
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.write("Эмулятор запущен. Доступные команды: ls, cd, exit.")
        self.write("Команды ls и cd на этапах 1–3 работают как заглушки.")
        self.show_prompt()
        self.entry.focus_set()

    def write(self, text):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, str(text) + "\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def show_prompt(self):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, self.prompt)
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def on_enter(self, event=None):
        command_line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.write(command_line)
        should_continue = self.emulator.execute(command_line, self.write)
        if should_continue:
            self.show_prompt()
        else:
            self.close()

    def run_script(self, script_path):
        path = Path(script_path)
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as error:
            self.write(f"Ошибка чтения стартового скрипта: {error}")
            return
        self.write(f"Запуск стартового скрипта: {path}")
        had_error = False
        for line_number, line in enumerate(lines, start=1):
            command_line = line.strip()
            if not command_line or command_line.startswith("#"):
                continue
            self.write(self.prompt + command_line)
            try:
                success = self.emulator.execute(command_line, self.write)
            except Exception as error:
                success = True
                self.write(f"Ошибка в строке {line_number}: {error}")
            if not success:
                break
            if self.emulator.last_error:
                had_error = True
                self.write("Стартовый скрипт остановлен из-за ошибки.")
                break
        if had_error:
            self.write("Стартовый скрипт завершён с ошибками.")
        else:
            self.write("Стартовый скрипт завершён.")

    def close(self):
        self.root.destroy()

def main():
    args = parse_args()
    print("Параметры запуска:")
    print(f"  VFS: {args.vfs}")
    print(f"  Приглашение: {args.prompt!r}")
    print(f"  Стартовый скрипт: {args.script or 'не задан'}")

    try:
        vfs = load_vfs(args.vfs)
    except (OSError, ValueError) as error:
        print(f"Ошибка загрузки VFS: {error}", file=sys.stderr)
        vfs = {"type": "directory", "name": "/", "children": []}

    emulator = ShellEmulator(vfs)
    root = tk.Tk()
    app = EmulatorGUI(root, emulator, args.prompt)
    if args.script:
        root.after(150, lambda: app.run_script(args.script))
    root.mainloop()


if __name__ == "__main__":
    main()