import os


def version(request):
    version = os.getenv("RUN_VERSION")
    if version:
        version = {"version": version}
        patch = os.getenv("PATCHTIME")
        if patch:
            version["patch"] = patch
    else:
        version = {"version": "UNSET"}
    return version


def maintenance(request):
    maintenance_time_end = os.getenv("MAINTENANCE_TIME_END")
    if maintenance_time_end:
        maintenance_time_end = {"maintenance_time_end": maintenance_time_end}
    else:
        maintenance_time_end = {"maintenance_time_end": "未定"}
    return maintenance_time_end


def attention_message(request):
    attention_message = os.getenv("ATTENTION_MESSAGE")
    if attention_message:
        attention_message = {"attention_message": attention_message}
    else:
        attention_message = {"attention_message": ""}
    return attention_message
