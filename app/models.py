# coding:utf8


from . import database as db


class Brick(db.Model):
    """茶饼数据库模型"""
    __tablename__ = "brick"

    id = db.Column(db.String(36), primary_key=True)
    code = db.Column(db.String)
    name = db.Column(db.String)
    descriptioin = db.Column(db.Text)
    phash = db.Column(db.Text)
    image = db.Column(db.String)

    def __repr__(self):
        return "<茶饼%r(%r)>" % (self.code, self.id)
