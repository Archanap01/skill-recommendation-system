from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max=30)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', message="Password must contain uppercase, lowercase and digits.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SkillSelectionForm(FlaskForm):
    interests = SelectMultipleField('Select Your Skills', coerce=int, validators=[DataRequired()])
    cost = SelectField('Preferred Cost', choices=[('any', 'Any'), ('Free', 'Free'), ('Paid', 'Paid')])
    level = SelectField('Level', choices=[('any', 'Any'), ('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')])
    submit = SubmitField('Get Recommendations')
