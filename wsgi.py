from app import app as application  # name "application" is recognized by gunicorn

if __name__ == "__main__":
    if application is not None:
        application.run(use_reloader=False)