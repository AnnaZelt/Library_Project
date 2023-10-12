import json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sports import sports

app = Flask(__name__)
app.register_blueprint(sports)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

# post - insert
@app.route('/students',methods=["post"])
def add_student():
    data= request.json
    print(data["city"])
    newStudent= students(data["name"],data["city"],data["addr"],data["pin"])
    db.session.add (newStudent)
    db.session.commit()

    return {'add':"true"}

# get - select
@app.route('/students',methods=["get"])
def get_students():
    res=[]
    for stu in students.query.all():
         res.append({"id":stu.id,"name":stu.name,"city":stu.city,"addr":stu.addr,"pin":stu.pin})
    return json.dumps( res)


@app.route('/students/<id>',methods=["delete"])
def del_students(id):
    stu= students.query.filter_by(id=id).first()
    db.session.delete(stu)
    db.session.commit()
    return {'del':"true"}

# get - select
@app.route('/posts',methods=["get"])
def get_posts():
    res=[]
    for stu in Post.query.all():
         res.append({"id":stu.id,"content":stu.content})
    return json.dumps( res)

@app.route('/posts/<id>',methods=["delete"])
def del_post(id):
    stu= Post.query.filter_by(id=id).first()
    db.session.delete(stu)
    db.session.commit()
    return {'del':"true"}


@app.route('/students/<id>',methods=["put"])
def upd_students(id):
    data= request.json
    stu= students.query.filter_by(id=id).first()
    stu.name=data["name"]
    db.session.commit()
    return {'upd':"true"}

def init_data():
    post1 = Post(title='Post The First', content='Content for the first post')
    post2 = Post(title='Post The Second', content='Content for the Second post')
    post3 = Post(title='Post The Third', content='Content for the third post')

    comment1 = Comment(content='Comment for the first post', post=post1)
    comment2 = Comment(content='Comment for the second post', post=post2)
    comment3 = Comment(content='Another comment for the second post', post_id=2)
    comment4 = Comment(content='Another comment for the first post', post_id=1)


    db.session.add_all([post1, post2, post3])
    db.session.add_all([comment1, comment2, comment3, comment4])
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
            db.create_all()
                # init_data()
    app.run(debug = True)