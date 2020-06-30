from apscheduler.schedulers.blocking import BlockingScheduler
import tasks
import requests as rq
from django.utils import timezone
from django.utils.timezone import localtime  # 追加
from datetime import datetime as dt
import api

sched = BlockingScheduler()


@sched.scheduled_job("interval", minutes=1)
def timed_job_TDL():
    parkInfo = {}
    parks_calendars = api.get_parks_calendars()
    time = localtime(timezone.now())
    for info in parks_calendars:
        if info["date"] == time.strftime("%Y-%m-%d"):
            parkInfo[info["parkType"]] = info
    if (
        parkInfo["TDL"]["openTime"]
        <= time.strftime("%H:%M")
        <= parkInfo["TDL"]["closeTime"]
    ):
        tasks.insertdata("TDL", parkInfo)
        print(parkInfo)
        print("This job is run every three minutes.1")
    else:
        print("This job is run every three minutes.TDL")
    if (
        parkInfo["TDS"]["openTime"]
        <= time.strftime("%H:%M")
        <= parkInfo["TDS"]["closeTime"]
    ):
        tasks.insertdata("TDS", parkInfo)
        print(parkInfo)
        print("This job is run every three minutes.1")
    else:
        print("This job is run every three minutes.TDS")


sched.start()
