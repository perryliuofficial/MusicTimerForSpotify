from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, StringField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):
    timer = DecimalField('Timer (in minutes)', validators=[DataRequired()])
    submit = SubmitField('Enter')

class PlaylistForm(FlaskForm):
    playlist_id = StringField()
    submit = SubmitField('Enter')