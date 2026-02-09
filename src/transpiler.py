from tokenize import tokenize, untokenize, NAME
from sys import argv, exit
from io import BytesIO

# Импорт словаря
try:
    from aliases import VOCABULARY, INVERSE_VOCAB
except ImportError:
    print("[Tiramisu] Error: Could not find \"aliases.py\". Is the pantry empty?")
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
        exception_msg = exception_msg.replace(f"'{py_word}'", f"'{tira_word}'")
        result_msg = exception_msg.replace(f" {py_word} ", f" {tira_word} ")
    return result_msg


def run_file(filename: str) -> None:
    """
    Запускает файл с кодом на Tiramisu.
    :param filename: Имя файла с кодом на Tiramisu
    """
    with open(filename, 'r', encoding='utf-8') as file:
        source_code = file.read()

    python_code = translate_tiramisu(source_code)

    try:
        exec(python_code, globals())
    except Exception as e:
        message = format_error(str(e))
        print(f"[Tiramisu] Compiling error: {message}")


if __name__ == '__main__':
    if len(argv) < 2:
        print("[Tiramisu] Usage: python transpiler.py <recipe.tira>")
    else:
        run_file(argv[1])
