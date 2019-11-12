
from flask import session,redirect,url_for
from functools import wraps

# 登录限制
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ['jpg','jpeg','png','gif']