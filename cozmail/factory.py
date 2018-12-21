from cozmail import mao
import inspect, sys
import os

_DATA_PATH = "cozmail"
_MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')


def get_mao() -> mao.Mailer:
    active_mail_class = os.environ["MAIL_CLASS"]
    all_maos = _get_all_maos()
    return all_maos[active_mail_class]() # Örnek değer: HardCode


def _get_all_modules():
    output = []
    path = os.path.join(os.getcwd(), _DATA_PATH)
    files = [f for f in os.listdir(path)]
    for f in files:
        if f[:2] != "__" and f[:3] != "mao" and f[:7] != "factory":
            fname = os.path.splitext(f)[0]
            output.append(fname)
    return output


def _get_all_maos() -> {}:
    output = {}

    modules = _get_all_modules()

    for m in modules:
        module_name = _DATA_PATH + "." + m
        module = __import__(module_name, fromlist=[""])

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if _DATA_PATH in str(obj) and \
                    name != "Mailer" and \
                    name != "factory":
                output[name] = obj

    return output
