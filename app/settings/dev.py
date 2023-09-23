# -*- coding: utf-8 -*-

DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
SECRET_KEY = '<replace with a secret key>'
HOST = '0.0.0.0'
PORT = 5000

LOG_FOLDER = '/tmp/'

SQLALCHEMY_DATABASE_URI = 'postgresql://{MAIL_USERNAME}:{MAIL_PASSWORD}@postgresql/flask'
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_ENABLE_UTC = False
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_TRACK_STARTED = True
CELERY_RESULT_PERSISTENT = True
CELERYD_POOL_RESTARTS = True
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

from decouple import config

# Configurações de E-mail
MAIL_SERVER = config('MAIL_SERVER')
MAIL_PORT = config('MAIL_PORT', default=25, cast=int)
MAIL_USE_TLS = config('MAIL_USE_TLS', default=False, cast=bool)
MAIL_USERNAME = config('MAIL_USERNAME')
MAIL_PASSWORD = config('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = config('MAIL_DEFAULT_SENDER')