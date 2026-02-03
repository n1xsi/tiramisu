from tokenize import tokenize, untokenize, NAME
from io import BytesIO
from sys import argv

# Словарь перевода (алиасы)
VOCABULARY = {
    # Струкртура и функции
    'pie': 'class',

    # Логика и циклы
    'taste': 'if',

    # Типы данных и значения
    'bake': 'print',

    # Операторы
    'sour': 'not'
}


def translate_tiramisu(code_string: str) -> str:
    """
    Переводит код Tiramisu в валидный Python код, используя токенизацию.
    :param code_string: Строка с кодом на Tiramisu
    :return: Строка с кодом на Python
    """
    tokens = tokenize(BytesIO(code_string.encode('utf-8')).readline)
    result = []

    for token in tokens:
        token_type = token.type
        token_string = token.string

        # Замена только имён (переменных, ключевых слов), а не строк
        if token_type == NAME and token_string in VOCABULARY:
            result.append((token_type, VOCABULARY[token_string]))
        else:
            result.append((token_type, token_string))

    return untokenize(result).decode('utf-8')


def run_file(filename: str) -> None:
    """
    Запускает файл с кодом на Tiramisu.
    :param filename: Имя файла с кодом на Tiramisu
    """
    with open(filename, 'r', encoding='utf-8') as file:
        source_code = file.read()

    python_code = translate_tiramisu(source_code)

    try:
        exec(python_code)
    except Exception as e:
        print(f"Tiramisu compiling error: {e}")


if __name__ == '__main__':
    if len(argv) < 2:
        print("Usage: python tiramisu.py <filename.tira>")
    else:
        run_file(argv[1])
