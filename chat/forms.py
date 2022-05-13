from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, validators
from flask_wtf.file import FileField, FileAllowed

class ChatForm(FlaskForm):
    text = TextAreaField('')
    picture = FileField('Upload image', validators=[FileAllowed(['jpg', 'png'], 'Image formats only!')])
    submit = SubmitField('Submit!')