import logging
import typing
from datetime import datetime, timedelta

import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from player import create_players
from mail import send_mail


players = create_players()

interval = 6  # interval for job schedule
interval_str = f"*/{interval}"
scheduler = BackgroundScheduler()  # create scheduler
atexit.register(lambda: scheduler.shutdown())  # shutdown scheduler when flask stops
scheduler.start()  # start scheduler


def _create_body(players: typing.List["Player"], current_time: datetime):
    """
    Create mail html body
    :param players: list with instances of Player class
    :param current_time: current time in datetime format
    :return: html with starting and stopping player names or None
    """
    from io import StringIO
    should_start = [p.name for p in players if p.should_start(current_time)]
    should_stop = [p.name for p in players if p.should_end(current_time)]
    buf = StringIO()
    if len(should_stop) > 0 or len(should_stop) > 0:
        buf.write('<div style="width:100px;background: #b5d387;'
                  'margin:10px auto; padding: 20px 20px 20px 50px;'
                  'font-size: large;">')
        for name in should_start:
            buf.write("+%s<br>" % name)
        buf.write('</div><div style="width:100px;background: #80b7c9;'
                  'margin:10px auto; padding: 20px 20px 20px 50px;'
                  'font-size: large;">')
        for name in should_stop:
            buf.write("-%s<br>" % name)
        buf.write('</div>')
        return buf.getvalue()
    else:
        return None


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
            body = _create_body(players, current_time)
            if body is not None:
                send_mail(body)
    except Exception as e:
        logging.exception(e, exc_info=True)
    finally:
        print(scheduler.print_jobs())
