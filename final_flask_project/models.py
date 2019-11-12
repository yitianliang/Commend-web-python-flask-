
from extension import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    image_path = db.Column(db.String(256),nullable=False, server_default='img/7dc3c78d-edf1-4827-b6d4-9043638f8024.jpg')


class Questions(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    #now（）获取的是服务器第一次运行的时间
    #now 是每次创立一个模型时候，都获取当前的时间，不要搞混了
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User', backref = db.backref('questions'))

class Command(db.Model):
    __tablename__ = 'command'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    #通过在backref里添加order_by的函数，是数据库的倒序输出
    question = db.relationship('Questions', backref = db.backref('commands',order_by = id.desc()))
    author = db.relationship('User', backref = db.backref('commands'))
