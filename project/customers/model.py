from flask_sqlalchemy import SQLAlchemy

# Define the Customer model without initializing SQLAlchemy
db_customers = SQLAlchemy()

class Customer(db_customers.Model):
    __tablename__ = 'customers'

    id = db_customers.Column(db_customers.Integer, primary_key=True)
    name = db_customers.Column(db_customers.String, nullable=False)
    email = db_customers.Column(db_customers.String, unique=True, nullable=False)
    loans = db_customers.relationship('Loan', back_populates='customer')
