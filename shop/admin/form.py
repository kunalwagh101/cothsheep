from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm

from wtforms.validators import DataRequired,Length,Email

class RegistrationForm(Form):
    username = StringField('Username',validators= [Length(min=4, max=25),DataRequired()] )
    email = StringField('Email Address',validators= [Length(min=4, max=25),DataRequired(),Email() ] )
    
    password = PasswordField('Password', validators=[validators.DataRequired(), 
                                                     validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password',validators=[DataRequired()])
 
    
class Loginform(Form) :
        email = StringField('Email Address',validators= [Length(min=4, max=25),DataRequired(),Email() ] )
        password = PasswordField('Password', validators=[validators.DataRequired()])