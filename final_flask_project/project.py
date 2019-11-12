from flask import Flask,render_template,request,redirect,url_for,session,g
import config
from extension import db
from models import User,Questions,Command
from sqlalchemy import desc,or_
from os import path
from werkzeug.utils import secure_filename

#导入限制器，限制用户在没有登陆得时候跳转到登陆界面
from decorators import login_required, allowed_file

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():

    # 通过设置字典，将数据库中的用户数据调取出来，在从后端渲染到前端上
    context={
        # 通过sqlalchemy的query来查询字段
        # 通过order_by来查询以某一个字段为线索的结果。
        # 通过desc将查询结果倒序
        # 通过all()，显示出查询的所有结果
        'questions': Questions.query.order_by(desc('create_time')).all()
    }

    return render_template('index.html',**context) # **调取字典

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # 提取前端用户输入的数据
        username = request.form.get('username')
        password = request.form.get('password')

        # 对数据进行对比
        user = User.query.filter(User.username == username,User.password == password).first()

        if user:
            # 设置session,为了保证用户下次不用登入
            session['user_id'] = user.id
            #如果想在31天内都不需要登入
            session.permanent = True

            return redirect(url_for('index'))

        else:
            return 'Username or Password wrong,pls check'

@app.route('/registered/',methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 检查手机号码是否被注册过
        user = User.query.filter(User.telephone == telephone).first()

        if user:
            return 'your phone number has be resisted'
        else:
            #两次出入的密码得相同
            if password != confirm_password:
                return 'the confirm password is not same with password '
            else:
                #录入用户资料
                user = User(telephone = telephone,username = username, password = password)
                db.session.add(user)
                db.session.commit()

                #如果注册成功，跳转到登录页面
                return redirect(url_for('login'))

@app.route('/post/',methods=['POST','GET'])
@login_required
def post():
    if request.method =='GET':
        return render_template('post.html')
    else:
        #从前端录入form
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question = Questions(title=title, content=content, author=user)
        db.session.add(question)
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/detail/<question_id>/')
def detail(question_id):
    qs = Questions.query.filter(Questions.id == question_id).first()
    return render_template('detail.html',question = qs)

@app.route('/search/')
def search():
    keywords = request.args.get('search')
    # 从sqlalchemy中导出or_函数，对内容和标题进行搜索
    # contains的是搜索包含keywords的内容
    result = Questions.query.filter(or_(Questions.title.contains(keywords),
                                            Questions.content.contains(keywords))).order_by(desc('create_time')).all()
    if result:
        return render_template('search.html', questions=result)
    else:
        return render_template('warn.html')

@app.route('/command/', methods=['POST'])
@login_required
def command():
        content = request.form.get('command')

        # 通过前端传回的question_id，在再后端定位command的位置
        question_id = request.form.get('question_id')
        question = Questions.query.filter(Questions.id == question_id).first()
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        command = Command(content=content,author=user,question=question)

        db.session.add(command)
        db.session.commit()

        return redirect(url_for('detail',question_id = question_id))

@app.route('/log_out/')
def log_out():
    session.pop('user_id')
    return redirect( url_for('index'))

@app.route('/profile/')
def profile():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()

    return render_template('profile.html',user = user)

@app.route('/profile/password/', methods=['POST','GET'])
def password():
    if request.method == 'GET':
        return render_template('changeing_password.html')
    else:
        o_password = request.form.get('o_password')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_id = session.get('user_id')

        # 检查用户的输入信息是否与数据库中的数据一样（password）
        user = User.query.filter(User.id == user_id, User.password == o_password).first()

        if user:
            if password != confirm_password:
                return 'confirm password is not same'

            else:

                # 对用户的密码进行修改
                user.password = password
                db.session.commit()
                return redirect(url_for('profile'))

        else:
            return 'original password is not same'

@app.route('/profile/image/', methods=['GET','POST'])
def image():
    if request.method == 'GET':
        return render_template('image_chane.html')

    else:
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        file = request.files['image_upload']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            base_path = path.abspath(path.dirname(__file__))
            filename = str(user_id) + '.' + file.filename.rsplit('.', 1)[1]
            file_path = path.join(base_path, 'static', 'img', 'upload_image', filename)
            file.save(file_path)

            # 修改user。image_path里的图片
            user.image_path = 'img/upload_image/' + filename
            db.session.commit()

        else:
            return 'Your file does not meet the standard'


        return redirect(url_for('profile'))

# 上下文处理器，如果前端有需要返回的user的值的，无需在视图函数中再次引用
# 可直接使用上下文处理器对前端进行传输
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}

# @app.before_request
# def request():
#     user_id = session.get('user_id')
#     if user_id:
#         g.user = User.query.filter(User.id == user_id).first()

if __name__ == '__main__':
    app.run()
