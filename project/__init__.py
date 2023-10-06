import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from project.customers.view import customers
from project.loans.view import loans
from project.books.view import books

app = Flask(__name__)
UPLOAD_FOLDER = 'UPLOAD_FOLDER'
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = "random string"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')

app.register_blueprint(customers)
app.register_blueprint(loans)
app.register_blueprint(books)

db = SQLAlchemy(app)
Migrate(app,db)

DEBUG = 1

if DEBUG:
    with app.app_context():
            db.create_all()
