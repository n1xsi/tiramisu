from .transpiler import run_file, translate_tiramisu
import argparse


def main():
    # ------------------ Парсер команд ------------------
    parser = argparse.ArgumentParser(
        description="🍰 Tiramisu Compiler",
        prog="tiramisu"
    )

    # Флаг версии (tiramisu -v)
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    # ------------------ Подменю для команд ------------------
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Команда RUN (Подготовить и запустить файл)
    run_parser = subparsers.add_parser("run", help="Run a .tira file")
    run_parser.add_argument("file", help="Path to the .tira recipe file")

    # Считывание аргументов командной строки
    args = parser.parse_args()

    # Выполнение логики по команде
    if args.command == "run":
        run_file(args.file)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
