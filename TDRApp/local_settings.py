import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "7vtea)7rx)53$uyi3bfgaocg=--1=_$6j10!#70%2s5kln5xez"
"""
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
"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "df721fkr12ic60",
        "USER": "svvmghhjjysbcx",
        "PASSWORD": "90553f1f55f78fe4134bfb45ca9433f056f341aac96b12042cfb79d6cec36b3b",
        "HOST": "ec2-52-22-216-69.compute-1.amazonaws.com",
        "PORT": "5432",
    }
}

DEBUG = True
