from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from cozweb import http as cozhttp
from cozmodel.user import User
from cozdata import factory as dao_factory

app = Flask(__name__)
app.secret_key = "SARI_KEDI_BEYAZ_KEDI"
app.config["CACHE_TYPE"] = "null"

############################################################
# H T M L
############################################################


@app.route('/')
def html_hello_world():
    return render_template("hello.html")


@app.route('/admin')
def html_admin_home():
    return render_template("hacker.html")


@app.route('/administrator')
def html_administrator_home():
    return render_template("hacker.html")


@app.route('/game', methods=['GET'])
def html_game():
    try:
        dao, username = cozhttp.init_auth_post(request, session)
        dao.disconnect()
        return render_template("user_game.html")
    except Exception:
        return render_template("hacker.html")


@app.route('/login', methods=['POST'])
def html_login():
    try:
        dao, username = cozhttp.init_auth_post(request, session)
        session["username"] = username
        if dao.get_user(username).role == User.ROLE_ADMIN:
            return redirect(url_for("html_admin"))
        else:
            return redirect(url_for("html_game"))
    except Exception:
        return render_template("hacker.html")


@app.route('/logout', methods=['GET'])
def html_logout():
    session["username"] = ""
    return redirect(url_for("html_hello_world"))


@app.route('/privacy', methods=['GET'])
def html_privacy():
    return app.send_static_file("privacy.html")


@app.route('/psm', methods=['GET'])
def html_admin():
    try:
        dao, username = cozhttp.init_auth_post(request, session)
        dao.disconnect()
        return render_template("admin_menu.html")
    except Exception:
        return render_template("hacker.html")

############################################################
# J S O N
############################################################


'''
Puzzle
'''


@app.route("/json/add_puzzle", methods=['POST'])
def json_add_puzzle():
    try:
        dao, cud_puzzle = cozhttp.init_json_puzzle_cud(request, session)
        dao.add_puzzle(cud_puzzle)
        dao.disconnect()
        return cozhttp.get_success_as_json("Question added")
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/check_answer", methods=['POST'])
def json_check_answer():
    try:
        dao, username = cozhttp.init_auth_post(request, session)

        user_question = request.form.get("question")
        user_answer = request.form.get("answer").replace(" ", "").replace("i", "İ").upper()

        is_correct = dao.get_puzzle(user_question).answer == user_answer
        dao.disconnect()
        return cozhttp.get_success_as_json(str(is_correct))
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/del_puzzle", methods=['POST'])
def json_del_puzzle():
    try:
        dao, cud_puzzle = cozhttp.init_json_puzzle_cud(request, session)
        dao.del_puzzle(cud_puzzle.question)
        dao.disconnect()
        return cozhttp.get_success_as_json("Question deleted")
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/get_puzzle", methods=['GET', 'POST'])
def json_get_puzzle():
    try:
        dao, username = cozhttp.init_auth_post(request, session)
        puzzle = dao.get_random_puzzle(username)
        dao.disconnect()
        return jsonify(puzzle.get_dict(include_answer=False))
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/update_puzzle", methods=['POST'])
def json_update_puzzle():
    try:
        dao, cud_puzzle = cozhttp.init_json_puzzle_cud(request, session)
        dao.update_puzzle(cud_puzzle)
        dao.disconnect()
        return cozhttp.get_success_as_json("Question modified")
    except Exception as error:
        return cozhttp.get_error_as_json(error)


'''
User
'''


@app.route("/json/add_user", methods=['POST'])
def json_add_user():
    try:
        dao, cud_user = cozhttp.init_json_user_cud(request, session)
        dao.add_user(cud_user)
        dao.disconnect()
        return cozhttp.get_success_as_json("User added")
    except Exception as error:
        return cozhttp.get_error_as_json(error, dao)


@app.route("/json/del_user", methods=['POST'])
def json_del_user():
    try:
        dao, cud_user = cozhttp.init_json_user_cud(request, session)
        dao.del_user(cud_user.username)
        dao.disconnect()
        return cozhttp.get_success_as_json("User deleted")
    except Exception as error:
        return cozhttp.get_error_as_json(error, dao)


@app.route("/json/get_user", methods=['POST'])
def json_get_user():
    try:
        dao, username = cozhttp.init_auth_post(request, session)
        user = dao.get_user(username)
        dao.disconnect()
        return jsonify(user.get_dict())
    except Exception as error:
        return cozhttp.get_error_as_json(error, dao)


@app.route("/json/oauth", methods=['GET'])
def json_oauth():
    try:
        oauth_username = request.args.get("oauth_username")
        if oauth_username is None or oauth_username == "":
            raise Exception("Invalid username")
        session["username"] = oauth_username
        return cozhttp.get_success_as_json("True")
    except Exception as error:
        return cozhttp.get_error_as_json(error, None)


@app.route("/json/update_user", methods=['POST'])
def json_update_user():
    try:
        dao, cud_user = cozhttp.init_json_user_cud(request, session)
        dao.update_user(cud_user)
        dao.disconnect()
        return cozhttp.get_success_as_json("User modified")
    except Exception as error:
        return cozhttp.get_error_as_json(error, dao)


############################################################
# S T A R T U P
############################################################


if __name__ == '__main__':
    app.run()
