from os import truncate
import requests as rq
import os

try:
    import local_api

    headers = local_api.headers()
except ImportError:
    headers = {
        "Host": os.environ.get("TDRAPI_HOST"),
        "X-PORTAL-DEVICE-ID": os.environ.get("TDRAPI_PORTAL_DEVICE_ID"),
        "x-api-key": os.environ.get("TDRAPI_API_KEY"),
        "Accept-Language": os.environ.get("TDRAPI_API_ACCEPT_LANGUAGE"),
        "X-PORTAL-OS-VERSION": os.environ.get("TDRAPI_API_PORTAL_OS_VERSION"),
        "X-PORTAL-APP-VERSION": os.environ.get("TDRAPI_API_PORTAL_APP_VERSION"),
        "Accept-Encoding": os.environ.get("TDRAPI_API_ACCEPT_ENCODING"),
        "Connection": os.environ.get("TDRAPI_API_CONNECTION"),
        "Content-Type": os.environ.get("TDRAPI_API_CONTENT_TYPE"),
        "User-Agent": os.environ.get("TDRAPI_API_USER_AGENT"),
        "X-PORTAL-LANGUAGE": os.environ.get("TDRAPI_API_PORTAL_LANGUAGE"),
        "Accept": os.environ.get("TDRAPI_API_ACCEPT"),
        "Cookie": os.environ.get("TDRAPI_API_COOKIE"),
        "X-PORTAL-AUTH": os.environ.get("TDRAPI_API_PORTAL_AUTH"),
    }


def get_facilities():
    try:
        url = os.environ.get("TDRAPI_FACILITIES_URL")
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
        url = os.environ.get("TDRAPI_FACILITIES_CONDITIONS_URL")
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
        url = os.environ.get("TDRAPI_PARKS_CONDITIONS_URL")
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
        url = os.environ.get("TDRAPI_PARKS_CALENDARS_URL")
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
        url = f'http://api.openweathermap.org/data/2.5/weather?lat=35.6340084392334&lon=139.879596507559&units=metric&appid={os.environ.get("OPENWEATHERMAPAPI_KEY")}'
    except KeyError:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat=35.6340084392334&lon=139.879596507559&units=metric&appid={local_api.openweathermap_api_key()}"
    r = rq.session()
    data = r.get(url)
    return data.json()
