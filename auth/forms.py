from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, validators
from wtforms.fields.html5 import EmailField


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = EmailField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    accept_tos = BooleanField('I accept the Terms Of Service', [validators.DataRequired()])
    submit = SubmitField('Submit!')


class LoginForm(FlaskForm):
    email = EmailField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password')
    submit = SubmitField('Submit!')


class ChatForm(FlaskForm):
    text = TextAreaField('', [validators.DataRequired()])
    submit = SubmitField('Submit!')
