from flask_mail import Mail, Message
from wsgi import application as app


def send_mail(body, subject):
    with app.app_context():
        mail = Mail(app)
        msg = Message(sender=app.config.get("MAIL_USERNAME"),
                      recipients=[app.config.get("RECIPIENT")])
        msg.subject = subject
        msg.html=body
        mail.send(msg)