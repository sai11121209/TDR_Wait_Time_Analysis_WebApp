import sys
import os
import django
import datetime
import api


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TDRApp.settings")


def insertdata(parkType):
    django.setup()
    from standbytime.models import standbyTimeDataTDL, standbyTimeDataTDS

    attractions = None
    attractions_conditions = None
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
                    if "一時運営中止" in operating_status:
                        standby_time = -1
                    elif "案内終了" in operating_status:
                        standby_time = -0.7
                    else:
                        standby_time = -0.3
                    operating_status_start = (
                        datetime.datetime.strptime(
                            attractions_condition["operatings"][0]["startAt"],
                            "%Y-%m-%dT%H:%M:%S.%fZ",
                        )
                        + datetime.timedelta(hours=9)
                    ).strftime("%H:%M")
                    operating_status_end = (
                        datetime.datetime.strptime(
                            attractions_condition["operatings"][0]["endAt"],
                            "%Y-%m-%dT%H:%M:%S.%fZ",
                        )
                        + datetime.timedelta(hours=9)
                    ).strftime("%H:%M")
            elif attractions_condition["standbyTimeDisplayType"] == "NORMAL":
                try:
                    standby_time = attractions_condition["standbyTime"]
                    operating_status = "運営中"
                except:
                    operating_status = "準備中"
                    operating_status_start = (
                        datetime.datetime.strptime(
                            attractions_condition["operatings"][0]["startAt"],
                            "%Y-%m-%dT%H:%M:%S.%fZ",
                        )
                        + datetime.timedelta(hours=9)
                    ).strftime("%H:%M")
                    operating_status_end = (
                        datetime.datetime.strptime(
                            attractions_condition["operatings"][0]["endAt"],
                            "%Y-%m-%dT%H:%M:%S.%fZ",
                        )
                        + datetime.timedelta(hours=9)
                    ).strftime("%H:%M")
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
                standby_time = 0
                operating_status_start = (
                    datetime.datetime.strptime(
                        attractions_condition["operatings"][0]["startAt"],
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                    )
                    + datetime.timedelta(hours=9)
                ).strftime("%H:%M")
                operating_status_end = (
                    datetime.datetime.strptime(
                        attractions_condition["operatings"][0]["endAt"],
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                    )
                    + datetime.timedelta(hours=9)
                ).strftime("%H:%M")
            if parkType == "TDL":
                standbyTimeDataTDL.objects.create(
                    facility_code=attractions_condition["facilityCode"],
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
                    facility_code=attractions_condition["facilityCode"],
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
