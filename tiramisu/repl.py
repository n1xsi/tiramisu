from .transpiler import translate_tiramisu, print_traceback
from .importer import enable_import_hook

from tokenize import TokenError
import codeop
import sys
import os


def start_repl():
    """Запускает интерактивную консоль для рецептов (REPL)."""

    # Включение импортов + добавление текущей папки в пути для импорта локальнх .tira файлов прямо из консоли
    sys.path.insert(0, os.getcwd())
    enable_import_hook()

    print("🍰 Welcome to the Tiramisu REPL!")
    print("Type 'exit()' or press Ctrl+Z+Enter to leave.\n")

    env = {"__name__": "__main__"}  # Память консоли
    buffer = []  # Буфер для многострочных команд (например, функции, циклы и т.д.)
    compiler = codeop.CommandCompiler()  # Встроенный компилятор Python (завершён ли код или нет)

    while True:
        # Если буфер пустой, то это новая строка (>>>) ИНАЧЕ внутри блока (внутри taste/chef)
        # Разные приглашения для первой строки и продолжения
        prompt = "..." if buffer else ">>> "

        try:
            line = input(prompt)
        except EOFError:
            print("\nLeaving REPL... 👨‍🍳")
            break
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt! 🍳")
            buffer = []  # Очистить буфер при прерывании
            continue

        buffer.append(line)  # Добавить строку в буфер
        source_code = "\n".join(buffer)  # Собрать весь код из буфера

        # ПОПЫТКА ПЕРЕВОДА РЕЦЕПТА В PYTHON
        try:
            python_code = translate_tiramisu(source_code)
        except TokenError:
            # TokenError возникает, если скобка/кавычка открыта, но не закрыта:
            # в таком случае просто ожидание следующей строки.
            continue
        except Exception as e:
            print(f"📛 [Tiramisu] Transpiler Error: {e}")
            buffer = []
            continue

        # ПОПЫТКА КОМПИЛИРОВАНИЯ ПЕРЕВЕДЁННОГО КОДА
        try:
            code_object = compiler(python_code, "<console>", "single")
        except SyntaxError as e:
            print_traceback(e, "<console>", source_code.splitlines())
            buffer = []
            continue

        if code_object is None:
            # Ввод не завершён (например, открытая функция или цикл), ждём продолжения ИЛИ клавиши Enter
            continue

        # ВЫПОЛНЕНИЕ КОДА ИЗ БУФЕРА
        try:
            exec(code_object, env)
        except SystemExit:
            print("\nLeaving REPL... 👨‍🍳")
            break
        except Exception as e:
            print_traceback(e, "<console>", source_code.splitlines())

        buffer = []  # Очистить буфер после успешного выполнения
