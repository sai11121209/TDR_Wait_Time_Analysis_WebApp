from sys import implementation
from django.shortcuts import render, redirect
import requests as rq
from .models import *
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import datetime as dt
import sys

sys.path.append("../")
import api
from django.utils import timezone
from django.utils.timezone import localtime  # 追加

# Create your views here.


class standbytime(View):
    def get(self, request, now_open_info, attraction_name, park_type, facility_code):
        attractions = sorted(
            api.get_facilities()["attractions"], key=lambda x: x["facilityCode"],
        )
        attractions_conditions = sorted(
            api.get_facilities_conditions()["attractions"],
            key=lambda x: x["facilityCode"],
        )
        if park_type == "TDL":
            parksCondition = api.get_parks_conditions()["schedules"][0]
        else:
            parksCondition = api.get_parks_conditions()["schedules"][1]
        for attraction, attraction_conditions in zip(
            attractions, attractions_conditions
        ):
            if attraction["facilityCode"] == str(facility_code):
                info = attraction_conditions
                attraction_info = attraction
                break
        st = []
        fp = []
        fps = []
        fpe = []
        if park_type == "TDL":
            maindata = standbyTimeDataTDL.objects.filter(
                # ローカルタイム問題修正予定
                # time__startswith=localtime(timezone.now()).date(),
                time__startswith=localtime(timezone.now().date()),
                facility_code=facility_code,
            ).order_by("time")
        else:
            maindata = standbyTimeDataTDS.objects.filter(
                # ローカルタイム問題修正予定
                # time__startswith=localtime(timezone.now()).date(),
                time__startswith=timezone.now().date(),
                facility_code=facility_code,
            ).order_by("time")

        #
        print(localtime(timezone.now()))
        print(localtime(timezone.now()).date())
        for m in maindata:
            print(m)
        #

        if "中止" not in maindata.reverse()[0].operating_status:
            for std in maindata:
                if std.standby_time or std.operating_status == "運営中":
                    if std.standby_time:
                        st.append(std.standby_time)
                    else:
                        st.append(0)
                    if "fastpass" in info:
                        if std.facility_fastpass_start:
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
                    std.time.astimezone(dt.timezone(dt.timedelta(hours=+9))).strftime(
                        "%H:%M"
                    )
                    for std in standbyTimeDataTDL.objects.filter(
                        # ローカルタイム問題修正予定
                        # time__startswith=localtime(timezone.now()).date(),
                        time__startswith=timezone.now().date(),
                        facility_code=facility_code,
                    )
                ]
            else:
                t = [
                    std.time.astimezone(dt.timezone(dt.timedelta(hours=+9))).strftime(
                        "%H:%M"
                    )
                    for std in standbyTimeDataTDS.objects.filter(
                        # ローカルタイム問題修正予定
                        # time__startswith=localtime(timezone.now()).date(),
                        time__startswith=timezone.now().date(),
                        facility_code=facility_code,
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
                "data": data,
                "attractionInfo": attraction_info,
                "info": info,
                "parkType": park_type,
                "fp": fp,
                "parksCondition": parksCondition,
            },
        )

