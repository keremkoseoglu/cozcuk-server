from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from cozdata import factory as cozdata_factory
from cozweb import http as cozhttp, captcha as cozcaptcha
from cozmodel.user import User
import os

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config["SECRET_KEY"] = "SARI_KEDI_BEYAZ_KEDI"
app.config["APP_ROOT"] = os.path.dirname(os.path.abspath(__file__))
app.config["STATIC_FOLDER"] = os.path.join(app.config["APP_ROOT"], 'static')

############################################################
# H T M L
############################################################


@app.route('/')
def html_hello_world():
    if cozcaptcha.is_captcha_needed(session):
        return render_template("hello_captcha.html")
    else:
        return render_template("hello.html")


@app.route('/admin')
def html_admin_home():
    return render_template("hacker.html")


@app.route('/administrator')
def html_administrator_home():
    return render_template("hacker.html")


@app.route('/add_puzzle', methods=['GET'])
def html_add_puzzle():
    try:
        dao, username = cozhttp.init_auth_post(app, request, session)
        dao.disconnect()
        return render_template("add_puzzle.html")
    except Exception:
        return render_template("hacker.html")


@app.route('/add_user', methods=['GET'])
def html_add_user():
    try:
        return render_template(
            "user_register.html",
            uname="",
            email="",
            post_url=url_for("json_add_user")
        )
    except Exception:
        return render_template("hacker.html")


@app.route('/edit_user', methods=['GET'])
def html_edit_user():

    try:
        reset_token = request.args.get("reset_token")
        if reset_token is not None and reset_token != "":
            dao = cozdata_factory.get_dao()
            dao.connect()
            user = dao.get_user_by_reset_token(reset_token)
        else:
            dao, username = cozhttp.init_auth_post(app, request, session)
            user = dao.get_user(username)
        dao.disconnect()

        if user is None:
            raise Exception("Can't determine user")

        return render_template(
            "user_register.html",
            uname=user.username,
            email=user.email,
            post_url=url_for("json_update_user")
        )
    except Exception:
        return render_template("hacker.html")


@app.route('/forgot_pwd', methods=['GET'])
def html_forgot_pwd():
    try:
        return render_template("forgot_pwd.html")
    except Exception:
        return render_template("hacker.html")


@app.route('/game', methods=['GET'])
def html_game():
    try:
        dao, username = cozhttp.init_auth_post(app, request, session)
        dao.disconnect()
        return render_template("user_game.html")
    except Exception:
        return render_template("hacker.html")


@app.route('/help', methods=['GET'])
def html_help():
    return render_template("help.html")


@app.route('/login', methods=['POST'])
def html_login():
    try:
        dao, username = cozhttp.init_auth_post(app, request, session)
        session["username"] = username
        cozcaptcha.initialize_captcha(session)
        if dao.get_user(username).role == User.ROLE_ADMIN:
            try:
                cozcaptcha.delete_old_files(app.config["STATIC_FOLDER"])
            except:
                pass
            return redirect(url_for("html_admin"))
        else:
            return redirect(url_for("html_game"))
    except Exception:
        if cozhttp.get_form_value(request, "username") is not None or cozhttp.get_form_value(request, "username") != "":
            cozcaptcha.generate_captcha(session, app.config["STATIC_FOLDER"])
        return redirect(url_for("html_hello_world"))


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
        dao, username = cozhttp.init_auth_post(app, request, session)
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
        dao, cud_puzzle = cozhttp.init_json_puzzle_cud(
            app,
            request,
            session,
            must_be_admin=False
        )
        dao.add_puzzle(cud_puzzle)
        dao.disconnect()
        return cozhttp.get_success_as_json("True")
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/check_answer", methods=['POST'])
def json_check_answer():
    try:
        dao, username = cozhttp.init_auth_post(app, request, session)

        user_question = cozhttp.get_form_value(request, "question")
        user_answer = cozhttp.get_form_value(request, "answer").replace(" ", "")
        correct_answer = dao.get_puzzle(user_question).answer

        is_correct = correct_answer == user_answer
        dao.disconnect()
        return cozhttp.get_success_as_json(str(is_correct))
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/del_puzzle", methods=['POST'])
def json_del_puzzle():
    try:
        dao, cud_puzzle = cozhttp.init_json_puzzle_cud(app, request, session)
        dao.del_puzzle(cud_puzzle.question)
        dao.disconnect()
        return cozhttp.get_success_as_json("True")
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/forgot_pwd", methods=['GET'])
def json_forgot_pwd():
    try:
        posted_username = request.args.get("uname")
        cozhttp.send_forgot_password_email(posted_username, url_for("html_edit_user"))
        return cozhttp.get_success_as_json("True")
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/get_puzzle", methods=['GET', 'POST'])
def json_get_puzzle():
    try:
        dao, username = cozhttp.init_auth_post(app, request, session)
        puzzle = dao.get_random_puzzle(username)
        dao.disconnect()
        return jsonify(puzzle.get_dict(include_answer=False))
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/update_puzzle", methods=['POST'])
def json_update_puzzle():
    try:
        dao, cud_puzzle = cozhttp.init_json_puzzle_cud(app, request, session)
        dao.update_puzzle(cud_puzzle)
        dao.disconnect()
        return cozhttp.get_success_as_json("True")
    except Exception as error:
        return cozhttp.get_error_as_json(error)


'''
User
'''


@app.route("/json/add_user", methods=['POST'])
def json_add_user():
    try:
        dao, cud_user = cozhttp.init_json_user_cud(
            app,
            request,
            session,
            check_auth=False
        )
        dao.add_user(cud_user)
        dao.disconnect()
        return cozhttp.get_success_as_json("True")
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/del_user", methods=['POST'])
def json_del_user():
    try:
        dao, cud_user = cozhttp.init_json_user_cud(app, request, session)
        dao.del_user(cud_user.username)
        dao.disconnect()
        return cozhttp.get_success_as_json("True")
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/get_user", methods=['POST'])
def json_get_user():
    try:
        dao, username = cozhttp.init_auth_post(app, request, session)
        user = dao.get_user(username)
        dao.disconnect()
        return jsonify(user.get_dict())
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/oauth", methods=['GET'])
def json_oauth():
    try:
        oauth_username = request.args.get("oauth_username")
        oauth_token = request.args.get("oauth_token")
        if oauth_username is None or oauth_username == "":
            raise Exception("Invalid username")
        if not cozhttp.is_oauth_valid(oauth_token, oauth_username):
            raise Exception("Invalid token")

        ldao = cozdata_factory.get_dao()
        ldao.connect()
        ldao.register_oauth_user(oauth_username)
        ldao.disconnect()

        session["username"] = oauth_username
        return cozhttp.get_success_as_json("True")
    except Exception as error:
        return cozhttp.get_error_as_json(error)


@app.route("/json/update_user", methods=['POST'])
def json_update_user():
    try:
        dao, cud_user = cozhttp.init_json_user_cud(app, request, session)
        dao.update_user(
            cud_user,
            set_password=(cud_user.password != "")
        )
        dao.disconnect()
        return cozhttp.get_success_as_json("True")
    except Exception as error:
        return cozhttp.get_error_as_json(error)


############################################################
# S T A R T U P
############################################################


if __name__ == '__main__':
    app.run()
