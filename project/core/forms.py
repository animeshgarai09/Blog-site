from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email,length,Regexp
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from project.models import user

class LoginForm(FlaskForm):
    email=StringField('email',validators=[DataRequired(),Email()],render_kw={"placeholder": "Email","class":"input100",'autocomplete':'off'})
    password=PasswordField('password',validators=[DataRequired()],render_kw={"placeholder": "Password","class":"input100"})

class SignupForm(FlaskForm):
    fullname=StringField('fullname',
                        validators=[DataRequired(),
                                    Regexp(r'^([a-zA-Z]+|[a-zA-Z]+\s{1}[a-zA-Z]{1,}|[a-zA-Z]+\s{1}[a-zA-Z]{3,}\s{1}[a-zA-Z]{1,})$',
                                    message='Fullname must containe character and space')],
                        render_kw={"placeholder": "fullname","class":"input100",'autocomplete':'off'})
    email=StringField('email',validators=[DataRequired(),Email()],render_kw={"placeholder": "Email","class":"input100",'autocomplete':'off'})
    password=PasswordField('password',validators=[DataRequired(),length(min=8,max=25,message="Password should be between 4 to 25 characters")],render_kw={"placeholder": "Password","class":"input100"})
    con_password=PasswordField('password',validators=[DataRequired(),EqualTo('password',message="Password didn't match")],render_kw={"placeholder": "Confirm password","class":"input100"})

    def checkEmail(self,field):
        if user.query.filter_by(email=field.data).first():
            raise ValidationError('Your email is already registered')