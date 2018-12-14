from captcha.image import ImageCaptcha
import random, os


_CAPTCHA_CHARS = "1234567890qwertyuiopasdfghjklzxcvbnm"
_CAPTCHA_FOLDER = "captcha"
_STATIC_FOLDER = ""


def generate_captcha(session, static_folder: str):

    global _STATIC_FOLDER

    captcha_answer = ""
    _STATIC_FOLDER = static_folder

    for i in range(0, 4):
        rnd_pos = random.randint(0, len(_CAPTCHA_CHARS) - 1)
        rnd_char = _CAPTCHA_CHARS[rnd_pos:rnd_pos+1]
        captcha_answer += rnd_char

    target_path = _get_png_file_path(captcha_answer)

    image = ImageCaptcha()
    image.write(captcha_answer, target_path)

    session["captcha_answer"] = captcha_answer


def initialize_captcha(session):
    session["captcha_answer"] = ""


def is_captcha_needed(session) -> bool:
    if "captcha_answer" in session:
        if session["captcha_answer"] != "":
            return True
    return False


def _get_png_file_path(answer: str) -> str:
    global _STATIC_FOLDER

    file_name = answer + ".png"
    target_path = os.path.join(_STATIC_FOLDER, _CAPTCHA_FOLDER, file_name)
    return target_path

