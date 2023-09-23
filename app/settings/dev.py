# -*- coding: utf-8 -*-
import os

user = os.environ["PG_USER"]
password = os.environ["PG_PASSWORD"]

mail_user = os.environ["MAIL_USER"]
mail_password = os.environ["MAIL_PASSWORD"]

DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
SECRET_KEY = '<replace with a secret key>'
HOST = '0.0.0.0'
PORT = 5000

LOG_FOLDER = '/tmp/'

#Substituição por variaveis de ambiente

SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@postgresql/flask'
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
MAIL_USERNAME = mail_user
MAIL_PASSWORD = mail_password
MAIL_DEFAULT_SENDER = 'support@postfix'
