import sys
import time
from datetime import datetime, timedelta

# pip
import daemon
import daemon.pidfile

__all__ = ["start_daemon", "log_to_stdout", "interval_run"]


def log_to_stdout(*msg, end=None):
    """ログを標準(&エラー)出力

    Parameter
    ------------------------------
        *msg: object(ログ内容)
        end: str(print末尾の文字)

    Return
    ------------------------------
    """
    print(datetime.now(), *msg, end=end)
    sys.stdout.flush()
    sys.stderr.flush()


def interval_run(interval):
    """interval分ごとに関数実行
    intervalに1または60を割り切れない数を入れるとバグる(すいません)

    Parameter
    ------------------------------
        interval: int(実行間隔 -分)

    Return
    ------------------------------
        function(デコレーション後の関数)
    """

    def _deco(f):
        def _wrapper(*args, **kws):
            while 1:
                # 現在時刻と次回起動時刻
                t = datetime.now().replace(second=0, microsecond=0)
                n = t + timedelta(minutes=interval)

                # intervalの倍数ジャストに起動
                if t.minute % interval == 0:
                    f(*args, **kws)

                # 1周目 次回実行時間まで調整
                else:
                    stop = stop = interval - t.minute % interval
                    n = t + timedelta(minutes=stop)

                w = (n - datetime.now()).total_seconds()
                log_to_stdout("[INFO]", "Sleep", w, "seconds.")
                time.sleep(w)

        return _wrapper

    return _deco


def start_daemon(func, *args, pidpath=None, logpath=None, **kws):
    """対象の関数をデーモン化
    SIGTERMで終了 関数内でのエラーでは停止しない(1分sleep)

    Parameter
    ------------------------------
        func: function(デーモンにしたい関数)
        *args: list(funcで使う引数)
        pidpath: str(PIDファイルパス -default:fg)
        logpath: str(ログファイルパス -default:stdout)
        **kws: dict(funcで使うキーワード引数)

    Return
    ------------------------------
    """

    # 多重起動防止
    if pidpath:
        pid = daemon.pidfile.PIDLockFile(pidpath)
        if pid.is_locked():
            raise Exception("Process is already started.")

    # PID指定がなければフォアグラウンド
    else:
        pid = None

    # ログ
    if logpath:
        std_out = open(logpath, mode="a+", encoding="utf-8")
        std_err = std_out

    # 指定がなければ標準出力
    else:
        std_out = sys.stdout
        std_err = sys.stderr

    dc = daemon.DaemonContext(umask=0o002, pidfile=pid, stdout=std_out, stderr=std_err,)

    # 内部で実行される
    def forever():
        while 1:
            try:
                func(*args, **kws)

            # kill -SIGTERM {pid} で停止する
            except SystemExit as e:
                log_to_stdout("Killed by SIGTERM.")
                raise

            # それ以外のエラーは無視して動き続ける
            except Exception as e:
                log_to_stdout("Uncaught exception was raised, but process continue.", e)

    with dc:
        forever()

