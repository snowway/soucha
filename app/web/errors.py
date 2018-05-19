# coding:utf8

from flask import render_template
from . import web


@web.app_errorhandler(404)
def page_not_found(error):
    """
    自定义404错误页面
    @web.errorhandler: 只有当前blueprint中的错误才能出发
    @web.app_errorhandler: 全局错误处理器
    """
    return render_template('404.ja', error=error), 404


# @web.app_errorhandler(Exception)
# def internal_server_error(error):
#     """自定义5XX错误页面"""
#     return render_template('500.ja', error=error), 500
