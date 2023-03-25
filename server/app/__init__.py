# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:00 上午
# @Author  : xu.junpeng
import os
import socket
import time
from threading import Thread
from flask import Flask
import redis
from celery import Celery
from app.base.basemodel import db
from app.utils.service_manager import ServiceManager
import config
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

from app import app_config

# sentry_sdk.init(
#     dsn="http://7c508a7e6095471f92ebdc29da48d36d@localhost:9000/1",
#     integrations=[FlaskIntegration()]
# )
app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config.from_object("config")
db.init_app(app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=['app.tasks.operate_info', 'app.tasks.spider_tasks']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)

redis_cli = {
    "token": redis.StrictRedis(host=app_config.REDIS_HOST, port=app_config.REDIS_PORT, db=app_config.REDIS_TOEKN_DB)
}


def register_server():
    while True:
        server_info = {
            "node_name": app.config["REGISTER_SERVER_NAME"],
            "node_host": socket.gethostbyname(socket.gethostname()),
            "node_port": app.config["SERVER_PORT"],
            "node_register_time": time.time()
        }
        time.sleep(30)
        server_register = ServiceManager()
        server_register.service_register(server_info)


def create_app():
    # Thread(target=register_server).start()
    from app.urls import bind_urls
    bind_urls(app)
    return app

# if you want create database table;
# you should run `flask shell` in terminal at Apollo, and then do this
# 1. from app.models import *
# 2. from app import db
# 3. db.create_all()
