import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "7vtea)7rx)53$uyi3bfgaocg=--1=_$6j10!#70%2s5kln5xez"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "TDRApp",
        "USER": "root",
        "PASSWORD": "Yuta1209",
        "HOST": "",
        "PORT": "",
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

DEBUG = True
