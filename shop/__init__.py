from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_msearch import Search
from flask_login import LoginManager

import os




# create the extension

# create the app
# basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myshop.db"
app.config['SECRET_KEY'] = 'kunal@123'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

search = Search()
search.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'loginregister'  # type: ignore
login_manager.needs_refresh_message_category = "danger"
login_manager.login_message = u"Please login first"



# app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir,'static/images')

# photos = UploadSet('photos', IMAGES)
# configure_uploads(app,photos)
# patch_request_class(app) 
 


from shop.admin import routes 
from shop.products import routes
from shop.carts import carts
from shop.customers import routes

