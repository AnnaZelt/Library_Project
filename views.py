import datetime
import json
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from models.models import Book, Customer, Loan
from project.books.views import books_blueprint
from project.customers.views import customers_blueprint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)
app.register_blueprint(books_blueprint)
app.register_blueprint(customers_blueprint)

@app.route('/')
def index():
    return render_template('index.html')

# # post - insert
# @app.route('/students',methods=["post"])
# def add_student():
#     data= request.json
#     print(data["city"])
#     newStudent= students(data["name"],data["city"],data["addr"],data["pin"])
#     db.session.add (newStudent)
#     db.session.commit()
#     return {'add':"true"}

# @app.route('/students/<id>',methods=["delete"])
# def del_students(id):
#     stu= students.query.filter_by(id=id).first()
#     db.session.delete(stu)
#     db.session.commit()
#     return {'del':"true"}

# # get - select
# @app.route('/posts',methods=["get"])
# def get_posts():
#     res=[]
#     for stu in Post.query.all():
#          res.append({"id":stu.id,"content":stu.content})
#     return json.dumps( res)

# @app.route('/posts/<id>',methods=["delete"])
# def del_post(id):
#     stu= Post.query.filter_by(id=id).first()
#     db.session.delete(stu)
#     db.session.commit()
#     return {'del':"true"}

# @app.route('/students/<id>',methods=["put"])
# def upd_students(id):
#     data= request.json
#     stu= students.query.filter_by(id=id).first()
#     stu.name=data["name"]
#     db.session.commit()
#     return {'upd':"true"}


