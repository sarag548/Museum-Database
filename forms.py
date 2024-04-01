from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from flaskDemo import db
#from flaskDemo.models import User, Department, getDepartment, getDepartmentFactory, Employee, Works_On, Project #import the correct models
from flaskDemo.models import User, Artist, Art_Mediums, Art_Work, Era, Medium
from wtforms.fields import DateField

eras = Era.query.with_entities(Era.EraID).distinct()
eraResults=list()
for row in eras:
    rowDict=row._asdict()
    eraResults.append(rowDict)
myEraChoices = [(row['EraID'], row['EraID']) for row in eraResults] #to change display, second ssn change to fname

class ArtistUpdateForm(FlaskForm):
     fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
     lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
     submit = SubmitField('Submit')

class ArtworkUpdateForm(FlaskForm):
    newEra = SelectField('Era ID:', choices=myEraChoices, coerce=int)
    submit = SubmitField("Update this Artwork's Date")

    def validate_newEra(self, newEra):
        era = Era.query.filter_by(EraID=newEra.data).first()
        if era is None:
            raise ValidationError("Sorry, that era doesn't appear to exist")
        #is the title still the same one

class DateSearchForm(FlaskForm):
    start = IntegerField('Lower Date Range', validators=[DataRequired(), NumberRange(min=0, max=2022)])
    end = IntegerField('Higher Date Range', validators=[DataRequired(), NumberRange(min=0, max=2022)])
    submit = SubmitField('Search')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
