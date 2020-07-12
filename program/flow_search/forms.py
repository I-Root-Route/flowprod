from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    """
    artist = StringField('Artist')
    genre = StringField('Genre')
    """
    submit = SubmitField('Find Out')