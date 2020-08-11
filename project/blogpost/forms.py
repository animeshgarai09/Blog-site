from flask_wtf import FlaskForm
from wtforms import StringField, TextField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed
class createPost(FlaskForm):
    title=StringField('title',validators=[DataRequired()],render_kw={"placeholder": "Blog Title","class":"input100",'autocomplete':'off'})
    picture=FileField('picture',validators=[FileAllowed(['jpg','jpeg','png'])])
    short=StringField('title',validators=[DataRequired()],render_kw={"placeholder": "Short description","class":"input100",'autocomplete':'off'})