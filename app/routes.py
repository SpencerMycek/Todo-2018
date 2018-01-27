from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Spencer'}
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
    return render_template('index.html', title='Home', user=user, todos=todos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user{}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
