from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.modle import User
from flask_login import current_user


# ````````` REGISTRATION FORM`````````
class RegistrationForm(FlaskForm):
    username = StringField('Username: ',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sing Up')

    # this method structured required
    # def validate_filed(self,filed):
    #     if True:
    #         raise ValidationError('Error message autometic handale')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() #otherwise return None
        if user:
            raise ValidationError('The Username is taken. Please choose another diffrent one!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() #otherwise return None
        if user:
            raise ValidationError('The Email is taken. Please choose another diffrent one!')


# ```````````LOGIN FORM`````````````
class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
    
    
# ````````` ACCOUNT UPDATE FORM`````````
class AccountUpdateForm(FlaskForm):
    username = StringField('Username: ',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    picture = FileField('Please Choose Your Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first() #otherwise return None
            if user:
                raise ValidationError('The Username is taken. Please choose another diffrent one!')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first() #otherwise return None
            if user:
                raise ValidationError('The Email is taken. Please choose another diffrent one!')




class RequestResetForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset Password')
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that account. You must register first")
    

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')