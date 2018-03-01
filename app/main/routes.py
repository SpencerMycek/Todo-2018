from flask import render_template, redirect, url_for, request, jsonify, current_app
from app.main import bp
from app import db
from app.main.forms import TodoForm
from flask_login import current_user, login_required
from app.models import Todo
from datetime import datetime
from flask_babel import _, get_locale


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
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
        page, current_app.config['TODOS_PER_PAGE'], False)
    next_url = url_for('index', page=todos.next_num) \
        if todos.has_next else None
    prev_url = url_for('index', page=todos.prev_num) \
        if todos.has_prev else None
    return render_template('index.html', title=_('Home'), form=form1,
                           todos=todos.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/all')
@login_required
def all():
    page = request.args.get('page', 1, type=int)
    todos = current_user.all_todos().paginate(
        page, current_app.config['TODOS_PER_ALL'], False)
    next_url = url_for('index', page=todos.next_num) \
        if todos.has_next else None
    prev_url = url_for('index', page=todos.prev_num) \
        if todos.has_prev else None
    return render_template('index.html', title=_('All'),
                           todos=todos.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/to-do/<id>')
def to_do(id):
    todo = Todo.query.filter_by(id=id).first_or_404()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(request.referrer)


