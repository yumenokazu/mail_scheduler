import logging
import typing
from datetime import datetime, timedelta

import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from wsgi import application as app

from instance import create_from_csv
from mail import send_mail


players = create_from_csv(app.config.get("INSTANCE_PATH"))

interval = app.config.get("SCHEDULER_INTERVAL")  # interval for job schedule
interval_str = f"*/{interval}"
scheduler = BackgroundScheduler()  # create scheduler
atexit.register(lambda: scheduler.shutdown())  # shutdown scheduler when flask stops
scheduler.start()  # start scheduler


def _create_body(players: typing.List["Instance"], current_time: datetime):
    """
    Create mail html body with starting and stopping player names
    :param players: list with instances of Instance class
    :param current_time: current time in datetime format
    :return: tuple containing html or None and subject string or None
    """
    from io import StringIO
    should_start = [p.name for p in players if p.should_start(current_time)]
    should_stop = [p.name for p in players if p.should_end(current_time)]
    is_running = [p.name for p in players if p.is_running(current_time)]
    buf = StringIO()
    if len(should_stop) > 0 or len(should_stop) > 0:
        buf.write('<div style="width:200px;background: #b5d387;'
                  'margin:10px auto; padding: 20px 20px 20px 50px;'
                  'font-size: large;"><p>Should be running:</p>')
        for name in is_running:
            buf.write("+%s<br>" % name)
        buf.write('</div>')
        subject = "+%s; -%s" %(', +'.join(should_start), ', -'.join(should_stop))
        return (buf.getvalue(), subject)
    else:
        return (None, None)


# Schedules compose_mail to be run every 6 hours
@scheduler.scheduled_job('cron', id="compose_mail", hour=interval_str, misfire_grace_time=3600, coalesce=True,
                         max_instances=2)
def compose_mail():
    """
    Compose and send e-mail
    """
    try:
        for job in scheduler.get_jobs():
            current_time = (job.next_run_time - timedelta(hours=interval)).strftime('%Y-%m-%d %H:%M:%S')
            current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
            body, subject = _create_body(players, current_time)
            if (body is not None) and (subject is not None):
                send_mail(body, subject)
    except Exception as e:
        logging.exception(e, exc_info=True)
    finally:
        print(scheduler.print_jobs())