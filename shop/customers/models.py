from shop import db,app,login_manager
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.types import TypeDecorator,Text ,TEXT
import json
import secrets


@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(user_id)


class Customer(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    city = db.Column(db.String(120) , nullable=False)
    country = db.Column(db.String(120) , nullable=False)

    contact = db.Column(db.Integer , nullable=False)
    address = db.Column(db.String(120) , nullable=False)
    zipcode = db.Column(db.Integer , nullable=False)
    datetime =db.Column(db.DateTime , nullable=False ,default=datetime.utcnow)

    def __repr__(self):
        return '<Customer %r>' % self.name


class JSONEncodedDict(db.TypeDecorator):

    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return {}
        else :
            return json.dumps(value)

    def process_result_value(self, value, dialect):
         if value is None:
            return {}
         else :
            return json.loads(value)



class CustomerOrder(db.Model) :
      id = db.Column(db.Integer, primary_key=True)
      invoice = db.Column(db.String(80), unique=True, nullable=False)
      status = db.Column(db.String(80),  nullable=False ,default ="pending")
      customer_id = db.Column(db.Integer, nullable =False)
      orders =  db.Column(JSONEncodedDict)

      date = db.Column(db.DateTime , nullable=False ,default=datetime.utcnow)
      

 



      def __repr__(self):
        
         return '<CustomerOrder %r>' % self.invoice






with app.app_context():
    db.create_all()