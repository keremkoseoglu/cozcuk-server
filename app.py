from flask import Flask, jsonify, request
from cozmodel import http as cozhttp
from cozmodel.puzzle import Puzzle

app = Flask(__name__)

############################################################
# H T M L
############################################################


@app.route('/')
def hello_world():
    return 'Çözcük'


############################################################
# J S O N
############################################################


'''
Puzzle
'''


@app.route("/json/add_puzzle", methods=['POST'])
def json_add_puzzle():
    try:
        dao, username = cozhttp.init_json_post(request)
        new_puzzle = Puzzle(
            request.form.get["question"],
            request.form.get["hint"],
            request.form.get["answer"],
            int(request.form.get["difficulty"]),
            False
        )
        dao.add_puzzle(new_puzzle)
        dao.disconnect()
        return cozhttp.get_success_as_json("Question added")
    except Exception as error:
        return cozhttp.get_error_as_json(error, dao)


@app.route("/json/get_puzzle", methods=['POST'])
def json_get_puzzle():
    try:
        dao, username = cozhttp.init_json_post(request)
        puzzle = dao.get_puzzle(username)
        dao.disconnect()
        return jsonify(puzzle.get_dict())
    except Exception as error:
        return cozhttp.get_error_as_json(error, dao)


############################################################
# S T A R T U P
############################################################


if __name__ == '__main__':
    app.run()
