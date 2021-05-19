import os
import smtplib
from email.message import EmailMessage

class Mail:
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL')

    @classmethod
    def send_email(cls, receiver: str, subject: str, text: str):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = cls.SENDER_EMAIL
        msg['To'] = receiver
        msg.set_content(text)

        with smtplib.SMTP(cls.MAIL_SERVER, cls.MAIL_PORT) as server:
            server.login(cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            server.send_message(msg)
