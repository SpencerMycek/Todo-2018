from flask import render_template
from app import app


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
