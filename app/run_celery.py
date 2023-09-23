# -*- coding: utf-8 -*-

import os

from celery import Celery

from app import create_app

#Uma variável local ou nome de parâmetro de função precisam corresponder à expressão regular fornecida,  taskBase.
def make_celery(app=None):
    app = app or create_app('celeryapp', os.path.dirname(__file__))
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    taskBase = celery.Task

      class ContextTask(taskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return taskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
