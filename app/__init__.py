# coding=utf8


from flask import *
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
moment = Moment()
database = SQLAlchemy()


def create_app(config_name):
    """创建flask app对象"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    for module in [bootstrap, moment, database]:
        module.init_app(app)

    # 导入web模块blueprint
    from web import web
    app.register_blueprint(web)
    return app
