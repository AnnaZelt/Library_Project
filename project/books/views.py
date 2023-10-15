import json
from models.models import Book
from flask import Blueprint
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Replace 'your_database_uri' with the actual database URI
engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)

books_blueprint = Blueprint('books', __name__)

@books_blueprint.route('/books', methods=["GET"])
def get_books():
    res = []

    # Create a session to interact with the database
    session = Session()

    # Use the session to query the database
    books = session.query(Book).all()

    for book in books:
        res.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "available copies": book.copies_available
        })

    # Close the session
    session.close()

    return json.dumps(res)
