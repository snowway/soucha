# coding:utf8

from operator import attrgetter

import requests
from flask import render_template, redirect

from app.cha import imagehash
from boot import app
from . import web, forms
from ..models import db, Brick


@web.route("/")
def index():
    """首页"""
    return render_template("index.ja")


@web.route("/bricks")
def bricks():
    """茶饼列表"""
    return render_template("brick/index.ja", bricks=Brick.query.all())


# @web.route("/brick/upload", methods=("POST",))
# def brick_upload():
#     """上传茶饼图片"""
#     url = app.config['SOUCHA_STORAGE_UPLOAD_URL']
#     _file = request.files['image']
#     if _file:
#         res = requests.post(url, files=[("file", _file)])
#     return jsonify(res.json())


@web.route("/brick/edit", methods=("GET", "POST"))
def brick_edit():
    """茶饼添加/编辑"""
    form = forms.BrickEditForm()
    if form.validate_on_submit():
        db.session.add(form.to_brick())
        db.session.commit()
        return redirect("/brick/edit")
    # todo: FLASH成功的消息
    return render_template("brick/edit.ja", form=form)


@web.route("/brick/delete/<id>")
def brick_delete(id):
    """删除茶饼"""
    url = app.config['SOUCHA_STORAGE_VIEW_URL']
    if id:
        brick = Brick.query.filter(Brick.id == id).one()
        if brick:
            # 删除图片
            requests.delete(url + "/" + brick.image)
            db.session.delete(brick)
            db.session.commit()
    return redirect("/bricks")


@web.route("/brick/search", methods=("GET", "POST"))
def brick_search():
    form = forms.BrickSearchForm()
    _bricks = []
    if form.validate_on_submit():
        phash = form.phash(form.thumbnail.data)
        for brick in Brick.query.all():
            brick.similarity = imagehash.hamming(int(phash), int(brick.phash))
            _bricks.append(brick)
            _bricks.sort(key=attrgetter("similarity"))
    return render_template("brick/search.ja", form=form, bricks=_bricks)
