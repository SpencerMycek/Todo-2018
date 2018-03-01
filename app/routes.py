from flask import render_template, flash, redirect, url_for, request, g
from app import app, db
from app.forms import LoginForm, RegistrationForm, TodoForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Todo
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email
from flask_babel import _


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
    return render_template('index.html', title=_('Home'), form=form1,
                           todos=todos.items, next_url=next_url,
                           prev_url=prev_url)










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
    return render_template('index.html', title=_('All'),
                           todos=todos.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/to-do/<id>')
def to_do(id):
    todo = Todo.query.filter_by(id=id).first_or_404()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(request.referrer)






