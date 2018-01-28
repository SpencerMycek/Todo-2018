from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, TodoForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Todo
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form1 = TodoForm()
    if form1.validate_on_submit():
        day = form1.day.data
        month = form1.month.data
        year = form1.year.data
        date_str = year + '-' + month + '-' + day
        datetime_obj = datetime.strptime(date_str, '%Y-%b-%d')
        todo = Todo(body=form1.todo.data, author=current_user,
                    due_date=datetime_obj)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))
    todos = [
        {
            'author': {'username': 'Spencer'},
            'body': 'Make dentist appointment',
            'due_date': '2/1/18'
        },
        {
            'author': {'username': 'Spencer'},
            'body': 'Finish Physics homework',
            'due_date': '1/29/18'
        }
    ]
    return render_template('index.html', title='Home', form=form1, todos=todos)


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
