from project import db,app

class Students(db.Model):

    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    age = db.Column(db.Integer)
    img = db.Column(db.String(50))
    

    # initialise an instance (row) of a table/entity
    def __init__(self, name, age,img):
        self.name = name
        self.img = img
        self.age = age


    # __repr__ is used to represent an instance, such as for print() function
    def __repr__(self):
        return f"Name: {self.name}"
with app.app_context():
    db.create_all()
