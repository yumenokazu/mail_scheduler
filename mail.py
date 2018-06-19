from flask_mail import Mail, Message
from app import app


def send_mail(body):
    with app.app_context():
        mail = Mail(app)
        msg = Message(subject=app.config.get("SUBJECT"),
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=[app.config.get("RECIPIENT")])
        msg.html=body
        mail.send(msg)