import os


def version(request):
    version = os.getenv("RUN_VERSION")
    if version:
        data = {"version": version}
        patch = os.getenv("PATCHTIME")
        if patch:
            data = {"version": version, "patch": patch}
    else:
        data = {"version": "UNSET"}
    return data
