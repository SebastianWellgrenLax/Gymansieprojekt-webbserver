from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=40)
    ])

    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])

    password = PasswordField('Password', validators=[
        DataRequired()
    ])

    confirm_password = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password')
    ])

    submit = SubmitField('Create account')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])

    password = PasswordField('Password', validators=[
        DataRequired()
    ])

    submit = SubmitField('Login')
