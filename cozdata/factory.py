from cozdata import dao, hard_code
import inspect, sys
import os

_DATA_PATH = "cozdata"
_MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')


def get_dao(data_class: str) -> dao.DataAccessObject:
    all_daos = _get_all_daos()
    return all_daos[data_class]() # Örnek değer: HardCode


def _get_all_modules():
    output = []
    path = os.path.join(os.getcwd(), _DATA_PATH)
    files = [f for f in os.listdir(path)]
    for f in files:
        if f[:2] != "__" and f[:3] != "dao" and f[:7] != "factory":
            fname = os.path.splitext(f)[0]
            output.append(fname)
    return output


def _get_all_daos() -> {}:
    output = {}

    modules = _get_all_modules()

    for m in modules:
        module_name = _DATA_PATH + "." + m
        module = __import__(module_name, fromlist=[""])

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if _DATA_PATH in str(obj) and \
                    name != "DataAccessObject" and \
                    name != "factory":
                output[name] = obj

    return output
