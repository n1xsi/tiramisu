from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_loader
import sys
import os

from transpiler import translate_tiramisu, print_traceback


class TiramisuLoader(Loader):
    """Класс для импорта файлов с рецептом в Python"""
    def __init__(self, filename):
        self.filename = filename

    def create_module(self, spec):
        return None  # Позволяем Python создать пустой модуль по умолчанию

    def exec_module(self, module):
        # Чтение рецепта из файла
        with open(self.filename, 'r', encoding='utf-8') as file:
            source_code = file.read()

        # Перевод на Python
        python_code = translate_tiramisu(source_code)
        
        # Назначение атрибутов, чтобы модуль знал свой путь
        module.__file__ = self.filename
        module.__loader__ = self

        # Исполнение кода внутри пространства имён этого модуля
        try:
            exec(python_code, module.__dict__)
        except Exception as e:
            # Если в импортируемом модуле ошибка - вывод Tiramisu-traceback'а
            source_lines = source_code.splitlines()
            print_traceback(e, self.filename, source_lines)
            # Выброс ImportError, чтобы скрипт остановился
            raise ImportError(f"📛 [Tiramisu] Failed to bake imported module '{module.__name__}'") from None


class TiramisuFinder(MetaPathFinder):
    ...
