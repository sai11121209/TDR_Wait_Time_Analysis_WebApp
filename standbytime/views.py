import sys
from django.shortcuts import render, redirect
from .models import standbyTimeDataTDL, standbyTimeDataTDS
from django.views import View
from django.utils import timezone
import datetime as dt
import pandas as pd


sys.path.append("../")
import api


# Create your views here.


class standbytime(View):
    def get_standbytime_group(self, date, park_type, facility_code):
        if park_type == "TDL":
            return standbyTimeDataTDL.objects.filter(
                time__startswith=date, facility_code=facility_code,
            ).order_by("time")
        else:
            return standbyTimeDataTDS.objects.filter(
                time__startswith=date, facility_code=facility_code,
            ).order_by("time")

    def get_standbytime_time(self, maindata, info, opentime):
        dateDF = pd.DataFrame(
            {
                "time": pd.date_range(
                    opentime["openTime"], opentime["closeTime"], freq="T",
                )
            }
        )
        dateDF["time"] = dateDF["time"].dt.strftime("%H:%M")
        dateDF = dateDF.set_index("time")
        mainDF = pd.DataFrame(maindata)
        mainDF["time"] = mainDF["time"].dt.strftime("%H:%M")
        mainDF = mainDF.set_index("time")
        pd.set_option("display.max_rows", None)
        mainDF = mainDF.merge(dateDF, how="outer", left_index=True, right_index=True)
        mean = int(mainDF.mean()["standby_time"])
        return mainDF.fillna(-0.5), mean

    def get(self, request, attraction_name, park_type, facility_code):
        try:
            data_today = []
            data_yesterday = []
            fp = []
            attractions = sorted(
                api.get_facilities()["attractions"], key=lambda x: x["facilityCode"],
            )
            attractions_conditions = sorted(
                api.get_facilities_conditions()["attractions"],
                key=lambda x: x["facilityCode"],
            )
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
                opentime = api.get_parks_calendars()[0]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
                opentime = api.get_parks_calendars()[1]
            for attraction, attraction_conditions in zip(
                attractions, attractions_conditions
            ):
                if attraction["facilityCode"] == str(facility_code):
                    info = attraction_conditions
                    attraction_info = attraction
                    break
            maindata = self.get_standbytime_group(
                timezone.now().date(), park_type, facility_code
            )
            if maindata:
                if "中止" not in maindata.reverse()[0].operating_status:
                    maindata, standby_mean = self.get_standbytime_time(
                        maindata.values(), info, opentime
                    )
                    table_data = []
                    for datas in list(maindata.index.values):
                        table_data.append(
                            [maindata.loc[datas].name, maindata.loc[datas].standby_time]
                        )
                    data_today = [maindata, standby_mean, table_data]
                    maindata = self.get_standbytime_group(
                        timezone.now().date() + dt.timedelta(days=-1),
                        park_type,
                        facility_code,
                    )
                    maindata, standby_mean = self.get_standbytime_time(
                        maindata.values(), info, opentime
                    )
                    table_data = []
                    for datas in list(maindata.index.values):
                        table_data.append(
                            [maindata.loc[datas].name, maindata.loc[datas].standby_time]
                        )
                    data_yesterday = [maindata, standby_mean, table_data]
                    maindata = self.get_standbytime_group(
                        timezone.now().date() + dt.timedelta(days=-7),
                        park_type,
                        facility_code,
                    )
                    maindata, standby_mean = self.get_standbytime_time(
                        maindata.values(), info, opentime
                    )
                    table_data = []
                    for datas in list(maindata.index.values):
                        table_data.append(
                            [maindata.loc[datas].name, maindata.loc[datas].standby_time]
                        )
                    data_lastweek = [maindata, standby_mean, table_data]
                else:
                    data_today = info["operatings"][0]["operatingStatusMessage"]
                return render(
                    request,
                    "standbytime/standbytime.html",
                    {
                        "now_time": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "data_today": data_today,
                        "data_yesterday": data_yesterday,
                        "data_lastweek": data_lastweek,
                        "attraction_info": attraction_info,
                        "info": info,
                        "park_type": park_type,
                        "fp": fp,
                        "now_open_info": parks_condition,
                        # "now_open_info": True,
                    },
                )
            else:
                return render(
                    request,
                    "standbytime/standbytime.html",
                    {
                        "now_time": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "attraction_info": attraction_info,
                        "info": info,
                        "park_type": park_type,
                        "now_open_info": parks_condition,
                    },
                )
        except:
            return redirect("error")

