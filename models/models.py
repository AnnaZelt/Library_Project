import datetime
from sqlalchemy import Column, Integer, ForeignKey, Date, String, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy import ForeignKeyConstraint

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    
    # Add a unique constraint for email
    __table_args__ = (UniqueConstraint('email', name='uq_email'),)
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    loans = relationship('Loan', back_populates='customer')

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    copies_available = Column(Integer, nullable=False)
    loans = relationship('Loan', back_populates='book')
    
    # A check constraint to ensure copies_available is non-negative
    __table_args__ = (CheckConstraint('copies_available >= 0', name='check_copies_available'),)

class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    
    # Foreign key constraints for customer and book relationships
    ForeignKeyConstraint(['customer_id'], ['customers.id'], name='fk_customer_id'),
    ForeignKeyConstraint(['book_id'], ['books.id'], name='fk_book_id'),

    # A check constraint for return_date
    __table_args__ = (
        CheckConstraint('return_date IS NULL OR due_date >= return_date', name='check_due_date'),
    )

    customer = relationship('Customer', back_populates='loans')
    book = relationship('Book', back_populates='loans')

engine = create_engine('sqlite:///library.db', echo=True)

# Creates dummy data
def init_data():
    customer1 = Customer(name='Customer 1', email='customer1@example.com')
    customer2 = Customer(name='Customer 2', email='customer2@example.com')

    book1 = Book(title='Title 1', author='Author 1', copies_available=10)
    book2 = Book(title='Title 2', author='Author 2', copies_available=15)

    # Creates a Loan entry (with references to customers and books)
    loan1 = Loan(customer=customer1, book=book1, due_date=datetime.date(2023, 12, 31))
    loan2 = Loan(customer=customer2, book=book2, due_date=datetime.date(2023, 11, 15))

    # Creates all tables
    Base.metadata.create_all(engine)  

    # Creates a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add and commit changes to DB
    session.add_all([customer1, customer2, book1, book2, loan1, loan2])
    session.commit()
