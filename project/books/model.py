from flask_sqlalchemy import SQLAlchemy

db_books = SQLAlchemy()

class Book(db_books.Model):
    __tablename__ = 'books'

    id = db_books.Column(db_books.Integer, primary_key=True)
    title = db_books.Column(db_books.String, nullable=False)
    author = db_books.Column(db_books.String, nullable=False)
    copies_available = db_books.Column(db_books.Integer, nullable=False)
    loans = db_books.relationship('Loan', back_populates='book')
