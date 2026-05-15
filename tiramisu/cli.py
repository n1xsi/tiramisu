from importlib.metadata import version, PackageNotFoundError
import argparse

from .transpiler import run_file, translate_tiramisu
from .repl import start_repl


def get_version() -> str:
    """Получает версию пакета из метаданных (pyproject.toml)."""
    try:
        return version("tiramisu-lang")
    except PackageNotFoundError:
        # Если запускают скрипт напрямую, без установки через pip
        return "dev-unknown"


def main():
    # ------------------ Парсер команд ------------------
    parser = argparse.ArgumentParser(
        description="🍰🤎 Tiramisu Compiler - how it works:",
        prog="tiramisu"
    )

    # Флаг версии (tiramisu -v)
    current_version = get_version()
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {current_version}"
    )

    # ------------------ Подменю для команд ------------------
    # dest="command" означает, что args.command будет содержать имя команды (run, show, repl и т.д.)
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Команда RUN (Подготовить и запустить файл)
    run_parser = subparsers.add_parser("run", help="Run a .tira file")
    run_parser.add_argument("file", help="Path to the .tira recipe file")

    # Команда SHOW
    show_parser = subparsers.add_parser("show", help="Show the raw Python recipe without running")
    show_parser.add_argument("file", help="Path to the .tira recipe file")

    # Команда REPL
    repl_parser = subparsers.add_parser("repl", help="Start the interactive Tiramisu console")

    # Считывание аргументов командной строки
    args = parser.parse_args()

    # ------------------ Логика маршрутизации команд ------------------
    match args.command:
        case "run":
            run_file(args.file)
        case "show":
            try:
                with open(args.file, 'r', encoding='utf-8') as file:
                    code = file.read()
                print("🐍 Translated Python Recipe 🐍\n")
                print(translate_tiramisu(code))
            except FileNotFoundError:
                print(f"❓ [Tiramisu] Error: Could not find recipe '{args.file}'")
        case "repl":
            start_repl()
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
