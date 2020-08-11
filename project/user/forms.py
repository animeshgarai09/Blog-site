from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField,FileAllowed
class changeImage(FlaskForm):
    picture=FileField('picture',validators=[FileAllowed(['jpg','jpeg','png'])],render_kw={"id": "picture"})

class changePassword(FlaskForm):
    oldPassword=PasswordField('oldPassword',validators=[DataRequired()],render_kw={"placeholder": "Old Password","class":"form-control"})
    newPassword=PasswordField('newPassword',validators=[DataRequired(),EqualTo('confirmPassword')],render_kw={"placeholder": "New Password","class":"form-control"})
    confirmPassword=PasswordField('confirmPassword',validators=[DataRequired()],render_kw={"placeholder": "Confirm Password","class":"form-control"})
