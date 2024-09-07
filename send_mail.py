"""SMTP Mail Send"""

import smtplib
from email.mime.text import MIMEText


def send_email(sender, receiver, subject, message):
    """Sending email"""
    server = smtplib.SMTP("localhost", port=25)

    msg_body = "Conversation History:\n"
    msg_body += str(message)

    mail_message = MIMEText(msg_body, "plain")
    mail_message["Subject"] = subject
    mail_message["From"] = sender
    mail_message["To"] = receiver

    server.sendmail(sender, receiver, mail_message.as_string())

    server.quit()
