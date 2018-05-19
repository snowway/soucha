# coding:utf8

from uuid import uuid1

import requests
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from boot import app
from config import uploadset
from ..models import Brick


def upload(filename):
    """文件上传"""
    url = app.config['SOUCHA_STORAGE_UPLOAD_URL']
    with open(filename, "rb") as f:
        res = requests.post(url, files=[("file", f)])
        return res.json()['fid']


class BrickEditForm(FlaskForm):
    """
    茶饼图片表单
    """
    code = StringField(u"编号", validators=[DataRequired(message=u"必须输入编号,如#1")])
    name = StringField(u"名称")
    description = TextAreaField(u"描述")
    images = FileField(u'茶饼原图', validators=[
        FileRequired(),
        FileAllowed(uploadset)
    ])
    submit = SubmitField(u"保存")

    def to_brick(self):
        """转换为茶饼数据库对象"""
        brick = Brick(
            id=str(uuid1()),
            code=self.code.data,
            name=self.name.data,
            descriptioin=self.description.data)
        filename = uploadset.save(self.images.data, folder=app.config['UPLOADS_DEFAULT_DEST'])
        brick.image = upload(filename)
        return brick
