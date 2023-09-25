import datetime
from sqlalchemy import func
from db_models import *

def borrow_book(customer_id, book_id, days_to_return=14):
    """Borrow a book for a customer."""
    customer = session.query(Customer).filter_by(id=customer_id).first()
    book = session.query(Book).filter_by(id=book_id).first()

    if not customer:
        return "Customer not found"
    if not book:
        return "Book not found"

    if book.copies_available <= 0:
        return "No copies of this book available for borrowing"

    due_date = datetime.date.today() + datetime.timedelta(days=days_to_return)
    loan = Loan(customer=customer, book=book, due_date=due_date)
    book.copies_available -= 1
    session.add(loan)
    session.commit()

    return f"Book '{book.title}' borrowed by {customer.name}. Due on {due_date}"

def return_book(customer_id, book_id):
    """Return a book for a customer."""
    customer = session.query(Customer).filter_by(id=customer_id).first()
    book = session.query(Book).filter_by(id=book_id).first()

    if not customer:
        return "Customer not found"
    if not book:
        return "Book not found"

    loan = (
        session.query(Loan)
        .filter_by(customer=customer, book=book, return_date=None)
        .first()
    )

    if not loan:
        return f"Customer {customer.name} does not have this book on loan"

    loan.return_date = datetime.date.today()
    book.copies_available += 1
    session.commit()

    return f"Book '{book.title}' returned by {customer.name}"

def search_books_by_title_or_author(query):
    """Search for books by title or author (case-insensitive)."""
    query = query.lower()
    books = (
        session.query(Book)
        .filter(
            (func.lower(Book.title).like(f"%{query}%")) |
            (func.lower(Book.author).like(f"%{query}%"))
        )
        .all()
    )
    return books

def search_customers_by_name_or_email(query):
    """Search for customers by name or email (case-insensitive)."""
    query = query.lower()
    customers = (
        session.query(Customer)
        .filter(
            (func.lower(Customer.name).like(f"%{query}%")) |
            (func.lower(Customer.email).like(f"%{query}%"))
        )
        .all()
    )
    return customers

def add_new_book(title, author, copies_available):
    """Add a new book to the library."""
    book = Book(title=title, author=author, copies_available=copies_available)
    session.add(book)
    session.commit()
    return f"Book '{title}' by {author} added to the library."

def add_new_customer(name, email):
    """Add a new customer to the library."""
    customer = Customer(name=name, email=email)
    session.add(customer)
    session.commit()
    return f"Customer '{name}' added to the library."

def change_customer_status(query, new_status='inactive'):
    """Change a customer's status to 'inactive' by default."""
    customers = search_customers_by_name_or_email(query)

    if not customers:
        return "Customer not found"

    for customer in customers:
        customer.status = new_status

    session.commit()

    return f"Customer(s) with '{query}' status changed to '{new_status}'"


