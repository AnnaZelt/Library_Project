import json
from models.models import Customer
from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
customers_blueprint = Blueprint('customers', __name__)

#Get customers
@customers_blueprint.route('/customers', methods=["GET"])
def get_customers():
    # Wait for a search term from the search by name field
    res = []
    session = Session()
    custoemrs = session.query(Customer).all()

    for customer in custoemrs:
        res.append({
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
        })
    session.close()
    return json.dumps(res)

#Add a customer
@customers_blueprint.route('/customers/add', methods=["POST"])
def add_customers():
    try:
        data = request.get_json()
        # Extract customer information from JSON data
        name = data.get('name')
        email = data.get('email')
        #Create new customer with the data and commit
        new_customer = Customer(name=name, email=email)
        session = Session()
        session.add(new_customer)
        session.commit()
        session.close()
        return jsonify({'message': 'Customer added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

#Update a customer
@customers_blueprint.route('/customers/update/<int:id>', methods=["PUT"])
def update_customer(id):
    try:
        data = request.get_json()
        # Extract parameters from JSON data
        name = data.get('name')
        email = data.get('email')
        session = Session()
        customer = session.query(Customer).filter(Customer.id == id).first()

        #Update customer with the data and commit
        if customer:
            if name is not None:
                customer.name = name
            if email is not None:
                customer.email = email
            session.commit()
            session.close()
            return jsonify({'message': 'Customer updated successfully'})
        return jsonify({'error': 'Customer not found'})
    
    except Exception as e:
        return jsonify({'error': str(e)})

#Delete a customer
@customers_blueprint.route('/customers/delete/<int:id>', methods=["DELETE"])
def delete_customer(id):
    try:
        session = Session()
        customer = session.query(Customer).filter(Customer.id == id).first()

        #Delete and commit
        if customer:
            session.delete(customer)
            session.commit()
            session.close()
            return jsonify({'message': 'Customer deleted successfully'})
        return jsonify({'error': 'Customer not found'})

    except Exception as e:
        return jsonify({'error': str(e)})
