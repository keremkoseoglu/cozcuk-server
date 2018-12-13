from abc import ABC, abstractmethod
from cozmodel.puzzle import Puzzle
from cozmodel.user import User


class DataAccessObject(ABC):

    def __init__(self):
        pass

    '''
    Database
    '''

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    '''
    Puzzle
    '''

    @abstractmethod
    def add_puzzle(self, new_puzzle: Puzzle):
        pass

    @abstractmethod
    def approve_puzzle(self, question: str):
        pass

    @abstractmethod
    def del_puzzle(self, question: str):
        pass

    @abstractmethod
    def get_puzzle(self, question: str) -> Puzzle:
        pass

    @abstractmethod
    def get_random_puzzle(self, user: str) -> Puzzle:
        pass

    @abstractmethod
    def reject_puzzle(self, question: str):
        pass

    @abstractmethod
    def update_puzzle(self, new_puzzle: Puzzle):
        pass

    '''
    User
    '''

    @abstractmethod
    def add_user(self, new_user: User):
        pass

    @abstractmethod
    def del_user(self, username: str):
        pass

    @abstractmethod
    def get_user(self, username: str) -> User:
        pass

    @abstractmethod
    def login(self, user: str, password: str) -> bool:
        pass

    @abstractmethod
    def update_user(self, new_user: User):
        pass

