#!/usr/bin/python3
from apscheduler.schedulers.blocking import BlockingScheduler
import tasks
from django.utils import timezone
import api


sched = BlockingScheduler()


@sched.scheduled_job("interval", minutes=1)
def timed_job_TDL():
    parkInfo = {}
    parks_calendars = api.get_parks_calendars()
    parks_conditions = api.get_parks_conditions()["schedules"]
    time = timezone.now()
    for info in parks_calendars:
        if info["date"] == time.strftime("%Y-%m-%d"):
            parkInfo[info["parkType"]] = info
    if parks_conditions[0]["open"]:
        tasks.insertdata("TDL")
        print("TDL:Task start")
    else:
        print("TDL is now closed")
    if parks_conditions[1]["open"]:
        tasks.insertdata("TDS")
        print("TDS: Task start")
    else:
        print("TDS is now closed")


sched.start()
