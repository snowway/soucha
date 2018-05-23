# coding:utf8

"""应用配置"""

import os
import tempfile
from flask_uploads import UploadSet, IMAGES, configure_uploads

basedir = os.path.abspath(os.path.dirname(__file__))
uploadset = UploadSet(extensions=IMAGES)


class Config:
    """通用配置类, 继承后提供各种环境配置"""

    def __init__(self):
        pass

    SECRET_KEY = os.environ.get("SECRET_KEY") or "e7d77c61bf39c64b7db96a335c4b1883"

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    UPLOADS_DEFAULT_DEST = tempfile.gettempdir()

    @staticmethod
    def init_app(app):
        configure_uploads(app, uploadset)


class LocalConfig(Config):
    """本地环境"""
    DEBUG = True
    SOUCHA_STORAGE_UPLOAD_URL = "http://localhost:9333/submit"
    SOUCHA_STORAGE_VIEW_URL = "http://localhost:10333/"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data", "soucha-local.sqlite")


class DevelopmentConfig(Config):
    """开发环境"""
    DEBUG = False
    SOUCHA_STORAGE_UPLOAD_URL = "http://weed.shtianxin.com/submit"
    SOUCHA_STORAGE_VIEW_URL = "http://weed.shtianxin.com"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data", "soucha-dev.sqlite")


config = {
    'local': LocalConfig,
    'development': DevelopmentConfig,
    'default': LocalConfig
}
