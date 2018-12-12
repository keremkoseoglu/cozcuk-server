from cozdata.dao import DataAccessObject
from cozmodel.puzzle import Puzzle


class HardCode(DataAccessObject):

    def add_puzzle(self, new_puzzle: Puzzle):
        return

    def connect(self):
        return

    def disconnect(self):
        return

    def get_puzzle(self, user: str) -> Puzzle:
        return Puzzle("SAÇSIZDOĞURTANK", "SAÇSIZ DOĞURTAN K", "KELEBEK", 1)

    def login(self, user: str, password: str) -> bool:
        return True
