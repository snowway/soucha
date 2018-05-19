# -*- coding:utf8 -*-

import os

from fabric.api import *
settings.warn_only=True

@task
def weed():
    """启动weed文件服务器, 用来保存图片"""
    local("ps -ef | egrep -v 'grep|weed' | grep 'weed' | awk '{print $2}' | xargs kill -9")
    local("weed/weed.darwin server -master.port=9333 -volume.port=10333 &")


@task
def db_init():
    """初始化项目, 生成数据库等文件, 只能运行一次"""
    local("source bin/activate && python boot.py db init")


@task
def db_upgrade():
    """数据库结构变化后更新schema"""
    local("source bin/activate && python boot.py db upgrade")


@task
def web():
    """启动web server"""
    weed()
    local("source bin/activate && python boot.py runserver")


@task
def freeze():
    """记录项目pip依赖并保存到requirement.txt中"""
    local("source bin/activate && pip freeze > requirement.txt")


@task
def match():
    """图片对比任务"""
    local("source bin/activate")
    curdir = os.getcwd()
    with lcd("app/cha"):
        for candidate in os.listdir(curdir + "/app/cha/sample/candidate"):
            print("%s%s[%s]%s" % ('-' * 50, r'匹配图片', candidate, '-' * 50))
            local("python imagehash.py sample/candidate/%s sample/original" % candidate)
