from os import truncate
import requests as rq
import os

try:
    import local_api

    headers = local_api.headers()
except ImportError:
    headers = {
        "Host": os.environ["TDRAPI_HOST"],
        "X-PORTAL-DEVICE-ID": os.environ["TDRAPI_PORTAL_DEVICE_ID"],
        "x-api-key": os.environ["TDRAPI_API_KEY"],
        "Accept-Language": os.environ["TDRAPI_API_ACCEPT_LANGUAGE"],
        "X-PORTAL-OS-VERSION": os.environ["TDRAPI_API_PORTAL_OS_VERSION"],
        "X-PORTAL-APP-VERSION": rq.get(
            "https://itunes.apple.com/lookup?id=1313147771&country=JP"
        ).json()["results"][0]["version"],
        "Accept-Encoding": os.environ["TDRAPI_API_ACCEPT_ENCODING"],
        "Connection": os.environ["TDRAPI_API_CONNECTION"],
        "Content-Type": os.environ["TDRAPI_API_CONTENT_TYPE"],
        "User-Agent": os.environ["TDRAPI_API_USER_AGENT"],
        "X-PORTAL-LANGUAGE": os.environ["TDRAPI_API_PORTAL_LANGUAGE"],
        "Accept": os.environ["TDRAPI_API_ACCEPT"],
        "Cookie": os.environ["TDRAPI_API_COOKIE"],
        "X-PORTAL-AUTH": os.environ["TDRAPI_API_PORTAL_AUTH"],
    }


def get_version():
    return rq.get("https://itunes.apple.com/lookup?id=1313147771&country=JP").json()[
        "results"
    ][0]["version"]


def get_facilities():
    try:
        url = os.environ["TDRAPI_FACILITIES_URL"]
        headers["X-PORTAL-APP-VERSION"] = get_version
    except KeyError:
        url = local_api.facilities_url()
    count = 0
    r = rq.session()
    while True:
        try:
            data = r.get(url, headers=headers)
            print("g_f_try")
            print(data)
            return data.json()
        except:
            print("g_f_except")
            count += 1
            if count >= 3:
                return False


def get_facilities_conditions():
    try:
        url = os.environ["TDRAPI_FACILITIES_CONDITIONS_URL"]
        headers["X-PORTAL-APP-VERSION"] = get_version
    except KeyError:
        url = local_api.facilities_conditions_url()
    count = 0
    r = rq.session()
    while True:
        try:
            data = r.get(url, headers=headers)
            print("g_f_c_try")
            print(data)
            return data.json()
        except:
            print("g_f_c_except")
            count += 1
            if count >= 3:
                return False


def get_parks_conditions():
    try:
        url = os.environ["TDRAPI_PARKS_CONDITIONS_URL"]
        headers["X-PORTAL-APP-VERSION"] = get_version
    except KeyError:
        url = local_api.parks_conditions_url()
    count = 0
    r = rq.session()
    while True:
        try:
            data = r.get(url, headers=headers)
            print("g_p_co_try")
            print(data)
            return data.json()
        except:
            print("g_p_co_except")
            count += 1
            if count >= 3:
                return False


def get_parks_calendars():
    try:
        url = os.environ["TDRAPI_PARKS_CALENDARS_URL"]
        headers["X-PORTAL-APP-VERSION"] = get_version
    except KeyError:
        url = local_api.parks_calendars_url()
    count = 0
    r = rq.session()
    while True:
        try:
            data = r.get(url, headers=headers)
            print("g_p_ca_try")
            print(data)
            return data.json()
        except:
            print("g_p_ca_except")
            count += 1
            if count >= 3:
                return False


def getWeather():
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?lat=35.6340084392334&lon=139.879596507559&units=metric&appid={os.environ["OPENWEATHERMAPAPI_KEY"]}'
    except KeyError:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat=35.6340084392334&lon=139.879596507559&units=metric&appid={local_api.openweathermap_api_key()}"
    r = rq.session()
    data = r.get(url)
    return data.json()
