from abc import ABC, abstractmethod
from cozmodel.puzzle import Puzzle

class DataAccessObject(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def add_puzzle(self, new_puzzle: Puzzle):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def get_puzzle(self, user: str) -> Puzzle:
        pass

    @abstractmethod
    def login(self, user: str, password: str) -> bool:
        pass
