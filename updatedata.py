import sys
import os
import django
import datetime


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TDRApp.settings")


def updatedata():
    django.setup()
    from standbytime.models import standbyTimeDataTDL, standbyTimeDataTDS

    check = (
        input(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: UPDATE THE DATABASE. HAVE YOU BACK UP DATABASE? (yes, no): "
        )
        == "yes"
    )
    if check:
        # 一時運営中止の待ち時間を-1に修正
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE TASK START"
        )
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA ACQUISITION START: TDL (TASKCASE:1 CLOSE_NOTICE)"
        )
        updateTDL = standbyTimeDataTDL.objects.filter(operating_status="一時運営中止")
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA ACQUISITION CLEAR: TDL (TASKCASE:1 CLOSE_NOTICE) RESULT: {len(updateTDL)}rows"
        )
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA ACQUISITION START: TDS (TASKCASE:1 CLOSE_NOTICE)"
        )
        updateTDS = standbyTimeDataTDS.objects.filter(operating_status="一時運営中止")
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA ACQUISITION CLEAR: TDS (TASKCASE:1 CLOSE_NOTICE) RESULT: {len(updateTDS)}rows"
        )
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE START: TDL (TASKCASE:1 CLOSE_NOTICE)"
        )
        updateTDL.update(standby_time=-1)
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE CLEAR: TDL (TASKCASE:1 CLOSE_NOTICE)"
        )
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE START: TDS (TASKCASE:1 CLOSE_NOTICE)"
        )
        updateTDS.update(standby_time=-1)
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE CLEAR: TDS (TASKCASE:1 CLOSE_NOTICE)"
        )

        # 案内中止の待ち時間を-0.7に修正
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA ACQUISITION START: TDL (TASKCASE:2 CLOSE)"
        )
        updateTDL = standbyTimeDataTDL.objects.filter(operating_status="案内終了")
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA ACQUISITION CLEAR: TDL (TASKCASE:2 CLOSE) RESULT: {len(updateTDL)}rows"
        )
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA ACQUISITION START: TDS (TASKCASE:2 CLOSE)"
        )
        updateTDS = standbyTimeDataTDS.objects.filter(operating_status="案内終了")
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA ACQUISITION CLEAR: TDS (TASKCASE:2 CLOSE) RESULT: {len(updateTDS)}rows"
        )
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE START: TDL (TASKCASE:2 CLOSE)"
        )
        updateTDL.update(standby_time=-0.7)
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE CLEAR: TDL (TASKCASE:2 CLOSE)"
        )
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE START: TDS (TASKCASE:2 CLOSE)"
        )
        updateTDS.update(standby_time=-0.7)
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE CLEAR: TDS (TASKCASE:2 CLOSE)"
        )

        # 準備中の待ち時間を-0.3に修正
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA ACQUISITION START: TDL (TASKCASE:3 PREPARATION)"
        )
        updateTDL = standbyTimeDataTDL.objects.filter(operating_status="準備中")
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA ACQUISITION CLEAR: TDL (TASKCASE:3 PREPARATION) RESULT: {len(updateTDL)}rows"
        )
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA ACQUISITION START: TDS (TASKCASE:3 PREPARATION)"
        )
        updateTDS = standbyTimeDataTDS.objects.filter(operating_status="準備中")
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA ACQUISITION CLEAR: TDS (TASKCASE:3 PREPARATION) RESULT: {len(updateTDS)}rows"
        )
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE START: TDL (TASKCASE:3 PREPARATION)"
        )
        updateTDL.update(standby_time=-0.3)
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE CLEAR: TDL (TASKCASE:3 PREPARATION)"
        )
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE START: TDS (TASKCASE:3 PREPARATION)"
        )
        updateTDS.update(standby_time=-0.3)
        print(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: DATABASE DATA UPDATE CLEAR: TDS (TASKCASE:3 PREPARATION)"
        )
    else:
        print(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: UPDATE TASK STOP")


if __name__ == "__main__":
    pass

updatedata()
