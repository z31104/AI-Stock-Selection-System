from flask_mail import Message


def send_email(mail, to_email, subject, content):

    msg = Message(
        subject,
        sender=None,
        recipients=[to_email]
    )

    msg.body = content

    mail.send(msg)

    return True