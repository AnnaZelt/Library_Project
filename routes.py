from flask import render_template, request, redirect, flash
from app import app
import webbrowser

from helper import *

# Customer Portal Routes

@app.route('/customer')
def customer_portal():
    return render_template('customer_portal.html')

@app.route('/customer/search', methods=['POST'])
def customer_search():
    query = request.form['query']
    # Implement your customer-specific search function here
    # Return the search results as needed
    results = []  # Replace this with actual search results
    return render_template('customer_portal.html', results=results)

# Librarian Portal Routes

@app.route('/librarian')
def librarian_portal():
    return render_template('librarian_portal.html')

@app.route('/librarian/search', methods=['POST'])
def librarian_search():
    query = request.form['query']
    # Implement your librarian-specific search function here
    # Return the search results as needed
    results = []  # Replace this with actual search results
    return render_template('librarian_portal.html', results=results)

@app.route('/librarian/change_status', methods=['POST'])
def librarian_change_status():
    query = request.form['query']
    result = change_customer_status(query)
    flash(result)
    return redirect('/librarian')

@app.route('/librarian/open_html')
def librarian_open_html():
    webbrowser.open('customers.html')
    return redirect('/librarian')
