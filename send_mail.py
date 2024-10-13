"""SMTP Mail Send"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_core.messages import AIMessage, HumanMessage


def send_email(sender, receiver, subject, history):
    """Sending email"""
    print("ChatHistory:", history)
    server = smtplib.SMTP("localhost", port=25)

    msg_body = "<h3> Conversation History: </h3> <br/>"
    for message in history.messages:
        if isinstance(message, AIMessage):
            msg_body = "".join(
                [
                    msg_body,
                    '<strong style="font-size: 18;">AI: </strong>',
                    message.content,
                    "<br/>",
                ]
            )
        elif isinstance(message, HumanMessage):
            msg_body = "".join(
                [
                    msg_body,
                    '<strong style="font-size: 18;">Human: </strong>',
                    message.content,
                    "<br/>",
                ]
            )
        else:
            print("Message Type:" + str(type(message)))

    # mail_message = MIMEText(msg_body, "plain")
    mail_message = MIMEMultipart("alternative")
    mail_message["Subject"] = subject
    mail_message["From"] = sender
    mail_message["To"] = receiver

    content_body = MIMEText(msg_body, "html")
    mail_message.attach(content_body)

    server.sendmail(sender, receiver, mail_message.as_string())

    server.quit()
