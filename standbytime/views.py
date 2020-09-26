import sys
from django.shortcuts import render, redirect
from .models import standbyTimeDataTDL, standbyTimeDataTDS
from django.views import View
from django.utils import timezone
import datetime as dt
import pandas as pd
import numpy as np


sys.path.append("../")
import api


# Create your views here.


class standbytime(View):
    def get_standbytime_group(self, date, park_type, facility_code):
        if park_type == "TDL":
            return standbyTimeDataTDL.objects.filter(
                time__startswith=date, facilityCode=facility_code,
            ).order_by("time")
        else:
            return standbyTimeDataTDS.objects.filter(
                time__startswith=date, facilityCode=facility_code,
            ).order_by("time")

    def get_standbytime_time(self, maindata, opentime):
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
        mainDF = mainDF.merge(dateDF, how="outer", left_index=True, right_index=True)
        mean = int(mainDF.mean()["standby_time"])
        return mainDF.fillna(-0.5), mean

    def make_standbytime_time_table(self, day, opentime, park_type, facility_code):
        try:
            maindata = self.get_standbytime_group(
                timezone.now().date() + dt.timedelta(days=-day),
                park_type,
                facility_code,
            ).values()
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
            maindata = mainDF.merge(
                dateDF, how="outer", left_index=True, right_index=True
            )
            mean = int(mainDF.mean()["standby_time"])
            return [
                maindata.fillna(-0.5)[["standby_time"]],
                (timezone.now().date() + dt.timedelta(days=-day)).strftime("%Y-%m-%d"),
                mean,
            ]
        except:
            pass

    def return_time(self, mainDF, DF):
        x = np.arange(len(DF))
        x[DF == -1] = 0
        np.maximum.accumulate(x, out=x)
        left = x
        DF_re = DF[::-1]
        x = np.arange(len(DF))
        x[DF_re == -1] = 0
        np.maximum.accumulate(x, out=x)
        right = len(DF) - 1 - x[::-1]
        y = right
        y -= left + 1
        y[x == 0] = 0
        retime = np.unique(y[y > 1])
        x = np.arange(len(mainDF))
        x[mainDF.standby_time <= -0.5] = 0
        time = dt.datetime.strptime(mainDF.index[max(x)], "%H:%M")
        redatas = {
            "count": len(retime),
            "max": max(retime),
            "max_time": time + dt.timedelta(minutes=int(max(retime))),
            "min": min(retime),
            "min_time": time + dt.timedelta(minutes=int(min(retime))),
            "avg": int(np.average(retime)),
            "avg_stime": time + dt.timedelta(minutes=int(np.average(retime) - 5)),
            "avg_etime": time + dt.timedelta(minutes=int(np.average(retime) + 5)),
        }
        return redatas

    def get(self, request, park_type, facility_code):
        try:
            data_today = []
            fp = []
            attractions = pd.DataFrame(list(api.get_facilities()["attractions"]))
            attractions_conditions = pd.DataFrame(
                list(api.get_facilities_conditions()["attractions"])
            )
            attractions_pd = pd.merge(
                attractions, attractions_conditions, on="facilityCode", how="left",
            )
            attraction_pd = attractions_pd[
                attractions_pd["facilityCode"] == facility_code
            ]
            attraction_pd = attraction_pd.astype(object).where(
                (pd.notnull(attraction_pd)), None
            )
            attraction = attraction_pd.to_dict(orient="records")[0]
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
                opentime = api.get_parks_calendars()[0]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
                opentime = api.get_parks_calendars()[1]

            maindata = self.get_standbytime_group(
                timezone.now().date(), park_type, facility_code
            )
            if maindata:
                if "公演中止" not in maindata.reverse()[0].operating_status:
                    mainDF, standby_mean = self.get_standbytime_time(
                        maindata.values(), opentime
                    )
                    table_data = []
                    for datas in list(mainDF.index.values):
                        try:
                            table_data.append(
                                [mainDF.loc[datas].name, mainDF.loc[datas].standby_time]
                            )
                        except:
                            table_data.append([datas, 0.5])
                    data_today = [mainDF, standby_mean, table_data]
                    st_datas = [
                        self.make_standbytime_time_table(
                            day, opentime, park_type, facility_code
                        )
                        for day in range(1, 14)
                    ]
                    # 平均値算出部分
                    vacant = []
                    redatas = {}
                    try:
                        avgDF = st_datas[0][0]["standby_time"]
                        for i in range(1, len(st_datas)):
                            try:
                                avgDF = pd.concat(
                                    [avgDF, st_datas[i][0]["standby_time"]]
                                )
                            except:
                                pass
                        if "一時運営中止" in maindata.reverse()[0].operating_status:
                            redatas = self.return_time(mainDF, avgDF)
                        avgDF = avgDF.replace([-0.3, -0.5, -0.7, -1], np.nan)
                        avgDF = avgDF.groupby("time").mean()
                        avgDF = avgDF.replace(np.nan, -1)
                        vacant = (
                            avgDF[timezone.now().strftime("%H:%M")]
                            >= attraction["standbyTime"]
                        )
                    except:
                        pass
                else:
                    data_today = attraction["operatings"][0]["operatingStatusMessage"]
                return render(
                    request,
                    "standbytime/standbytime.html",
                    {
                        "now_time": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "data_today": data_today,
                        "st_datas": st_datas,
                        "avg_datas": avgDF,
                        "attraction": attraction,
                        "park_type": park_type,
                        "fp": fp,
                        "now_open_info": parks_condition,
                        "weatherData": api.getWeather(),
                        "vacant": vacant,
                        "return_datas": redatas,
                        # 閉園時用
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
                        "weatherData": api.getWeather(),
                    },
                )
        except:
            return redirect("error")
