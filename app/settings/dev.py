# -*- coding: utf-8 -*-

import os
dbUser = os.environ["PG_USER"]
dbPassword = os.environ["PG_PASSWORD"]
mailUser = os.environ["MAIL_USERNAME"]
mailPassword = os.environ["MAIL_PASSWORD"]

DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
SECRET_KEY = '<replace with a secret key>'
HOST = '0.0.0.0'
PORT = 5000

LOG_FOLDER = '/tmp/'

SQLALCHEMY_DATABASE_URI = 'postgresql://{dbUser}:{dbPassword}@postgresql/flask'
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

MAIL_SERVER = 'postfix'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USERNAME = mailUser
MAIL_PASSWORD = mailPassword
MAIL_DEFAULT_SENDER = 'support@postfix'
