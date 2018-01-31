from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, TodoForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Todo
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form1 = TodoForm()
    if form1.validate_on_submit():
        day = form1.day.data
        month = form1.month.data
        year = form1.year.data
        hour = form1.hour.data
        minute = form1.minute.data
        a_p = form1.a_p.data
        date_str = year + '-' + month + '-' + day + '-' \
            + hour + '-' + minute + '-' + a_p
        datetime_obj = datetime.strptime(date_str, '%Y-%b-%d-%I-%M-%p')
        todo = Todo(body=form1.todo.data, author=current_user,
                    due_date=datetime_obj)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    todos = current_user.all_todos().paginate(
        page, app.config['TODOS_PER_PAGE'], False)
    next_url = url_for('index', page=todos.next_num) \
        if todos.has_next else None
    prev_url = url_for('index', page=todos.prev_num) \
        if todos.has_prev else None
    return render_template('index.html', title='Home', form=form1,
                           todos=todos.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/all')
@login_required
def all():
    page = request.args.get('page', 1, type=int)
    todos = current_user.all_todos().paginate(
        page, app.config['TODOS_PER_ALL'], False)
    next_url = url_for('index', page=todos.next_num) \
        if todos.has_next else None
    prev_url = url_for('index', page=todos.prev_num) \
        if todos.has_prev else None
    return render_template('index.html', title='Home',
                           todos=todos.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/to-do/<id>')
def to_do(id):
    todo = Todo.query.filter_by(id=id).first_or_404()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
