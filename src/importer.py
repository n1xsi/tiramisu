from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_loader
import sys
import os

from transpiler import translate_tiramisu, print_traceback


class TiramisuLoader(Loader):
    ...


class TiramisuFinder(MetaPathFinder):
    ...
