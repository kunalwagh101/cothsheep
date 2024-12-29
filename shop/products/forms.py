
from wtforms import Form, BooleanField,DecimalField , SelectField,TextAreaField, IntegerField,StringField, PasswordField, validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired 

from wtforms.validators import DataRequired,Length

class AddproductForm(Form):
    name = StringField('Product Name',validators= [Length(min=2, max=25),DataRequired()] )
    gender = SelectField('Choose the gender', choices=[('Men', 'Men'), ('Women', 'Women'), ('Girl', 'Girl'), ('Boy', 'Boy')], validators=[Length(min=2, max=25),DataRequired()])

    price = DecimalField('Price',validators= [DataRequired()] )
    discount = IntegerField('Discount' )
    stock = IntegerField('Stock' )
    description = TextAreaField('Discription',validators= [Length(min=4, max=150)] )
    color = TextAreaField('Colors',validators= [Length(min=2, max=25)] )

   
    image1 = FileField('Image 1 ', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only please')])
    image2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only please')])
    image3 = FileField('Image 3', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only please')])

          