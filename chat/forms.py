from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, validators

class ChatForm(FlaskForm):
    text = TextAreaField('', [validators.DataRequired()])
    submit = SubmitField('Submit!')