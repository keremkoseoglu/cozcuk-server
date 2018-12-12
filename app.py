from flask import Flask, jsonify, request
from cozmodel import http as cozhttp

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Çözcük'


@app.route("/json/get_puzzle", methods=['POST'])
def json_get_puzzle():
    username = request.form.get("username")
    password = request.form.get("password")
    dao, logged_in = cozhttp.init_json_post(username, password)

    if not logged_in:
        return ""
    puzzle = dao.get_puzzle(username)
    dao.disconnect()
    return jsonify(puzzle.get_dict())


if __name__ == '__main__':
    app.run()
