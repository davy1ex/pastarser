from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchPosts(FlaskForm):
    text_field = StringField("text_field")
    submit = SubmitField("ok")
