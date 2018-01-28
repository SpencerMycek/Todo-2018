from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class TodoForm(FlaskForm):
    todo = TextAreaField('What needs to be done', validators=[
        DataRequired(), Length(min=1, max=140)])
    month = SelectField('Month',
                        choices=[('Jan', 'January'), ('Feb', 'February'), ('Mar', 'March'),
                                 ('Apr', 'April'), ('May', 'May'), ('Jun', 'June'),
                                 ('Jul', 'July'), ('Aug', 'August'), ('Sep', 'September'),
                                 ('Oct', 'October'), ('Nov', 'November'), ('Dec', 'December')],
                        validators=[DataRequired()])
    year_num = datetime.utcnow().year
    year_choice = []
    for i in range(year_num, year_num+5, 1):
        year_tuple = (str(i), str(i))
        year_choice.append(year_tuple)
    year = SelectField('Year', choices=year_choice, validators=[DataRequired()])
    day_choice = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                  ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
                  ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'),
                  ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'),
                  ('29', '29'), ('30', '30'), ('31', '31')]
    day = SelectField("Day", choices=day_choice, validators=[DataRequired()])
    submit = SubmitField('Submit')


class CompleteForm(FlaskForm):
    complete = BooleanField("Complete")
    submit = SubmitField('Submit')
