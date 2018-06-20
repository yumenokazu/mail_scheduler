from flask import Flask
import config
import os


def create_app():
    cfg = config.ProductionConfig() if os.environ.get('ENV') == 'prod' else config.DevelopmentConfig()

    if all([cfg.MAIL_USERNAME, cfg.MAIL_PASSWORD, cfg.RECIPIENT]):
        app = Flask(__name__)   # name "application" is recognized by gunicorn
        app.config.from_object(cfg)
        return app
    else:
        print("Configure python-keyring variables MAIL_USER, MAIL_PASSWORD and RECIPIENT for 'scheduled_mail' service")
        quit(1)


application = create_app()
import task_scheduler

if __name__ == "__main__":
    if application is not None:
        application.run(use_reloader=False)