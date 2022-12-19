from xml.dom import ValidationErr
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from main.models import User

class RegistrationForm(FlaskForm):
    username= StringField("Username",validators=[DataRequired(),Length(min=2,max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password")])
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose another one")
    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("That Email is taken. Please choose another one")
class LoginForm(FlaskForm):
    username= StringField("username",validators=[DataRequired(),Length(min=2,max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Rember Me")
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    username= StringField("Username",validators=[DataRequired(),Length(min=2,max=20)])
    
    email = StringField('Email',validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg","png"])])
    submit = SubmitField("Update")
    bio= TextAreaField('Bio')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user: 
                raise ValidationError("That username is taken. Please choose another one")
    def validate_email(self,email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("That Email is taken. Please choose another one")


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg","png"])])
    priv = BooleanField("Private")
    id = IntegerField()


class SearchForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('search')

    def validate_name(self,name):
        all_name = User.query.filter_by(username=name.data).first()
        if not all_name:
            raise ValidationError("That Username does not Exist")

    

    

