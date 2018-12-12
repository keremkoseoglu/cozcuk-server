from cozdata.dao import DataAccessObject
from cozmodel.puzzle import Puzzle
from cozmodel.user import User

class HardCode(DataAccessObject):

    '''
    Database
    '''

    def connect(self):
        return

    def disconnect(self):
        return

    '''
    Puzzle
    '''

    def add_puzzle(self, new_puzzle: Puzzle):
        return

    def approve_puzzle(self, question: str):
        return

    def del_puzzle(self, question: str):
        return

    def get_puzzle(self, user: str) -> Puzzle:
        return Puzzle("SAÇSIZDOĞURTANK", "SAÇSIZ DOĞURTAN K", "KELEBEK", 1, True)

    def reject_puzzle(self, question: str):
        return

    def update_puzzle(self, new_puzzle: Puzzle):
        return

    '''
    User
    '''

    def add_user(self, new_user: User):
        return

    def del_user(self, username: str):
        return

    def login(self, user: str, password: str) -> bool:
        return True

    def update_user(self, new_user: User):
        return
