from cozdata import factory as cozdata_factory
from cozmail import factory as cozmail_factory
from cozmodel.puzzle import Puzzle
from cozmodel.user import User
from cozweb import captcha as cozcaptcha
from flask import jsonify
import os
import requests
import uuid
import json

'''
General
'''


def get_error_as_text(error) -> str:
    error_text = str(error)
    print("Error: " + error_text)
    return error_text


def get_error_as_json(error):
    error_text = str(error)
    print("Error: " + error_text)
    return jsonify({"error": error_text})


def get_form_value(request, key) -> str:
    output = ""

    output = request.form.get(key)

    if output is None or output == "":
        try:
            json_data = json.loads(request.data)
            output = json_data[key]
        except:
            pass

    return output


def get_success_as_json(success_text: str):
    return jsonify({"success": success_text})


def init_auth_post(app, request, session) -> tuple:

    logged_in = False
    ldao = cozdata_factory.get_dao()

    username = get_form_value(request, "username")

    if username is None or username == "":
        if "username" in session:
            username = session["username"]
            logged_in = username != ""
            ldao.connect()
    else:
        password = get_form_value(request, "password")
        ldao.connect()
        logged_in = ldao.login(username, password)

        if logged_in and cozcaptcha.is_captcha_needed(session):
            expected_captcha = session["captcha_answer"]
            logged_in = expected_captcha == get_form_value(request, "captcha")

    if not logged_in and ( not ( username is None or username == "" ) ):
        if is_oauth_valid(password, username):
            logged_in = True

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
        get_form_value(request, "question"),
        get_form_value(request, "hint"),
        get_form_value(request, "answer"),
        False,
        username
    )
    return ldao, new_puzzle


'''
User
'''


def get_oauth_response(user_token: str) -> {}:
    url = "https://graph.facebook.com/me?access_token={0}".format(user_token)
    resp = requests.get(url)
    return resp.json()


def init_json_user_cud(app, request, session, check_auth=True) -> tuple:

    posted_username = get_form_value(request, "_username")

    if check_auth:
        ldao, username = init_auth_post(app, request, session)
        if posted_username != session["username"]:
            ldao.get_user(username).ensure_admin()
    else:
        ldao = cozdata_factory.get_dao()
        ldao.connect()
    new_user = User(
        posted_username,
        get_form_value(request, "_password"),
        get_form_value(request, "email"),
        User.ROLE_CONSUMER,
        False
    )
    return ldao, new_user


def is_oauth_valid(user_token: str, user_name: str) -> bool:
    oauth_resp = get_oauth_response(user_token)
    if "id" in oauth_resp and oauth_resp["id"] == user_name:
        return True
    else:
        return False


def send_forgot_password_email(user_name: str, target_path: str):
    if user_name is None or user_name == "":
        return

    ldao = cozdata_factory.get_dao()
    ldao.connect()
    forgetful_user = ldao.get_user(user_name)

    if forgetful_user is None:
        ldao.disconnect()
        return
    if forgetful_user.email is None or forgetful_user.email == "":
        ldao.disconnect()
        return
    if forgetful_user.is_oauth:
        ldao.disconnect()
        return

    reset_token = str(uuid.uuid4().hex)

    ldao.set_user_reset_token(forgetful_user.username, reset_token)
    ldao.disconnect()

    url = os.environ["COZCUK_DOMAIN"] + target_path + "?reset_token=" + reset_token
    mail_body = "Parolanızı sıfırlamak için tıklayın: " + url

    cozmail_factory.get_mao().send_mail(
        forgetful_user.email,
        "Çözcük parola sıfırlama",
        mail_body
    )
