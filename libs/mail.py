import smtplib
from email.message import EmailMessage

class Mail:
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'ba04ea8026e716'
    MAIL_PASSWORD = '260615d93e79b7'
    SENDER_EMAIL = 'from@example.com'

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
