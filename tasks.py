import sys
import os
import django
import datetime
import api
import pandas as pd


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TDRApp.settings")


def insertdata(parkType):
    django.setup()
    from standbytime.models import standbyTimeDataTDL, standbyTimeDataTDS

    attractions = pd.DataFrame(list(api.get_facilities()["attractions"]))
    attractions_conditions = pd.DataFrame(
        list(api.get_facilities_conditions()["attractions"])
    )
    attractions_pd = pd.merge(
        attractions, attractions_conditions, on="facilityCode", how="left",
    )
    attractions = attractions_pd[attractions_pd["parkType"] == parkType].to_dict(
        orient="records"
    )
    attractions.sort(key=lambda x: x["facilityCode"])
    for attraction in attractions:
        standby_time = None
        operating_status_start = None
        operating_status_end = None
        facility_fastpass_status = None
        facility_fastpass_start = None
        facility_fastpass_end = None
        if attraction["standbyTimeDisplayType"] == "HIDE":
            if "standbyTime" in attraction:
                standby_time = attraction["standbyTime"]
                try:
                    operating_status = attraction["operatings"][0][
                        "operatingStatusMessage"
                    ]
                except:
                    operating_status = None
            elif "facilityStatusMessage" in attraction:
                operating_status = attraction["facilityStatusMessage"]
            else:
                operating_status = attraction["operatings"][0]["operatingStatusMessage"]
                if "準備中" == operating_status:
                    standby_time = -0.3
                elif "案内終了" == operating_status:
                    standby_time = -0.7
                else:
                    standby_time = -1
                operating_status_start = (
                    datetime.datetime.strptime(
                        attraction["operatings"][0]["startAt"], "%Y-%m-%dT%H:%M:%S.%fZ",
                    )
                    + datetime.timedelta(hours=9)
                ).strftime("%H:%M")
                operating_status_end = (
                    datetime.datetime.strptime(
                        attraction["operatings"][0]["endAt"], "%Y-%m-%dT%H:%M:%S.%fZ",
                    )
                    + datetime.timedelta(hours=9)
                ).strftime("%H:%M")
        elif attraction["standbyTimeDisplayType"] == "NORMAL":
            try:
                standby_time = attraction["standbyTime"]
                operating_status = "運営中"
            except:
                operating_status = "準備中"
                operating_status_start = (
                    datetime.datetime.strptime(
                        attraction["operatings"][0]["startAt"], "%Y-%m-%dT%H:%M:%S.%fZ",
                    )
                    + datetime.timedelta(hours=9)
                ).strftime("%H:%M")
                operating_status_end = (
                    datetime.datetime.strptime(
                        attraction["operatings"][0]["endAt"], "%Y-%m-%dT%H:%M:%S.%fZ",
                    )
                    + datetime.timedelta(hours=9)
                ).strftime("%H:%M")
            if "fastPassStatus" in attraction:
                if attraction["standbyTimeDisplayType"] == "TICKETING":
                    facility_fastpass_start = str(attraction["fastPassStartAt"])
                    facility_fastpass_end = str(attraction["fastPassEndAt"])
        else:
            operating_status = "運営中"
            standby_time = 0
            try:
                operating_status_start = (
                    datetime.datetime.strptime(
                        attraction["operatings"][0]["startAt"], "%Y-%m-%dT%H:%M:%S.%fZ",
                    )
                    + datetime.timedelta(hours=9)
                ).strftime("%H:%M")
                operating_status_end = (
                    datetime.datetime.strptime(
                        attraction["operatings"][0]["endAt"], "%Y-%m-%dT%H:%M:%S.%fZ",
                    )
                    + datetime.timedelta(hours=9)
                ).strftime("%H:%M")
            except:
                pass
        if parkType == "TDL":
            standbyTimeDataTDL.objects.create(
                facilityCode=attraction["facilityCode"],
                standby_time=standby_time,
                operating_status=operating_status,
                operating_status_start=operating_status_start,
                operating_status_end=operating_status_end,
                facility_fastpass_status=facility_fastpass_status,
                facility_fastpass_start=facility_fastpass_start,
                facility_fastpass_end=facility_fastpass_end,
            )
            print("TDL:Task completed")
        else:
            standbyTimeDataTDS.objects.create(
                facilityCode=attraction["facilityCode"],
                standby_time=standby_time,
                operating_status=operating_status,
                operating_status_start=operating_status_start,
                operating_status_end=operating_status_end,
                facility_fastpass_status=facility_fastpass_status,
                facility_fastpass_start=facility_fastpass_start,
                facility_fastpass_end=facility_fastpass_end,
            )
            print("TDS:Task completed")


if __name__ == "__main__":
    pass
