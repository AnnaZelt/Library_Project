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

Base.metadata.create_all(engine)  # Creates all tables

# Creates a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
