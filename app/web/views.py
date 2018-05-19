# coding:utf8

from flask import render_template

from . import web, forms
from ..models import db, Brick





@web.route("/")
def index():
    """首页"""
    return render_template("index.ja")


@web.route("/bricks")
def bricks():
    """茶饼列表"""
    return render_template("bricks.ja", bricks=Brick.query.all())


@web.route("/brick/edit", methods=("GET", "POST"))
def brick_edit():
    """茶饼添加/编辑"""
    form = forms.BrickEditForm()
    if form.validate_on_submit():
        db.session.add(form.to_brick())
        db.session.commit()
    # todo: FLASH成功的消息
    return render_template("brick.ja", form=form)


@web.route("/brick/search", methods=("GET", "POST"))
def brick_search():
    return render_template("index.ja")
