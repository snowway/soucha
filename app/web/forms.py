# coding:utf8

import base64
import os
import tempfile
import uuid

import requests
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired

from app.cha import imagehash
from boot import app
from config import uploadset
from ..models import Brick


class BrickForm(FlaskForm):
    """茶饼父类"""

    @staticmethod
    def upload(filename):
        """文件上传"""
        url = app.config['SOUCHA_STORAGE_UPLOAD_URL']
        with open(filename, "rb") as f:
            res = requests.post(url, files=[("file", f)])
            return res.json()['fid']

    @staticmethod
    def phash(b64str):
        # data:image/png;base64,iVBXX...
        imgdata = base64.b64decode(b64str[b64str.index("base64,") + 7:])
        with open(os.path.join(tempfile.gettempdir(), str(uuid.uuid1())), "w+") as f:
            f.write(imgdata)
            f.flush()
            return str(imagehash.phash(f.name))


class BrickSearchForm(BrickForm):
    """茶饼搜索表单"""
    thumbnail = HiddenField(u"", validators=[DataRequired(message=u"必须提供缩略图")])


class BrickEditForm(BrickForm):
    """茶饼编辑表单"""
    code = StringField(u"编号", validators=[DataRequired(message=u"必须输入编号,如#1")])
    name = StringField(u"名称")
    description = TextAreaField(u"描述")
    image = FileField(u'茶饼原图', validators=[FileRequired(message=u"请选择图片"), FileAllowed(uploadset)])
    thumbnail = HiddenField(u"", validators=[DataRequired(message=u"必须提供缩略图")])
    submit = SubmitField(u"保存")

    def to_brick(self):
        """转换为茶饼数据库对象"""
        brick = Brick(
            id=str(uuid.uuid1()),
            code=self.code.data,
            name=self.name.data,
            descriptioin=self.description.data)
        # 图片上传到weed
        filename = uploadset.save(self.image.data, folder=app.config['UPLOADS_DEFAULT_DEST'])
        brick.image = self.upload(filename)
        # 分析thumbnail
        brick.phash = self.phash(self.thumbnail.data)
        return brick
