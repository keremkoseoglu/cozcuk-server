from cozdata import factory as dao_factory
from flask import jsonify
from cozmodel.puzzle import Puzzle
from cozmodel.user import User
from cozweb import captcha as cozcaptcha
import requests

'''
General
'''


def get_error_as_text(error) -> str:
    return str(error)


def get_error_as_json(error):
    error_text = str(error)
    return jsonify({"error": error_text})


def get_success_as_json(success_text: str):
    return jsonify({"success": success_text})


def init_auth_post(app, request, session) -> tuple:

    logged_in = False
    ldao = dao_factory.get_dao(app.config["DATA_CLASS"])

    username = request.form.get("username")

    if username is None or username == "":
        if "username" in session:
            username = session["username"]
            logged_in = username != ""
            ldao.connect()
    else:
        password = request.form.get("password")
        ldao.connect()
        logged_in = ldao.login(username, password)

        if logged_in and cozcaptcha.is_captcha_needed(session):
            expected_captcha = session["captcha_answer"]
            logged_in = expected_captcha == request.form.get("captcha")

    if not logged_in:
        ldao.disconnect()
        raise Exception("Login error")
    return ldao, username


'''
Puzzle
'''


def init_json_puzzle_cud(app, request, session, must_be_admin: True) -> tuple:
    ldao, username = init_auth_post(app, request, session)
    if must_be_admin:
        ldao.get_user(username).ensure_admin()

    new_puzzle = Puzzle(
        request.form.get("question"),
        request.form.get("hint"),
        request.form.get("answer"),
        False,
        username
    )
    return ldao, new_puzzle


'''
User
'''


def init_json_user_cud(app, request, session, check_auth=True) -> tuple:
    if check_auth:
        ldao, username = init_auth_post(app, request, session)
        ldao.get_user(username).ensure_admin()
    else:
        ldao = dao_factory.get_dao(app.config["DATA_CLASS"])
        ldao.connect()
    new_user = User(
        request.form.get("_username"),
        request.form.get("_password"),
        request.form.get("email"),
        User.ROLE_CONSUMER
    )
    return ldao, new_user


def is_oauth_valid(user_token: str, app_token: str) -> bool:
    url = "http://graph.facebook.com/debug_token?input_token={0}&access_token={1}".format(user_token, app_token)
    resp = requests.get(url)
    return True

