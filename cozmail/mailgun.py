from cozmail.mao import Mailer
import os, requests


class Mailgun(Mailer):

    _SENDER = "Cozcuk <mailgun@cozcuk.keremkoseoglu.com>"

    def send_mail(self, to: str, subject: str, body: str):
        requests.post(
            "https://api.mailgun.net/v3/cozcuk.keremkoseoglu.com/messages",
            auth=("api", os.environ["MAILGUN_API_KEY"]),
            data={"from": self._SENDER,
                  "to": [to],
                  "subject": subject,
                  "text": body}
        )

