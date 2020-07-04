import sys
import itertools
import api
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.db.models import Avg


sys.path.append("../")
from standbytime.models import standbyTimeDataTDL, standbyTimeDataTDS

# Create your views here.


class OverView(View):
    def get(self, request, park_type):
        try:
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
                attractions_overview = {
                    standby_time.facility_code: standby_time.standby_time_avg
                    if standby_time.standby_time_avg
                    else -1
                    for standby_time in standbyTimeDataTDL.objects.filter(
                        time__startswith=timezone.now().date()
                    ).annotate(standby_time_avg=Avg("standby_time"))
                }
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
                attractions_overview = {
                    standby_time.facility_code: standby_time.standby_time_avg
                    if standby_time.standby_time_avg
                    else -1
                    for standby_time in standbyTimeDataTDS.objects.filter(
                        time__startswith=timezone.now().date()
                    ).annotate(standby_time_avg=Avg("standby_time"))
                }
            attractions = sorted(
                api.get_facilities()["attractions"], key=lambda x: x["facilityCode"]
            )
            attractions_conditions = sorted(
                api.get_facilities_conditions()["attractions"],
                key=lambda x: x["facilityCode"],
            )

            f_attractions = []
            for i, attraction in enumerate(attractions):
                if attraction["parkType"] == park_type:
                    attractions[i].update(attractions_conditions[i])
                    attractions[i].update(
                        {"avg": attractions_overview[int(attraction["facilityCode"])]}
                    )
                    f_attractions.append(attraction)

            f_attractions.sort(reverse=True, key=lambda x: (x["avg"], x["name"]))
            return render(
                request,
                "information/overview.html",
                {
                    "attractions": f_attractions,
                    "park_type": park_type,
                    "parks_condition": parks_condition,
                },
            )
        except:
            return redirect("error")


class List(View):
    def get(self, request, park_type):
        try:
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
            attractions = sorted(
                api.get_facilities()["attractions"], key=lambda x: x["facilityCode"],
            )
            attractions_conditions = sorted(
                api.get_facilities_conditions()["attractions"],
                key=lambda x: x["facilityCode"],
            )
            f_attractions = []
            for i, attraction in enumerate(attractions):
                if attraction["parkType"] == park_type:
                    attractions[i].update(attractions_conditions[i])
                    f_attractions.append(attraction)

            f_attractions.sort(key=lambda x: (x["area"]["id"], x["name"]))
            attraction_groups = {
                area: list(data)
                for area, data in itertools.groupby(
                    f_attractions, lambda x: x["area"]["id"]
                )
            }
            return render(
                request,
                "information/list.html",
                {
                    "attraction_groups": attraction_groups,
                    "park_type": park_type,
                    "now_open_info": parks_condition,
                },
            )
        except:
            return redirect("error")


class Detail(View):
    def get(self, request, attraction_name, park_type, facility_code):
        try:
            attractions = api.get_facilities()["attractions"]
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
            for attraction in attractions:
                if attraction["name"] == attraction_name:
                    info = attraction
                    break
            return render(
                request,
                "information/detail.html",
                {
                    "now_open_info": parks_condition,
                    "park_type": parks_condition,
                    "info": info,
                },
            )
        except:
            return redirect("error")


class Map(View):
    def get(self, request, attraction_name, park_type, facility_code):
        try:
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
            attractions = api.get_facilities()["attractions"]
            for attraction in attractions:
                if attraction["facilityCode"] == str(facility_code):
                    info = attraction
                    break
            return render(
                request,
                "information/map.html",
                {
                    "now_open_info": parks_condition,
                    "park_type": park_type,
                    "info": info,
                },
            )
        except:
            return redirect("error")

