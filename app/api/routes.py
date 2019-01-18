from app import db
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from flask import jsonify, request, url_for
from app.models import User, Todo
from datetime import datetime
import pytz
import re


# Return a User
@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


# Return a User based on username
@bp.route('/users/<string:uname>', methods=['GET'])
def get_username(uname):
    data = {
        'id': User.query.filter_by(username=uname).first_or_404().id,
        'username': uname
    }
    return jsonify(data)


# Return a collection of user's tasks
@bp.route('/users/<int:id>/tasks', methods=['GET'])
@token_auth.login_required
def get_tasks(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Todo.to_collection_dict(Todo.query.filter_by(user_id=id), page, per_page, 'api.get_tasks', id=id)
    return jsonify(data)


# Return a user's specific task
@bp.route('/users/<int:id>/tasks/<int:number>', methods=['GET'])
@token_auth.login_required
def get_task(id, number):
    return jsonify(Todo.query.filter_by(user_id=id, id=number).first().to_dict())


# Register a new user
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email, and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


# Modify a user
@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


# Create a new task for a user
@bp.route('/users/<int:id>/tasks', methods=['POST'])
@token_auth.login_required
def create_task(id):
    data = request.get_json() or {}
    if 'body' not in data or 'due_date' not in data:
        return bad_request('must include body and due_date fields')
    if not re.match('[0-9]{4}-[a-zA-Z]{3}-[0-3][0-9]-[0-2][0-9]-[0-5][0-9]', data['due_date']):
        return bad_request('due_date must follow the pattern of year-3LetterMonthCode-day-24HourClock-minute '
                           '(ie:2018-Dec-31-23-59)')
    datetime_obj = datetime.strptime(data['due_date'], '%Y-%b-%d-%H-%M')
    datetime_obj = datetime.astimezone(datetime_obj, pytz.UTC)
    data['user_id'] = id
    data['due_date'] = datetime_obj
    todo = Todo()
    todo.from_dict(data)
    db.session.add(todo)
    db.session.commit()
    response = jsonify(todo.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_task', id=id, number=todo.id)
    return response


# Modify a user's task
@bp.route('/users/<int:id>/tasks/<number>', methods=['PUT'])
@token_auth.login_required
def update_task(id, number):
    todo = Todo.query.filter_by(user_id=id, id=number).first_or_404()
    data = request.get_json() or {}
    if 'complete' in data and data['complete']=='True':
        db.session.delete(todo)
        db.session.commit()
        response = {
                'Message':'Task Completed'
        }
        return jsonify(response)
    else:
        if 'due_date' in data:
            if not re.match('[0-9]{4}-[a-zA-Z]{3}-[0-3][0-9]-[0-2][0-9]-[0-5][0-9]', data['due_date']):
                return bad_request('due_date must follow the pattern of year-3LetterMonthCode-day-24HourClock-minute (ie: XXXX-Dec-XX-XX-XX)')
            else:
                datetime_obj = datetime.strptime(data['due_date'], '%Y-%b-%d-%H-%M')
                datetime_obj = datetime.astimezone(datetime_obj, pytz.UTC)
                data['due_date'] = datetime_obj
        todo.from_dict(data)
        db.session.commit()
        return jsonify(todo.to_dict())
