from captcha.image import ImageCaptcha
import os, random, time, uuid


_CAPTCHA_CHARS = "345689qwertyupasdfghjklxcvbnm"
_CAPTCHA_FOLDER = "captcha"
_EXTENSION = "png"
_FILE_KEEP_DURATION = 5

_static_folder = ""


def delete_old_files(static_folder: str):
    captcha_path = _get_captcha_path(static_folder)
    now = time.localtime()
    for file in os.listdir(captcha_path):
        if not file.endswith(_EXTENSION):
            continue
        file_path = os.path.join(captcha_path, file)
        modified_epoch = os.path.getmtime(file_path)
        modified_time = time.localtime(modified_epoch)
        if _is_file_deletable(now, modified_time):
            os.remove(file_path)


def generate_captcha(session, static_folder: str):

    global _static_folder

    captcha_answer = ""
    _static_folder = static_folder

    for i in range(0, 4):
        rnd_pos = random.randint(0, len(_CAPTCHA_CHARS) - 1)
        rnd_char = _CAPTCHA_CHARS[rnd_pos:rnd_pos+1]
        captcha_answer += rnd_char

    file_name, target_path = _get_png_file_path()

    image = ImageCaptcha()
    image.write(captcha_answer, target_path)

    session["captcha_answer"] = captcha_answer
    session["captcha_file"] = file_name


def initialize_captcha(session):
    session["captcha_answer"] = ""


def is_captcha_needed(session) -> bool:
    if "captcha_answer" in session:
        if session["captcha_answer"] != "":
            return True
    return False


def _get_captcha_path(static_folder: str):
    return os.path.join(static_folder, _CAPTCHA_FOLDER)


def _get_png_file_path() -> tuple:
    global _static_folder

    file_name = str(uuid.uuid4()) + "." + _EXTENSION
    target_path = os.path.join(_get_captcha_path(_static_folder), file_name)
    return file_name, target_path


def _is_file_deletable(now, file_date) -> int:
    if now[0] > file_date[0]:
        return True
    elif now[0] == file_date[0]:
        if now[1] > file_date[1]:
            return True
        elif now[1] == file_date[1]:
            if now[2] > file_date[2]:
                return True
            elif now[2] == file_date[2]:
                if now[3] > file_date[3]:
                    return True
                elif now[3] == file_date[3]:
                    diff = now[4] - file_date[4]
                    if diff > _FILE_KEEP_DURATION:
                        return True
    return False
