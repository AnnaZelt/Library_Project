from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from project.books.views import books_blueprint
from project.customers.views import customers_blueprint
from project.loans.views import loans_blueprint

# Apply DB,BP and SQLAlchemy configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SECRET_KEY'] = "random string"
app.static_folder = 'static'
db = SQLAlchemy(app)
app.register_blueprint(books_blueprint)
app.register_blueprint(customers_blueprint)
app.register_blueprint(loans_blueprint)

@app.route('/')
def index():
    return render_template('index.html')