from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_loader
import sys
import os


class TiramisuLoader(Loader):
    """Класс для импорта .tira-файлов с рецептом в Python"""

    def __init__(self, filename):
        self.filename = filename

    def create_module(self, spec):
        return None  # Позволяем Python создать пустой модуль по умолчанию

    def exec_module(self, module):
        # Локальный импорт, чтобы избежать циклической зависимости
        from transpiler import translate_tiramisu, print_traceback

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
    """Класс для поиска импортируемых .tira-модулей с рецептом в Python"""

    def find_spec(self, fullname, path, target=None):
        if path is None:
            path = sys.path

        # Замена точек на слеши для вложенных импортов
        name_path = fullname.replace('.', os.sep)

        for entry in path:
            # Поиск файла с расширением '.tira'
            file_path = os.path.join(entry, name_path + '.tira')
            if os.path.exists(file_path):
                # Если файл найден, то он отдаётся загрузчику
                return spec_from_loader(fullname, TiramisuLoader(file_path))

        return None


def enable_import_hook():
    """Добавляет "магию" Tiramisu в стандартную систему импортов Python."""
    if not any(isinstance(finder, TiramisuFinder) for finder in sys.meta_path):
        # Вставка в самое начало списка, чтобы первым делом проверять '.tira'
        sys.meta_path.insert(0, TiramisuFinder())
