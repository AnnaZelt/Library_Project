from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for
from project import db,app
from forms import CreateLoan
from project.loans.models import Loans  # Import your CreateLoan form

loans = Blueprint('loans', __name__, template_folder='templates',url_prefix='/loans')


app = Flask(__name__)

@app.route('/create_loan', methods=['GET', 'POST'])

@app.route('/add_customer',methods=['post'])
def add_customer():
        data = request.get_json()
        
        if data:
            customer_id = data.get('customer_id')
            book_id = data.get('book_id')
            due_date = data.get('due_date')
            return_date = data.get('return_date')

            if customer_id and book_id and due_date and return_date:
                new_loan = Loans(customer_id=customer_id, book_id=book_id, due_date=due_date, return_date=return_date)
                db.session.add (new_loan)
                db.session.commit()
                return {'add':"true"}
