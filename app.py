from flask import Flask, jsonify
from cozdata import factory as dao_factory

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/json/get_puzzle")
def json_get_puzzle():
    ldao = dao_factory.get_dao()
    ldao.connect()
    puzzle = ldao.get_puzzle("") # todo 500 buraya user eklenecek
    ldao.disconnect()
    return jsonify(puzzle.get_dict())

if __name__ == '__main__':
    app.run()
