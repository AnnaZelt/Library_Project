from flask_sqlalchemy import SQLAlchemy

db_loans = SQLAlchemy()

class Loan(db_loans.Model):
    __tablename__ = 'loans'

    id = db_loans.Column(db_loans.Integer, primary_key=True)
    customer_id = db_loans.Column(db_loans.Integer, db_loans.ForeignKey('customers.id'), nullable=False)
    book_id = db_loans.Column(db_loans.Integer, db_loans.ForeignKey('books.id'), nullable=False)
    due_date = db_loans.Column(db_loans.Date, nullable=False)
    return_date = db_loans.Column(db_loans.Date)

    customer = db_loans.relationship('Customer', back_populates='loans')
    book = db_loans.relationship('Book', back_populates='loans')