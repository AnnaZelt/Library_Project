from models.models import Book
from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
books_blueprint = Blueprint('books', __name__)

#Get all books
@books_blueprint.route('/books', methods=["GET"])
def get_books():
    # Wait for a search term from the search by name field
    search_term = request.args.get('name')
    res = []
    session = Session()

    # Use the session to query the database
    if search_term:
        # Perform a case-insensitive search if a search term is provided
        query = session.query(Book).filter(Book.title.ilike(f"%{search_term}%"))
    else:
        # If no search term is provided, get all books
        query = session.query(Book)

    books = query.all()
    for book in books:
        res.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "copies_available": book.copies_available,
            "loan_duration_type": book.loan_duration_type
        })

    session.close()
    return jsonify(res)

#Add a book
@books_blueprint.route('/books/add', methods=["POST"])
def add_books():
    try:
        data = request.get_json()
        # Extract book information from JSON data
        title = data.get('title')
        author = data.get('author')
        copies_available = data.get('copies_available')
        loan_duration_type = data.get('loan_duration_type')

        #Create new book with the data and commit
        new_book = Book(title=title, author = author, copies_available = copies_available, loan_duration_type=loan_duration_type)
        session = Session()
        session.add(new_book)
        session.commit()
        session.close()

        return jsonify({'message': 'Book added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

#Update a book
@books_blueprint.route('/books/update/<int:id>', methods=["PUT"])
def update_book(id):
    try:
        data = request.get_json()
        # Extract parameters from JSON data
        title = data.get('title')
        author = data.get('author')
        copies_available = data.get('copies_available')
        loan_duration_type = data.get('loan_duration_type')
        session = Session()
        book = session.query(Book).filter(Book.id == id).first()

        if book:
            if title is not None:
                book.title = title
            if author is not None:
                book.author = author
            if copies_available is not None:
                book.copies_available = copies_available
            if loan_duration_type is not None:
                book.loan_duration_type = loan_duration_type
            session.commit()
            session.close()

            return jsonify({'message': 'Book updated successfully'})
        
        return jsonify({'error': 'Book not found'})
    except Exception as e:
        return jsonify({'error': str(e)})


#Delete a book
@books_blueprint.route('/books/delete/<int:id>', methods=["DELETE"])
def delete_book(id):
    try:
        session = Session()
        book = session.query(Book).filter(Book.id == id).first()

        #Delete and commit
        if book:
            session.delete(book)
            session.commit()
            session.close()
            return jsonify({'message': 'Book deleted successfully'})
        
        return jsonify({'error': 'Book not found'})
    except Exception as e:
        return jsonify({'error': str(e)})
