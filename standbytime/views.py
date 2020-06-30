from django.shortcuts import render, redirect
import requests as rq
from .models import *
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import datetime as dt
import sys

sys.path.append("../")
import api

# Create your views here.


class standbytime(View):
    def get(self, request, now_open_info, attraction_name, park_type, facility_code):
        attractions = api.get_facilities()["attractions"]
        if park_type == "TDL":
            parksCalendars = api.get_parks_calendars()[0]
        else:
            parksCalendars = api.get_parks_calendars()[1]
        for attraction in attractions:
            if attraction["name"] == attraction_name:
                info = attraction
                break
        st = []
        fp = []
        fps = []
        fpe = []
        if park_type == "TDL":
            maindata = standbyTimeDataTDL.objects.filter(
                facility_code=facility_code
            ).order_by("time")
        else:
            maindata = standbyTimeDataTDS.objects.filter(
                facility_code=facility_code
            ).order_by("time")
        if "中止" not in maindata.reverse()[0].operating_status:
            for std in maindata:
                if std.standby_time or std.operating_status == "運営中":
                    if std.standby_time:
                        st.append(std.standby_time)
                    else:
                        st.append(0)
                    if info["fastpass"]:
                        if std.facility_fastpass_start:
                            # .strftime("%H:%M")
                            fps.append(std.facility_fastpass_start.strftime("%H:%M"))
                            fpe.append(std.facility_fastpass_end.strftime("%H:%M"))
                        else:
                            fps.append(0)
                            fpe.append(0)
                else:
                    st.append(-1)
            fp = [fps, fpe]
            if park_type == "TDL":
                t = [
                    std.time.strftime("%H:%M")
                    for std in standbyTimeDataTDL.objects.filter(
                        facility_code=facility_code
                    )
                ]
            else:
                t = [
                    std.time.strftime("%H:%M")
                    for std in standbyTimeDataTDS.objects.filter(
                        facility_code=facility_code
                    )
                ]
            stmeans = [i for i in st if i != -1]
            stmean = int(sum(stmeans) / len(stmeans))
            if -1 in st:
                stin = int((len(stmeans) / len(st)) * 100)
            else:
                stin = 100
            data = [st, t, stmean, stin]
        else:
            data = maindata.reverse()[0].operating_status
        return render(
            request,
            "standbytime/standbytime.html",
            {
                "now_open_info": now_open_info,
                "data": data,
                "info": info,
                "parkType": park_type,
                "fp": fp,
            },
        )

