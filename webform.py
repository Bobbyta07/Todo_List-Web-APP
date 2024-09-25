from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length


class ListForm(FlaskForm):
    task = StringField(label='Enter Task', validators=[DataRequired()])
    time = DateField(label='Set_timer',  validators=[DataRequired()])
    submit = SubmitField(label='Add Task')


class Login(FlaskForm):
    username = StringField(label='username', validators=[DataRequired()])
    password = StringField(label='password', validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField(label='Submit')


class Registration(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Length(min=8, max=30)])
    password = StringField(label='Password', validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField(label='Submit')



