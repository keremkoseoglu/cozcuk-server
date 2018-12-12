from cozdata import factory as dao_factory
from cozdata.dao import DataAccessObject
from flask import jsonify


def get_error_as_json(error, dao: DataAccessObject):
    if dao is not None:
        dao.disconnect()
    error_text = str(error)
    return jsonify({"error": error_text})


def get_success_as_json(success_text: str):
    return jsonify({"success": success_text})


def init_json_post(request) -> tuple:

    username = request.form.get("username")
    password = request.form.get("password")

    ldao = dao_factory.get_dao()
    ldao.connect()
    logged_in = ldao.login(username, password)
    if not logged_in:
        ldao.disconnect()
        raise Exception("Login error")
    return ldao, username
