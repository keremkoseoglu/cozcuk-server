

class Puzzle:

    _DIFF_EASY = 1
    _DIFF_MEDIUM = 2
    _DIFF_HARD = 3

    def __init__(self, question: str, hint: str, answer: str, difficulty: int):
        self.question = question
        self.answer = answer
        self.hint = hint
        self.difficulty = difficulty

    def get_dict(self) -> {}:
        return {
            "question": self.question,
            "answer": self.answer,
            "hint": self.hint,
            "difficulty": self.difficulty
        }

