from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from models import db, Users, Questions, Comments
from werkzeug.security import generate_password_hash
from sqlalchemy import or_
from os import path
from exts import validate_login_register, validate_change_password
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def home():
    questions = Questions.query.order_by(Questions.create_time.desc()).all()
    return render_template('home.html', questions=questions)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username').strip()
        password1 = request.form.get('password1').strip()
        password2 = request.form.get('password2').strip()
        message = validate_login_register(username, password1, password2)
        flash(message)
        if '成功' in message:
            new_user = Users(username=username, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        message = validate_login_register(username, password)
        if '成功' in message:
            session['username'] = username
            session.permanent = True
            return redirect(url_for('home'))
        else:
            flash(message)
            return render_template('login.html')


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/question/', methods=['GET', 'POST'])
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        if hasattr(g, 'user'):
            question_title = request.form.get('question_title').strip()
            question_desc = request.form.get('question_desc').strip()
            author_id = g.user.id
            new_question = Questions(title=question_title, content=question_desc, author_id=author_id)
            db.session.add(new_question)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash('请先登录')
            return redirect(url_for('login'))


@app.route('/details/<question_id>/', methods=['GET', 'POST'])
def details(question_id):
    if request.method == 'GET':
        question_obj = Questions.query.filter(Questions.id == question_id).first()
        return render_template('details.html', question=question_obj)
    else:
        if hasattr(g, 'user'):
            content = request.form.get('comment_desc')
            # comment = Comments(content=content, question_id=question_id, author_id=g.user.id)
            comment = Comments(content=content)
            comment.author = g.user
            comment.question = Questions.query.filter(Questions.id == question_id).first()
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('details', question_id=question_id))
        else:
            flash('请先登录')
            return redirect(url_for('login'))


@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    result = Questions.query.filter(or_(Questions.title.contains(keyword),
                                    Questions.content.contains(keyword))).order_by(
                                    Questions.create_time.desc()).all()
    if result:
        return render_template('home.html', questions=result, search_title=True)
    else:
        return render_template('warn.html')


@app.route('/user/')
def user_center():
    return render_template('user.html')


@app.route('/user/security/', methods=['GET', 'POST'])
def security():
    if request.method == 'GET':
        return render_template('security.html')
    else:
        o_password = request.form.get('o_password')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        message = validate_change_password(g.user, o_password, password1, password2)
        if '成功' in message:
            g.user.password = generate_password_hash(password1)
            db.session.commit()
            session.clear()    # 先clear再flash，否则message也会丢失
            flash(message)
            return redirect(url_for('login'))
        else:
            flash(message)
            return render_template('security.html')


@app.route('/user/avatar/', methods=['GET', 'POST'])
def avatar():
    if request.method == 'POST':
        file = request.files['avatar_upload']
        base_path = path.abspath(path.dirname(__file__))
        filename = str(g.user.id) + '.' + file.filename.rsplit('.', 1)[1]
        file_path = path.join(base_path, 'static', 'images', 'uploads', filename)
        file.save(file_path)
        g.user.avatar_path = 'images/uploads/' + filename
        db.session.commit()
    return render_template('avatar.html')


@app.before_request
def my_before_request():
    username = session.get('username')
    if username:
        g.user = Users.query.filter(Users.username == username).first()


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'login_user': g.user}
    return {}


if __name__ == '__main__':
    app.run()
