import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Date, String, create_engine
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
    loans = relationship('Loan', back_populates='customer', cascade='all, delete-orphan')

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    copies_available = Column(Integer, nullable=False)
    loan_duration_type = Column(Integer, nullable=False)
    loans = relationship('Loan', back_populates='book', cascade='all, delete-orphan')
    
    # A check constraint to ensure copies_available is non-negative
    __table_args__ = (CheckConstraint('copies_available >= 0', name='check_copies_available'),)

class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    loan_start_date = Column(DateTime, nullable=True, default=None)
        
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

def init_data():
    Base.metadata.create_all(engine)
    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create customer data
    customer1 = session.query(Customer).filter_by(email='customer1@example.com').first()
    if not customer1:
        customer1 = Customer(name='Customer 1', email='customer1@example.com')
        session.add(customer1)

    customer2 = session.query(Customer).filter_by(email='customer2@example.com').first()
    if not customer2:
        customer2 = Customer(name='Customer 2', email='customer2@example.com')
        session.add(customer2)

    customer3 = session.query(Customer).filter_by(email='customer3@example.com').first()
    if not customer3:
        customer3 = Customer(name='Customer 3', email='customer3@example.com')
        session.add(customer3)

    today = datetime.date.today()
    type1_duration = datetime.timedelta(days=2)
    type2_duration = datetime.timedelta(days=5)
    type3_duration = datetime.timedelta(days=10)

    book1 = session.query(Book).filter_by(title='Title 1').first()
    if not book1:
        book1 = Book(title='Title 1', author='Author 1', copies_available=10, loan_duration_type=1)
        session.add(book1)

    book2 = session.query(Book).filter_by(title='Title 2').first()
    if not book2:
        book2 = Book(title='Title 2', author='Author 2', copies_available=15, loan_duration_type=2)
        session.add(book2)

    book3 = session.query(Book).filter_by(title='Title 3').first() 
    if not book3:
        book3 = Book(title='Title 3', author='Author 3', copies_available=22, loan_duration_type=3)
        session.add(book3)

    # Check if loans with customer and book associations already exist
    loan1 = session.query(Loan).filter_by(customer=customer1, book=book1).first()
    if not loan1:
        loan1 = Loan(
            customer=customer1,
            book=book1,
            due_date=today + type1_duration,
            loan_start_date=today
        )
        session.add(loan1)

    loan2 = session.query(Loan).filter_by(customer=customer2, book=book2).first()
    if not loan2:
        loan2 = Loan(
            customer=customer2,
            book=book2,
            due_date=today + type2_duration,
            loan_start_date=today
        )
        session.add(loan2)
    session.commit()
