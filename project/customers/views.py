import json
from models.models import Customer
from flask import Blueprint
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Replace 'your_database_uri' with the actual database URI
engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)

customers_blueprint = Blueprint('customers', __name__)

@customers_blueprint.route('/customers', methods=["GET"])
def get_customers():
    res = []

    # Create a session to interact with the database
    session = Session()

    # Use the session to query the database
    custoemrs = session.query(Customer).all()

    for customer in custoemrs:
        res.append({
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
        })

    # Close the session
    session.close()

    return json.dumps(res)
