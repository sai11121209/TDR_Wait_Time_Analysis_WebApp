from apscheduler.schedulers.blocking import BlockingScheduler
from standbytime.models import *
import tasks

sched = BlockingScheduler()


@sched.scheduled_job("interval", minutes=1)
def timed_job():
    tasks.insertdata()
    print("This job is run every three minutes.")


sched.start()
