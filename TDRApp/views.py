from django.shortcuts import render, redirect
import requests as rq
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.timezone import localtime  # 追加
from datetime import datetime as dt
import sys

sys.path.append("../")
import api


class Top(View):
    def get(self, request):
        parksCalendars = api.get_parks_calendars()
        parksConditions = api.get_parks_conditions()
        time = localtime(timezone.now())
        print(time.strftime("%h-%m-%d"))
        parkInfos = [
            info for info in parksCalendars if info["date"] == time.strftime("%Y-%m-%d")
        ]
        nextOpenInfos = [info for info in parksCalendars if info["closedDay"] == False]
        info = []
        for schedule, ticketSale, parkInfo, nextOpenInfo in zip(
            parksConditions["schedules"],
            parksConditions["ticketSales"],
            parkInfos,
            nextOpenInfos,
        ):
            info.append(
                {
                    "schedule": schedule,
                    "ticketSale": ticketSale,
                    "parkInfo": parkInfo,
                    "nextOpenInfo": nextOpenInfo,
                }
            )
        return render(request, "top/top.html", {"parksConditions": info})


class apierror(View):
    def get(self, request):
        return render(request, "top/apierror.html")

