from cozdata import factory as dao_factory
from flask import jsonify
from cozmodel.puzzle import Puzzle
from cozmodel.user import User


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


def init_auth_post(request, session) -> tuple:

    logged_in = False
    ldao = dao_factory.get_dao()

    username = request.form.get("username")

    if username is None or username == "":
        if "username" in session:
            username = session["username"]
            logged_in = True
    else:
        password = request.form.get("password")
        ldao.connect()
        logged_in = ldao.login(username, password)

    if not logged_in:
        ldao.disconnect()
        raise Exception("Login error")
    return ldao, username


'''
Puzzle
'''


def init_json_puzzle_cud(request, session) -> tuple:
    ldao, username = init_auth_post(request, session)
    ldao.get_user(username).ensure_admin()
    new_puzzle = Puzzle(
        request.form.get["question"],
        request.form.get["hint"],
        request.form.get["answer"],
        False,
        username
    )
    return ldao, new_puzzle


'''
User
'''


def init_json_user_cud(request, session) -> tuple:
    ldao, username = init_auth_post(request, session)
    ldao.get_user(username).ensure_admin()
    new_user = User(
        request.form.get["_username"],
        request.form.get["_password"],
        request.form.get["email"],
        request.form.get["role"]
    )
    return ldao, new_user
