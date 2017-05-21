from app import app
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.csrf import CsrfProtect

CsrfProtect(app)

class CommentForm(Form):
    name = StringField(
        'Name',
        validators = [DataRequired(), Length(max=255)]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])
