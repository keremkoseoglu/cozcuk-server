

class Puzzle:

    def __init__(self, question: str, hint: str, answer: str, approved: bool, author: str):
        self.question = question
        self.answer = answer
        self.hint = hint
        self.approved = approved
        self.author = author

    def get_dict(self, include_answer=True) -> {}:
        ret = {
            "question": self.question,
            "hint": self.hint,
            "approved": self.approved,
            "author": self.author
        }

        if include_answer:
            ret["answer"] = self.answer
            pass

        return ret

