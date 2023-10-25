from models.models import Book, Loan
from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from flask import request, jsonify

engine = create_engine('sqlite:///library.db')
DBSession = sessionmaker(bind=engine)
loans_blueprint = Blueprint('loans', __name__)

#Get loans
@loans_blueprint.route('/loans', methods=["GET"])
def get_loans():
    res = []
    session = DBSession()
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

    session.close()
    return jsonify(res)

#Get late loans
@loans_blueprint.route('/loans/late', methods=["GET"])
def get_late_loans():
    res = []
    session = DBSession()
    loans = session.query(Loan).all()

    for loan in loans:
        # Check if the due date is in the past and the book has not been returned
        if loan.due_date < datetime.now().date() and loan.return_date is None:
            res.append({
                "id": loan.id,
                "customer_id": loan.customer_id,
                "book_id": loan.book_id,
                "due_date": loan.due_date.strftime('%Y-%m-%d'),  # Format the date as a string
                "return_date": None,
                "loan_start_date": loan.loan_start_date.strftime('%Y-%m-%d')  # Format the date as a string
            })

    session.close()
    return jsonify(res)

#Loan a book
@loans_blueprint.route('/loans/loan', methods=['POST'])
def loan_book():
    session = DBSession()
    data = request.get_json()
    # Extract book information from JSON data
    book_id = data.get('book_id')
    customer_id = data.get('customer_id')
    loan_duration_type = data.get('loan_duration_type')

    # Check if the book is on loan by the customer
    if book_id is None or customer_id is None or loan_duration_type is None:
        return jsonify({'message': 'Invalid request data'}), 400
    
    loan = session.query(Loan).filter_by(customer_id=customer_id, book_id=book_id, return_date=None).first()

    # The book is available for loan; proceed with the loan
    if loan:
        return jsonify({'message': 'Book is already on loan by the customer'})
    else:
        loan_duration_type = int(data.get('loan_duration_type'))
        due_date = datetime.today() + timedelta(days=loan_duration_type)
        new_loan = Loan(
            customer_id=customer_id,
            book_id=book_id,
            due_date=due_date,
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

#Return a loan
@loans_blueprint.route('/loans/return', methods=['POST'])
def return_book():
    session = DBSession()
    data = request.get_json()
    # Extract book information from JSON data
    customer_id = data.get('customer_id')
    book_id = data.get('book_id')
    
    # Check if the book is on loan by the customer
    loan = session.query(Loan).filter_by(customer_id=customer_id, book_id=book_id, return_date=None).first()

    if loan:
        # Update the return_date for the loan
        loan.return_date = datetime.today()
        # Increment the copies_available count for the book
        book = session.query(Book).get(book_id)
        book.copies_available += 1
        session.commit()
        session.close()

        return jsonify({'message': 'Book returned successfully'})
    else:
        return jsonify({'message': 'Book not on loan by the customer'})

