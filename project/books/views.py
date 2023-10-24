import json
from models.models import Book
from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

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
    print('---------------------')

    for book in books:
        res.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "copies_available": book.copies_available,
            "loan_duration_type": book.loan_duration_type
        })
    print('---------------------')

    # Close the session
    session.close()

    return jsonify(res)


@books_blueprint.route('/books/add', methods=["POST"])
def add_books():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract customer information from JSON data
        title = data.get('title')
        author = data.get('author')
        copies_available = data.get('copies_available')
        loan_duration_type = data.get('loan_duration_type')

        # Create a new Customer object
        new_book = Book(title=title, author = author, copies_available = copies_available, loan_duration_type=loan_duration_type)

        # Create a session to interact with the database
        session = Session()

        # Add the new customer to the session
        session.add(new_book)
        session.commit()

        # Close the session
        session.close()

        return jsonify({'message': 'Book added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})
    
@books_blueprint.route('/books/update/<int:id>', methods=["PUT"])
def update_book(id):
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract parameters from JSON data
        title = data.get('title')
        author = data.get('author')
        copies_available = data.get('copies_available')  # Use 'copies_available' here
        loan_duration_type = data.get('loan_duration_type')

        # Create a session to interact with the database
        session = Session()

        # Find the book by its ID
        book = session.query(Book).filter(Book.id == id).first()

        if book:
            # Update book details
            if title is not None:
                book.title = title
            if author is not None:
                book.author = author
            if copies_available is not None:  # Use 'copies_available' here
                book.copies_available = copies_available  # Use 'copies_available' here
            if loan_duration_type is not None:  # Use 'copies_available' here
                book.loan_duration_type = loan_duration_type
            
            # Commit the changes to the database
            session.commit()

            # Close the session
            session.close()

            return jsonify({'message': 'Book updated successfully'})

        return jsonify({'error': 'Book not found'})

    except Exception as e:
        return jsonify({'error': str(e)})



@books_blueprint.route('/books/delete/<int:id>', methods=["DELETE"])
def delete_book(id):
    try:
        # Create a session to interact with the database
        session = Session()

        # Retrieve the customer to delete by their ID
        book = session.query(Book).filter(Book.id == id).first()

        if book:
            # Delete customer
            session.delete(book)

            # Commit the changes to the database
            session.commit()

            # Close the session
            session.close()

            return jsonify({'message': 'Book deleted successfully'})

        return jsonify({'error': 'Book not found'})

    except Exception as e:
        return jsonify({'error': str(e)})
