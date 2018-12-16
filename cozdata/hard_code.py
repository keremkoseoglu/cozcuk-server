from cozdata.dao import DataAccessObject
from cozmodel.puzzle import Puzzle
from cozmodel.user import User
import random


class HardCode(DataAccessObject):

    _EMAIL = "kerem@keremkoseoglu.com"
    _PASSWORD = "123"

    _PUZZLES = [
        {
            "question": "AĞIRLIKNIGRAD",
            "answer": "YÜKSÜK",
            "hint": "AĞIRLIK NIGRAD"
        },
        {
            "question": "BEYGİRTERBİYEİ",
            "answer": "ATARİ",
            "hint": "BEYGİR TERBİYE İ"
        },
        {
            "question": "DEFOLTERBİYE",
            "answer": "GİTAR",
            "hint": "DEFOL TERBİYE"
        },
        {
            "question": "DNAMREMAK",
            "answer": "DÜNYA",
            "hint": "D NAM REMAK"
        },
        {
            "question": "ELADAKIRMIZI",
            "answer": "SAKAL",
            "hint": "ELADA KIRMIZI"
        },
        {
            "question": "HİKIÇBÜTÜN",
            "answer": "HİPOPOTAM",
            "hint": "Hİ KIÇ BÜTÜN"
        },
        {
            "question": "KAYIKÇİĞNEYUT",
            "answer": "SANDALYE",
            "hint": "KAYIK ÇİĞNEYUT"
        },
        {
            "question": "KDUDAKLAİLAVE",
            "answer": "KÖPEK",
            "hint": "K DUDAKLA İLAVE"
        },
        {
            "question": "KÜLOTBEKLESU",
            "answer": "DONDURMA",
            "hint": "KÜLOT BEKLE SU"
        },
        {
            "question": "MATEMZA",
            "answer": "YASTIK",
            "hint": "MATEM ZA"
        },
        {
            "question": "PKAYAKIT",
            "answer": "PAPAZ",
            "hint": "P KAYA KIT"
        },
        {
            "question": "SAÇSIZDOĞURTANK",
            "answer": "KELEBEK",
            "hint": "SAÇSIZ DOĞURTAN K"
        },
        {
            "question": "TEICNABAYVİŞARETYERN",
            "answer": "TELEVİZYON",
            "hint": "TE ICNABAY V İŞARET YER N"
        },
        {
            "question": "YAKALAUCUPAPTA",
            "answer": "KAPLAN",
            "hint": "YAKALA UCUPAPTA"
        }
    ]

    _USERS = [
        {
            "username": "kerem",
            "role": "A"
        },
        {
            "username": "ozge",
            "role": "C"
        }
    ]


    ############################################################
    # D A T A B A S E
    ############################################################

    def connect(self):
        return

    def disconnect(self):
        return

    ############################################################
    # P U Z Z L E
    ############################################################

    def add_puzzle(self, new_puzzle: Puzzle):
        return

    def approve_puzzle(self, question: str):
        return

    def del_puzzle(self, question: str):
        return

    def get_puzzle(self, question: str) -> Puzzle:
        for p in self._PUZZLES:
            if p["question"] == question:
                return Puzzle(
                    p["question"],
                    p["hint"],
                    p["answer"],
                    True,
                    self._USERS[0]["username"]
                )
        raise Exception("Unknown puzzle")

    def get_random_puzzle(self, user: str) -> Puzzle:
        rnd_index = random.randint(0, len(self._PUZZLES) - 1)
        rnd_puzzle = self._PUZZLES[rnd_index]
        return Puzzle(
            rnd_puzzle["question"],
            rnd_puzzle["hint"],
            rnd_puzzle["answer"],
            True,
            self._USERS[0]["username"]
        )

    def reject_puzzle(self, question: str):
        return

    def update_puzzle(self, new_puzzle: Puzzle):
        return

    ############################################################
    # U S E R
    ############################################################

    def add_user(self, new_user: User):
        return

    def del_user(self, username: str):
        return

    def get_user(self, username: str) -> User:
        for user in self._USERS:
            if user["username"] == username:
                return User(
                    user["username"],
                    self._PASSWORD,
                    self._EMAIL,
                    user["role"]
                )
        raise Exception("Unknown user: " + username)

    def login(self, username: str, password: str) -> bool:
        try:
            return self.get_user(username).password == password
        except:
            return False

    def update_user(self, new_user: User, set_password=False):
        return
