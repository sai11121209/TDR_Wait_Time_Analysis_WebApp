from django.shortcuts import render, redirect
import requests as rq
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import sys
from django.utils.timezone import localtime  # 追加
from datetime import datetime as dt

sys.path.append("../")
from standbytime.models import *
import api

# Create your views here.


class Home(View):
    def get(self, request, park_type):
        parksCalendars = api.get_parks_calendars()
        attractions_conditions = api.get_facilities_conditions()
        time = localtime(timezone.now())
        parkInfo = None
        for info in parksCalendars:
            if (
                info["date"] == time.strftime("%Y-%m-%d")
                and info["parkType"] == park_type
            ):
                parkInfo = info
        if parkInfo:
            if (
                parkInfo["closedDay"] == False
                and parkInfo["openTime"]
                <= time.strftime("%H:%M")
                <= parkInfo["closeTime"]
            ):
                nowOpenInfo = True
            else:
                nowOpenInfo = False
        else:
            nowOpenInfo = False
        attractions = [
            attraction
            for attraction in api.get_facilities()["attractions"]
            if attraction["parkType"] == park_type
        ]
        for i, attraction in enumerate(attractions):
            if park_type == "TDL":
                st = (
                    standbyTimeDataTDL.objects.filter(
                        facility_code=attraction["facilityCode"]
                    )
                    .order_by("time")
                    .reverse()[0]
                )
            else:
                st = (
                    standbyTimeDataTDS.objects.filter(
                        facility_code=attraction["facilityCode"]
                    )
                    .order_by("time")
                    .reverse()[0]
                )

            attractions[i]["standbyTime"] = st.standby_time
            attractions[i]["operatingStatus"] = st.operating_status
            # 画面表示の順番変更時はこれ以降で入れ替えること
        return render(
            request,
            "information/home.html",
            {
                "attractions": attractions,
                "now_open_info": nowOpenInfo,
                "parkType": park_type,
            },
        )


class Detail(View):
    def get(self, request, now_open_info, attraction_name, park_type, facility_code):
        attractions = api.get_facilities()["attractions"]
        for attraction in attractions:
            if attraction["name"] == attraction_name:
                info = attraction
                break
        return render(
            request,
            "information/detail.html",
            {"now_open_info": now_open_info, "info": info},
        )
