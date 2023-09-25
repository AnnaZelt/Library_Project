from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

engine = create_engine('sqlite:///library.db', echo=True)
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    status = Column(String, default='active', nullable=False)
    loans = relationship('Loan', back_populates='customer')

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    copies_available = Column(Integer, nullable=False)
    loans = relationship('Loan', back_populates='book')

class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)

    customer = relationship('Customer', back_populates='loans')
    book = relationship('Book', back_populates='loans')

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
