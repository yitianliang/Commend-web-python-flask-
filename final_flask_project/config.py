
import os

DEBUG = True

SECRET_KEY = os.urandom(24)

# 表示最大上传文件的限制的限制为1MB
# 添加完成即可，Flask会自动处理
# 如果上传的文件超出，会抛出异常，显示无法连接，但程序不会中断
MAX_CONTENT_LENGTH = 1 * 1024 * 1024

DIALECT='mysql'
DRIVER='mysqldb'
USERNAME='root'
PASSWORD='yi1tian2liang3'
HOST='127.0.0.1'
PORT='3306'
DATABASE='project'

SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE) #设置db

SQLALCHEMY_TRACK_MODIFICATIONS=False

