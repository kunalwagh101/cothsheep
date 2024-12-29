from shop import db,app

from datetime import datetime


class Addproduct(db.Model):
    __searchable__ = ['name', 'description']
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80))
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    
    discount = db.Column(db.Integer,default = 0)
    stock   = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=False)
    color = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categorys', lazy=True))

    image1 = db.Column(db.String(150), nullable=False,default="image.jpg")
    image2 = db.Column(db.String(150) )
    image3 = db.Column(db.String(150) )

    def __repr__(self):
        return '<Addproduct %r>' % self.name



class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)



with app.app_context(): 
    db.create_all()   