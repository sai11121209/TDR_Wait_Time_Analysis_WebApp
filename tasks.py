import sys
import os
import django
import requests as rq
from django.utils import timezone
from django.utils.timezone import localtime  # 追加
import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TDRApp.settings")


def insertdata(parkType):
    django.setup()
    from standbytime.models import standbyTimeDataTDL, standbyTimeDataTDL

    print(parkType)
    headers = {
        "Host": "api-portal.tokyodisneyresort.jp",
        "X-PORTAL-DEVICE-ID": "OWNlNjIwT/EFcUXy8B9esqO2oh0JN7Rl0xIBYOvLCxgTPc8VuQi8Zosvw3OTfZKdGLZ/4mRAs3mgz8yuTuZdTvBtu2X/Rg==",
        "x-api-key": "818982cd6a62e7927700a4fbabcd4534a4657a422711a83c725433839b172371",
        "Accept-Language": "ja-JP;q=1.0, en-JP;q=0.9, en-US;q=0.8",
        "X-PORTAL-OS-VERSION": "iOS 13.3",
        "X-PORTAL-APP-VERSION": "1.4.0",
        "User-Agent": "TokyoDisneyResortApp/1.2.0 iOS/13.3",
        "Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
        "Connection": "keep-alive",
        "X-PORTAL-LANGUAGE": "ja",
        "Accept": "application/json",
        "Cookie": "bm_sv=1E5E7EEE8A665F7D00B6072198D01C32~or1cFA6oWCRaLGF5U+PiyzlUQZFHqGbYY2xjFzcgPHb7CbXTl88Vof33l8RBLvXyNKiUO4ecHEC9ujMRZ+9/N6mO1SVLgVtTmrZjgI8zR9CR7aX8cOvTHxr29VKRgWDxRBQqrORbDu5SlLilLpM+fIhwMcqwIpZpsCFD33644GU=; ak_bmsc=EE57BE32368D813C4176BCC3349245F2687003D5524B0000931E465EDE0A567A~plrr9M3sfCeOJ/dxvhjmeWwNyPJf+iewS9MazRIhyUova0m1+dzLb49bzrA3zekYVUEHA7V3qztwyIk5fiGzmc52rDKVyLJ/5bdVSNVjl+Bs7h0WOLix6N3S6BV3MdmBb2TLp1hJHS6Jt8Ljmx5V+wxJIp3qnnC9QB0jVy2V+SYHRcDSWUEoSiAndTf4F1CM2s5nPU9QSLsNTpp9fDdzvscXB9AqmlNzRVf432azFSY/behmxOQ0f+sw9SjyP+NjpQ; bm_sz=7819C1854A0F48DBE8DFD28F3869D6F3~YAAQzgNwaMdrNydwAQAANsVhQQZs3LCWESk6MgqDl/RHgoPXIOZJYIh19MmdWOmF8V1EjWhdCh64FVfRs1bkzjCjSanMIn6XE+fex/yzWv6w6XBJnvOZMXb467Pt2rQrr4WKjrOzR93loalJOTJ8214fu/AkkGZJqqc/Y93kLLFA4aBmbzEEo5Xsw3eBFj7pgrnf8f/6PpoYAg==; __pp_uid=BN3cUW5cISDBZlAvGQYsw1wRfMdZ8im7; _ga=GA1.2.564559699.1568211623; _abck=04B8A88ACEB0AE4C77FB77FEA817C5BA~0~YAAQ1QNwaAdanH1uAQAAZbaKTAODhqobXnCP2Lq7CC+rwJjSyKE6ZWEAIWF8tRZnY6WymJdhFQMbWg8pyE8q2p8NBVWsu5RL5/t58TKBOLQDRvbfLnDEcDgfmqI/jm029CQCwoGPme0eTA+ioFb10xDNa3NkIiKLSba8f+C+ezuRptfVBWCYPD4kScy6Vci+Nrvoz/jDh5/PggGNreA1gL4Pj6y/cCYVhX8u6Sc4iqe7R4yffQwbRqPwpu/rSFjLkBdWyQlUxKkIj6QELk0Ro/R2W5c10c1XuB386WIRsRQYGHlJOGMbzSQ87053jnZMR5Poi/FLwtt8uJ9Hxao7YTY=~-1~-1~-1; _gcl_au=1.1.367463172.1577536503; _a1_f=cf032510-7155-4ef3-87f8-902543306e6e; __td_signed=true",
        "X-PORTAL-AUTH": "MDVhMjVm8IMOOueTBWpIYxpIipWh4A259zH4SGgTyCyvn5XTFO6I+Xkpjhvj438uWYscUFxTPSYAwVSvfwX5FNT3ZC/YdA==",
    }
    url = "https://api-portal.tokyodisneyresort.jp/rest/v2/facilities"
    url2 = "https://api-portal.tokyodisneyresort.jp/rest/v2/facilities/conditions"
    url3 = "https://api-portal.tokyodisneyresort.jp/rest/v1/parks/calendars"

    attractions = sorted(
        rq.get(url, headers=headers).json(strict=False)["attractions"],
        key=lambda x: x["facilityCode"],
    )
    attractions_conditions = sorted(
        rq.get(url2, headers=headers).json(strict=False)["attractions"],
        key=lambda x: x["facilityCode"],
    )
    parksCalendars = rq.get(url3, headers=headers).json(strict=False)
    time = localtime(timezone.now())
    parkInfo = {}
    for info in parksCalendars:
        if info["date"] == time.strftime("%Y-%m-%d"):
            parkInfo[info["parkType"]] = info
    for attractions_condition, attraction in zip(attractions_conditions, attractions):
        if parkInfo[attraction["parkType"]]["closedDay"] == False and dt.strptime(
            parkInfo[attraction["parkType"]]["openTime"], "%H:%M"
        ) <= time.strftime("%H:%M") <= dt.strptime(
            parkInfo[attraction["parkType"]]["closeTime"], "%H:%M"
        ):
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
