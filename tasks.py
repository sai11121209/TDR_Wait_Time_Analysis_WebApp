import sys
import os
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TDRApp.settings")  # 自分のsettings.py]


def insertdata():
    django.setup()
    from standbytime.models import standbyTimeDataTDS

    standbyTimeDataTDS.objects.create(
        facility_code=156,
        standby_time=5,
        time="2020-02-18 20:48:00.000000",
        operating_status="運営中",
        operating_status_start="10:00:00.000000",
        operating_status_end="21:00:00.000000",
        facility_fastpass_status=None,
        facility_fastpass_start=None,
        facility_fastpass_end=None,
    )


if __name__ == "__main__":
    insertdata()
