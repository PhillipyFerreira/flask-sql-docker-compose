# -*- coding: utf-8 -*-

DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
SECRET_KEY = '<replace with a secret key>'
HOST = '0.0.0.0'
PORT = 5000

#Proteger os diretórios globais de modificação, corrupção ou exclusão de outros arquivos.
LOG_FOLDER = tempfile.mkdtemp()


#Proteger o código fonte em um repositório controlado. Usando senhas no PostgreSQL para autenticação de Usuários e proteger esta senha.
import os
user = os.environ["flask"]
password = os.environ["flask"]

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

#as senhas, credenciais não devem ser codificadas

import os

username = os.getenv('postfix') # Compliant
password = os.getenv('postfix') # Compliant
usernamePassword = 'user=%s&password=%s' % (username, password) # Compliant{code}


MAIL_SERVER = 'postfix'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_DEFAULT_SENDER = 'support@postfix'
