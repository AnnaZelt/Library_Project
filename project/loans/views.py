import json
from operator import or_
from models.models import Loan
from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

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

    return json.dumps(res)