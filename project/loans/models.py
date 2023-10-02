from project import db, app

class Loans(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)

    customer = db.relationship('Customer', back_populates='loans')
    book = db.relationship('Book', back_populates='loans')

    def __init__(self, customer_id, book_id, due_date, return_date=None):
        self.customer_id = customer_id
        self.book_id = book_id
        self.due_date = due_date
        self.return_date = return_date

    def __repr__(self):
        return f"Loan ID: {self.id}"

with app.app_context():
    db.create_all()
