from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,ValidationError
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileRequired
class loginForm(FlaskForm):

    email = StringField(validators=[DataRequired(),Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

class RegistrationForm(FlaskForm):

    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(),Email()])
    password = PasswordField(validators=[DataRequired(),EqualTo('password_confirm')])
    password_confirm = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

class sendMailForm(FlaskForm):

    to = StringField(validators=[DataRequired()])
    subject = StringField(validators=[DataRequired()])
    body = StringField(widget=TextArea())
    att = FileField(validators=[FileRequired()])
    submit = SubmitField("Send")
