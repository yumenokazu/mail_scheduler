from app import app as application  # "application" is recognized by gunicorn
import task_scheduler

if __name__ == "__main__":
    application.run()