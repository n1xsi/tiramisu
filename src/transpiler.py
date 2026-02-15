from tokenize import tokenize, untokenize, NAME
from sys import argv, exit, exc_info
from traceback import extract_tb
from io import BytesIO

# Импорт словаря
try:
    from aliases import VOCABULARY, INVERSE_VOCAB
except ImportError:
    print("❓ [Tiramisu] Error: Could not find \"aliases.py\". Is the pantry empty?")
    exit(1)


def translate_tiramisu(code_string: str) -> str:
    """
    Переводит код Tiramisu в валидный Python код, используя токенизацию.
    :param code_string: Строка с кодом на Tiramisu
    :return: Строка с кодом на Python
    """
    tokens = tokenize(BytesIO(code_string.encode('utf-8')).readline)
    result = []

    for token in tokens:
        # Замена ключевых слов Python, не затрагивая строки
        if token.type == NAME and token.string in VOCABULARY:
            result.append((token.type, VOCABULARY[token.string]))
        else:
            result.append((token.type, token.string))

    return untokenize(result).decode('utf-8')


def format_error(exception_msg: str) -> str:
    """
    Форматирует сообщение об ошибке, заменяя слова Python на Tiramisu.
    :param exception_msg: Сообщение об ошибке на Python
    """
    for py_word, tira_word in INVERSE_VOCAB.items():
        # Добавление пробелов в словах, чтобы не заменять кусок слова
        replacing_msg = exception_msg.replace(f"'{py_word}'", f"'{tira_word}'")
        result_msg = replacing_msg.replace(f" {py_word} ", f" {tira_word} ")
    return result_msg


def print_traceback(exception: str, filename: str, source_lines: str) -> None:
    """
    Печатает трассировку ошибки с контекстом Tiramisu.
    :param exception: Сообщение об ошибке на Python
    :param filename: Имя файла с кодом на Tiramisu
    :param source_lines: Строки исходного кода на Tiramisu
    """
    # Если это SyntaxError (ошибка на этапе чтения кода)
    if isinstance(exception, SyntaxError):
        print(f"\n❌ [Tiramisu] Invalid Recipe (Syntax Error)!")
        lineno = exception.lineno or 1  # Иногда line number может быть None
        print(f"   In file '{filename}', line {lineno}")

        # Вывод строки кода, где ошибка
        if lineno <= len(source_lines):
            line_content = source_lines[lineno - 1].strip()
            print(f"     > {line_content}")
            if exception.offset:  # Если есть offset, то вывод, где именно в строке ошибка
                print(f"       {' ' * (exception.offset - 1)}^")

        print(f"   Complaint: {format_error(exception.msg)}")
        return

    # Если это Runtime Error (ошибка во время выполнения кода)
    exc_type, exc_value, exc_tb = exc_info()
    print(f"\n🔥 [Tiramisu] Something went wrong while cooking ({exc_type.__name__})!")

    tb_list = extract_tb(exc_tb)  # Извлечение стека вызовов
    for frame in tb_list:  # frame: (filename, lineno, name, line_content)
        # Если ошибка в скрипте (exec даёт имя "<string>")
        if frame.filename == "<string>":
            current_file = filename
            line_num = frame.lineno
            # Взятие строки из исходного кода Tiramisu
            code_line = source_lines[line_num - 1].strip() if line_num <= len(source_lines) else "???"
            print(f"   In file '{current_file}', line {line_num}, in {frame.name}")
            print(f"     > {code_line}")
        else:
            # Ошибка внутри библиотеки Python или другого модуля
            print(f"   In external ingredient '{frame.filename}', line {frame.lineno}, in {frame.name}")
            print(f"     > {frame.line}")


def run_file(filename: str) -> None:
    """
    Запускает файл с кодом на Tiramisu.
    :param filename: Имя файла с кодом на Tiramisu
    """
    # Чтение кода из файла
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"❓ [Tiramisu] Error: Could not find recipe '{filename}'")
        return

    # Подготовка к выводу строк при ошибке
    source_lines = source_code.splitlines()

    # Транспиляция кода Tiramisu в Python
    try:
        python_code = translate_tiramisu(source_code)
    except Exception as e:
        print(f"📛 [Tiramisu] Transpiler broken (Internal Error): {e}")
        return

    # Исполнение кода на Python
    try:
        exec(python_code, globals())
    except Exception as e:
        print_traceback(e, filename, source_lines)


if __name__ == '__main__':
    if len(argv) < 2:
        print("❔ [Tiramisu] Usage: python transpiler.py <recipe.tira>")
    else:
        run_file(argv[1])
