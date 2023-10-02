from project import db,app

class Customers(db.Model):

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.Integer)
    age = db.Column(db.Integer)

    # initialise an instance (row) of a table/entity
    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    # __repr__ is used to represent an instance, such as for print() function
    def __repr__(self):
        return f"Name: {self.name}"
with app.app_context():
    db.create_all()

