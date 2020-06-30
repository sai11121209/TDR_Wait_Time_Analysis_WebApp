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
    print(time.strftime("%H:%M"))
    print(type(time.strftime("%H:%M")))
    print(dt.strptime(parkInfo["TDL"]["openTime"], "%H:%M"))
    print(type(dt.strptime(parkInfo["TDL"]["openTime"], "%H:%M")))
    if (
        dt.strptime(parkInfo["TDL"]["openTime"], "%H:%M")
        <= time.strftime("%H:%M")
        <= dt.strptime(parkInfo["TDL"]["closeTime"], "%H:%M")
    ):
        tasks.insertdata("TDL", parkInfo)
        print(parkInfo)
        print("This job is run every three minutes.1")
    else:
        print("This job is run every three minutes.TDL")
    if (
        dt.strptime(parkInfo["TDS"]["openTime"], "%H:%M")
        <= time.strftime("%H:%M")
        <= dt.strptime(parkInfo["TDS"]["closeTime"], "%H:%M")
    ):
        tasks.insertdata("TDS", parkInfo)
        print(parkInfo)
        print("This job is run every three minutes.1")
    else:
        print("This job is run every three minutes.TDS")


sched.start()
