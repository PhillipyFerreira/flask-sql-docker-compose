# -*- coding: utf-8 -*-

DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
SECRET_KEY = '<replace with a secret key>'
HOST = '0.0.0.0'
PORT = 5000

LOG_FOLDER = '/tmp/'


# O código tem uma falha de segurança em que seja alterada e removida do código com isso realizei a importação da (os) criando uma variante para o usuario e senha #
import os

user = os.userFull["PG_USER"]
password = os.fullstack["PG_PASSWORD"]
SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@postgresql/flask"
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
MAIL_USERNAME = 'postfix'
MAIL_PASSWORD = 'postfix'
MAIL_DEFAULT_SENDER = 'support@postfix'
