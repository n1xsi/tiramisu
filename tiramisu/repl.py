from .transpiler import translate_tiramisu, print_traceback
from .importer import enable_import_hook

from tokenize import TokenError
import codeop
import sys
import os


def start_repl():
    """Запускает интерактивную консоль для рецептов (REPL)."""
    ...
