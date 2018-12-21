from abc import ABC, abstractmethod


class Mailer(ABC):

    @abstractmethod
    def send_mail(self, to: str, subject: str, body: str):
        pass

    