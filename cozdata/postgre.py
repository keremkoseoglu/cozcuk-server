from cozdata.dao import DataAccessObject
from cozmodel.puzzle import Puzzle
from cozmodel.user import User
import hashlib, os, psycopg2, random


class Postgre(DataAccessObject):

    _DB_FALSE = ""
    _DB_TRUE = "X"
    _MAX_ITER = 30
    _SALT = "mollusqumcontagiogum"

    def __init__(self):
        self._conn = None
        self._database_url = os.environ['DATABASE_URL']

    ############################################################
    # D A T A B A S E
    ############################################################

    def connect(self):
        if self._conn is None:
            self._conn = psycopg2.connect(self._database_url, sslmode='require')

    def disconnect(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    ############################################################
    # P U Z Z L E
    ############################################################

    def add_puzzle(self, new_puzzle: Puzzle):
        if self.get_puzzle(new_puzzle.question) is not None:
            return
        command = "INSERT INTO public.puzzle(question, answer, hint, approved, author) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(
            new_puzzle.question,
            new_puzzle.answer,
            new_puzzle.hint,
            self._bool_to_db(new_puzzle.approved),
            new_puzzle.author
        )
        self._execute(command)

    def approve_puzzle(self, question: str):
        command = "UPDATE public.puzzle SET approved = '{0}' WHERE question = '{1}'".format(
            self._bool_to_db(True),
            question
        )
        self._execute(command)

    def del_puzzle(self, question: str):
        command = "DELETE FROM public.puzzle WHERE question = '{0}'".format(question)
        self._execute(command)

    def get_puzzle(self, question: str) -> Puzzle:
        command = "SELECT question, answer, hint, approved, author FROM public.puzzle WHERE question = '{0}'".format(question)
        itab = self._select(command)

        if itab is None or len(itab) == 0:
            return None

        question, answer, hint, approved, author = itab[0]

        return Puzzle(
            question,
            hint,
            answer,
            self._bool_to_db(approved),
            author
        )

    def get_random_puzzle(self, user: str) -> Puzzle:
        itab = self._select("SELECT min(unique_int) as _min, max(unique_int) as _max FROM public.puzzle WHERE approved='X'")

        if itab is None or len(itab) == 0:
            return None

        mini, maxi = itab[0]
        iteration = 0

        while True:
            iteration += 1
            if iteration > self._MAX_ITER:
                raise Exception("Can't find random puzzle")

            random_int = random.randint(mini, maxi)
            command = "SELECT question FROM public.puzzle WHERE unique_int = {0} AND approved = 'X'".format(str(random_int))
            itab = self._select(command)

            if itab is None or len(itab) == 0:
                continue

            question = itab[0][0]
            return self.get_puzzle(question)

    def reject_puzzle(self, question: str):
        self.del_puzzle(question)

    def update_puzzle(self, new_puzzle: Puzzle):
        command = "UPDATE puzzle SET answer = '{0}', hint = '{1}', approved = '{2}', author = '{3}' WHERE question = '{4}'".format(
            new_puzzle.answer,
            new_puzzle.hint,
            self._bool_to_db(new_puzzle.approved),
            new_puzzle.author,
            new_puzzle.question
        )
        self._execute(command)

    ############################################################
    # U S E R
    ############################################################

    def add_user(self, new_user: User):
        if self.get_user(new_user.username) is not None:
            raise Exception("Username taken")
        command = "INSERT INTO public.user(username, password, email, role, is_oauth) VALUES ('{0}', '{1}', '{2}', '{3}')".format(
            new_user.username,
            self._encode(new_user.password),
            new_user.email,
            new_user.role,
            self._bool_to_db(new_user.is_oauth)
        )
        self._execute(command)

    def del_user(self, username: str):
        command = "DELETE FROM public.user WHERE username = '{0}'".format(username)
        self._execute(command)

    def get_user(self, username: str) -> User:
        command = "SELECT * FROM public.user WHERE username = '{0}'".format(username)
        itab = self._select(command)
        if itab is None or len(itab) == 0:
            return None
        user, pwd, email, role, is_oauth = itab[0]
        return User(
            user,
            pwd,
            email,
            role,
            self._db_to_bool(is_oauth)
        )

    def login(self, username: str, password: str) -> bool:
        user = self.get_user(username)
        return (not user.is_oauth) and user.password == self._encode(password)

    def register_oauth_user(self, username: str):
        if not self.get_user(username) is None:
            return
        oauth_user = User(
            username,
            "",
            "",
            User.ROLE_CONSUMER,
            True
        )
        self.add_user(oauth_user)

    def update_user(self, new_user: User, set_password=False):
        command = "UPDATE user SET email = '{0}', role = '{1}' WHERE username = '{2}'".format(
            new_user.email,
            new_user.role,
            new_user.username
        )
        self._execute(command)

        if set_password:
            command = "UPDATE user SET password = '{0}' WHERE username = '{1}'".format(
                self._encode(new_user.password),
                new_user.username
            )
            self._execute(command)

    ############################################################
    # P R I V A T E
    ############################################################

    def _bool_to_db(self, b: bool) -> str:
        if b:
            return self._DB_TRUE
        else:
            return self._DB_FALSE

    def _db_to_bool(self, b: str) -> bool:
        return b == self._DB_TRUE

    def _encode(self, text: str) -> str:
        if text is None or text == "":
            return ""
        return hashlib.sha512(self._SALT.encode() + text.encode()).hexdigest()

    def _execute(self, command: str):
        cur = self._conn.cursor()
        cur.execute(command)
        self._conn.commit()
        cur.close()

    def _select(self, command: str):
        cur = self._conn.cursor()
        cur.execute(command)
        itab = cur.fetchall()
        cur.close()
        return itab
