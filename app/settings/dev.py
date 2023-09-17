# -*- coding: utf-8 -*-
import tempfile
import os
DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
SECRET_KEY = '<replace with a secret key>'
HOST = '0.0.0.0'
PORT = 5000
#Escondendo senha e login do banco de dados conforme sonarcloud 
LOG_FOLDER = tempfile.mkdtemp()
user = os.environ["PG_USER"]    
password = os.environ["PG_PASSWORD"]
testedb= os.environ["POSTGRES_DB"]
SQLALCHEMY_DATABASE_URI = f"postgres://{user}:{password}@postgresql/{testedb}"
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

#Escondendo senha e login do e-mail
username_m = os.getenv("username") # Compliant
password_m = os.getenv("password") # Compliant
usernamePassword = 'user=%s&password=%s' % (username, password) # Compliant{code}
MAIL_SERVER = 'postfix'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USERNAME = username_m
MAIL_PASSWORD = password_m
MAIL_DEFAULT_SENDER = 'support@postfix'
