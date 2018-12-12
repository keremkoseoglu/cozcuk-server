from cozdata.dao import DataAccessObject
from cozmodel.puzzle import Puzzle


class HardCode(DataAccessObject):

    def connect(self):
        return

    def disconnect(self):
        return

    def get_puzzle(self, user: str) -> Puzzle:
        return Puzzle("SAÇSIZDOĞURTANK", "SAÇSIZ DOĞURTAN K", "KELEBEK", 1)

