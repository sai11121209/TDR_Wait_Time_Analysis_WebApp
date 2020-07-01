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
import urllib.parse

# Create your views here.


class Home(View):
    def get(self, request, park_type):
        if park_type == "TDL":
            parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
        else:
            parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
        attractions = sorted(
            api.get_facilities()["attractions"], key=lambda x: x["facilityCode"],
        )
        attractions_conditions = sorted(
            api.get_facilities_conditions()["attractions"],
            key=lambda x: x["facilityCode"],
        )
        f_attractions_info = []
        for attraction, attraction_conditions in zip(
            attractions, attractions_conditions
        ):
            if attraction["parkType"] == park_type:
                f_attractions_info.append(
                    {
                        "attraction": attraction,
                        "attraction_conditions": attraction_conditions,
                    }
                )
        return render(
            request,
            "information/home.html",
            {
                "attractions": f_attractions_info,
                "park_type": park_type,
                "parks_condition": parks_condition,
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


class Map(View):
    def get(self, request, now_open_info, attraction_name, park_type, facility_code):
        attractions = api.get_facilities()["attractions"]
        for attraction in attractions:
            if attraction["facilityCode"] == str(facility_code):
                info = attraction
                break
        return render(
            request,
            "information/map.html",
            {"now_open_info": now_open_info, "info": info},
        )

