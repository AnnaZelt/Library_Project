import json
from operator import or_
from models.models import Customer
from flask import Blueprint, jsonify, request
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

@customers_blueprint.route('/customers/add', methods=["POST"])
def add_customers():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract customer information from JSON data
        name = data.get('name')
        email = data.get('email')

        # Create a new Customer object
        new_customer = Customer(name=name, email=email)

        # Create a session to interact with the database
        session = Session()

        # Add the new customer to the session
        session.add(new_customer)
        session.commit()

        # Close the session
        session.close()

        return jsonify({'message': 'Customer added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

@customers_blueprint.route('/customers/update/<int:id>', methods=["PUT"])
def update_customer(id):
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract parameters from JSON data
        name = data.get('name')
        email = data.get('email')

        # Create a session to interact with the database
        session = Session()

        # Find the customer by their ID
        customer = session.query(Customer).filter(Customer.id == id).first()

        if customer:
            # Update customer details
            if name is not None:
                customer.name = name
            if email is not None:
                customer.email = email

            # Commit the changes to the database
            session.commit()

            # Close the session
            session.close()

            return jsonify({'message': 'Customer updated successfully'})

        return jsonify({'error': 'Customer not found'})

    except Exception as e:
        return jsonify({'error': str(e)})

@customers_blueprint.route('/customers/delete/<int:id>', methods=["DELETE"])
def delete_customer(id):
    try:
        # Create a session to interact with the database
        session = Session()

        # Retrieve the customer to delete by their ID
        customer = session.query(Customer).filter(Customer.id == id).first()

        if customer:
            # Delete customer
            session.delete(customer)

            # Commit the changes to the database
            session.commit()

            # Close the session
            session.close()

            return jsonify({'message': 'Customer deleted successfully'})

        return jsonify({'error': 'Customer not found'})

    except Exception as e:
        return jsonify({'error': str(e)})
