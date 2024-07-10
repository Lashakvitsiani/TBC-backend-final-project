from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, equal_to


class LoginForm(FlaskForm):
    username = StringField("Enter username")
    email = EmailField("Enter email")
    password = PasswordField("Enter Password", validators=[DataRequired(), Length(min=7, max=64)])
    login = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Enter username")
    email = EmailField("Enter email")
    password = PasswordField("Enter your password", validators=[DataRequired(), Length(min=7, max=64)])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(),
                                                                   equal_to("password",
                                                                            message="retry password and password do not match")])

    register = SubmitField("Register")


class EditUserForm(FlaskForm):
    username = StringField("username")
    password = StringField("user password")
    email = StringField("user email")
    save = SubmitField("Save Changes")



