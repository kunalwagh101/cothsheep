from wtforms import Form, BooleanField,DecimalField ,SubmitField, SelectField,TextAreaField, validators,IntegerField,StringField, PasswordField
from flask_wtf import FlaskForm
from shop.customers.models import Customer
from wtforms.validators import DataRequired,Length,Email,NumberRange,ValidationError



class LoginForm(FlaskForm):
    email = StringField('Email Address',validators= [Length(min=4, max=25),DataRequired(),Email() ] )
    password = PasswordField('Password', validators=[DataRequired()]) 
    
    submit = SubmitField('Login')


def validate_name(self, name) :
    if Customer.query.filter_by(name = name.data).first() :
        raise ValidationError("Name is already register")

def validate_email(self, email) :
    if Customer.query.filter_by(email = email.data).first() :
        raise ValidationError("Email is already register")

class CustomerForm(FlaskForm):
    name = StringField(' Name',validators= [Length(min=2, max=25),validate_name,DataRequired()] )
  
    email = StringField('Email Address',validators= [Length(min=4, max=25),validate_email,DataRequired(),Email() ] )
    password = PasswordField('Password', validators=[validators.DataRequired(), 
                                                     validators.EqualTo('confirm', message='Passwords must match')])  
    confirm = PasswordField('Repeat Password',validators=[DataRequired()])

    city =  StringField('City',validators= [Length(min=2, max=25),DataRequired()] )
    country =  StringField('Country',validators= [Length(min=2, max=25),DataRequired()] )

    contact = IntegerField('Contact',validators= [ NumberRange(min=1000000000, max=9999999999, message='Contact number must be 10 digits'),DataRequired()] )
    address =  StringField('Address',validators= [Length(min=2, max=100) ] )
    zipcode =  IntegerField(' Zipcode',validators= [ NumberRange(min=10000, max=999999   ),DataRequired()] )

    submit = SubmitField('Register')





    