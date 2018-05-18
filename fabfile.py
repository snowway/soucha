# -*- coding:utf8 -*-

from fabric.api import *
import os


# 启动web server
@task
def web():
    local("source bin/activate && python boot.py runserver")


# 记录项目pip依赖并保存到requirement.txt中
@task
def freeze():
    local("source bin/activate && pip freeze > requirement.txt")


# 图片对比任务
@task
def match():
    local("source bin/activate")
    curdir = os.getcwd()
    with lcd("app/cha"):
        for candidate in os.listdir(curdir + "/app/cha/sample/candidate"):
            print("%s%s[%s]%s" % ('-' * 50, r'匹配图片', candidate, '-' * 50))
            local("python imagehash.py sample/candidate/%s sample/original" % candidate)
