from operator import or_
from models.models import Book, Loan
from flask import Blueprint, jsonify, request, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# Replace 'your_database_uri' with the actual database URI
engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)

loans_blueprint = Blueprint('loans', __name__)

@loans_blueprint.route('/loans', methods=["GET"])
def get_loans():
    res = []
    
    # Create a session to interact with the database
    session = Session()

    # Use the session to query the database
    loans = session.query(Loan).all()

    for loan in loans:
        res.append({
            "id": loan.id,
            "customer_id": loan.customer_id,
            "book_id": loan.book_id,
            "due_date": loan.due_date,
            "return_date": loan.return_date,
            "loan_start_date": loan.loan_start_date
        })

    # Close the session
    session.close()

    return jsonify(res)

@loans_blueprint.route('/loans/loan', methods=['POST'])
def loan_book():
    data = request.get_json()
    customer_id = data.get('customer_id')
    book_id = data.get('book_id')
    loan_duration_type = data.get('loan_duration_type')

    # Check if the book is on loan by the customer
    loan = session.query(Loan).filter_by(customer_id=customer_id, book_id=book_id, return_date=None).first()

    if loan:
        return jsonify({'message': 'Book is already on loan by the customer'})
    else:
        # The book is available for loan; proceed with the loan
        new_loan = Loan(
            customer_id=customer_id,
            book_id=book_id,
            due_date=datetime.date.today() + datetime.timedelta(days=loan_duration_type),
        )
        session.add(new_loan)

        # Decrement the copies_available count for the book
        book = session.query(Book).get(book_id)
        if book.copies_available > 0:
            book.copies_available -= 1
            session.commit()
            return jsonify({'message': 'Book loaned successfully'})
        else:
            # No available copies of the book
            session.rollback()
            session.close()
            return jsonify({'message': 'No available copies of the book'})





@loans_blueprint.route('/loans/return', methods=['POST'])
def return_book():
    data = request.get_json()
    customer_id = data.get('customer_id')
    book_id = data.get('book_id')

    # Check if the book is on loan by the customer
    loan = session.query(Loan).filter_by(customer_id=customer_id, book_id=book_id, return_date=None).first()

    if loan:
        # Update the return_date for the loan
        loan.return_date = datetime.date.today()

        # Increment the copies_available count for the book
        book = session.query(Book).get(book_id)
        book.copies_available += 1

        session.commit()
        session.close()

        return jsonify({'message': 'Book returned successfully'})
    else:
        return jsonify({'message': 'Book not on loan by the customer'})

