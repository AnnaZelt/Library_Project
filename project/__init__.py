import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
UPLOAD_FOLDER = 'UPLOAD_FOLDER'
app.config['SECRET_KEY'] = 'supersecret' #to allow us to use forms, not safe for deployment
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
##########################################
############ DATABASE SETUP ##############
##########################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

##########################################
######### REGISTER BLUEPRINTS ############
##########################################

from project.core.views import core
from project.books.views import books
from project.customers.views import customers

app.register_blueprint(customers)
app.register_blueprint(core)
app.register_blueprint(books)
