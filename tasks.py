import sys
import os
import django
import requests as rq
from django.utils import timezone
from django.utils.timezone import localtime  # 追加
import datetime
import api

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TDRApp.settings")


def insertdata(parkType, parksCalendars):
    django.setup()
    from standbytime.models import standbyTimeDataTDL, standbyTimeDataTDL

    attractions = sorted(
        api.get_facilities()["attractions"], key=lambda x: x["facilityCode"],
    )
    attractions_conditions = sorted(
        api.get_facilities_conditions()["attractions"], key=lambda x: x["facilityCode"],
    )
    for attractions_condition, attraction in zip(attractions_conditions, attractions):
        if attraction["parkType"] == parkType:
            standby_time = None
            operating_status_start = None
            operating_status_end = None
            facility_fastpass_status = None
            facility_fastpass_start = None
            facility_fastpass_end = None
            if attractions_condition["standbyTimeDisplayType"] == "HIDE":
                if "facilityStatusMessage" in attractions_condition:
                    operating_status = attractions_condition["facilityStatusMessage"]
                else:
                    operating_status = attractions_condition["operatings"][0][
                        "operatingStatusMessage"
                    ]
                    operating_status_start = datetime.datetime.strptime(
                        attractions_condition["operatings"][0]["startAt"],
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                    ) + datetime.timedelta(hours=9)
                    operating_status_end = datetime.datetime.strptime(
                        attractions_condition["operatings"][0]["endAt"],
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                    ) + datetime.timedelta(hours=9)
            elif attractions_condition["standbyTimeDisplayType"] == "NORMAL":
                standby_time = attractions_condition["standbyTime"]
                operating_status = "運営中"
                operating_status_start = datetime.datetime.strptime(
                    attractions_condition["operatings"][0]["startAt"],
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                ) + datetime.timedelta(hours=9)
                operating_status_end = datetime.datetime.strptime(
                    attractions_condition["operatings"][0]["endAt"],
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                ) + datetime.timedelta(hours=9)
                if "fastPassStatus" in attractions_condition:
                    if attractions_condition["standbyTimeDisplayType"] == "TICKETING":
                        facility_fastpass_start = str(
                            attractions_condition["fastPassStartAt"]
                        )
                        facility_fastpass_end = str(
                            attractions_condition["fastPassEndAt"]
                        )
            else:
                operating_status = "運営中"
                operating_status_start = datetime.datetime.strptime(
                    attractions_condition["operatings"][0]["startAt"],
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                ) + datetime.timedelta(hours=9)
                operating_status_end = datetime.datetime.strptime(
                    attractions_condition["operatings"][0]["endAt"],
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                ) + datetime.timedelta(hours=9)
            if parkType == "TDL":
                standbyTimeDataTDL.objects.create(
                    facility_code=attractions_condition["facilityCode"],
                    standby_time=standby_time,
                    time=localtime(timezone.now()),
                    operating_status=operating_status,
                    operating_status_start=operating_status_start.strftime("%H:%M"),
                    operating_status_end=operating_status_end.strftime("%H:%M"),
                    facility_fastpass_status=facility_fastpass_status,
                    facility_fastpass_start=facility_fastpass_start,
                    facility_fastpass_end=facility_fastpass_end,
                )
            else:
                standbyTimeDataTDS.objects.create(
                    facility_code=attractions_condition["facilityCode"],
                    standby_time=standby_time,
                    time=localtime(timezone.now()),
                    operating_status=operating_status,
                    operating_status_start=operating_status_start.strftime("%H:%M"),
                    operating_status_end=operating_status_end.strftime("%H:%M"),
                    facility_fastpass_status=facility_fastpass_status,
                    facility_fastpass_start=facility_fastpass_start,
                    facility_fastpass_end=facility_fastpass_end,
                )


if __name__ == "__main__":
    insertdata()
