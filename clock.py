#!/usr/bin/python3
from apscheduler.schedulers.blocking import BlockingScheduler
import tasks
from django.utils import timezone
import api

# gitPush時コメンとアウト外す
import syslog

sched = BlockingScheduler()
averageStatus = {"TDL": True, "TDS": True}


@sched.scheduled_job("interval", minutes=1)
def timed_job_TDR():
    parkInfo = {}
    parks_calendars = api.get_parks_calendars()
    parks_conditions = api.get_parks_conditions()["schedules"]
    time = timezone.now()
    for info in parks_calendars:
        if info["date"] == time.strftime("%Y-%m-%d"):
            parkInfo[info["parkType"]] = info
    if parks_conditions[0]["open"]:
        averageStatus["TDL"] = True
        print("TDL:Task start")
        syslog.syslog("TDL:Task start")
        tasks.insertdata("TDL")
    else:
        print("TDL is now closed")
        syslog.syslog("TDL is now closed")
        if averageStatus["TDL"]:
            averageStatus["TDL"] = tasks.insertdataAverage("TDL")

    if parks_conditions[1]["open"]:
        averageStatus["TDS"] = True
        print("TDS: Task start")
        syslog.syslog("TDS: Task start")
        tasks.insertdata("TDS")
    else:
        print("TDS is now closed")
        syslog.syslog("TDS is now closed")
        if averageStatus["TDS"]:
            averageStatus["TDS"] = tasks.insertdataAverage("TDS")


timed_job_TDR()
sched.start()
