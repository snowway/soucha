# -*- coding:utf8 -*-

from flask import *

app = Flask(__name__)


@app.route("/")
def index():
    return "hello flask web"
