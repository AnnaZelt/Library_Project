import json
from unicodedata import name
from flask import render_template, url_for, redirect, Blueprint
from project import db
from project.books.models import Book
from project.books.forms import CreateBook

books = Blueprint('books', __name__, template_folder='templates')

# CREATE NEW BOOK


@books.route('/create_book.html', methods=['GET', 'POST'])
def create_book():
    form = create_book()

    if form.validate_on_submit():

        book = book(name=form.name.data,
                    author=form.author.data,
                    year_published=form.year_published.data,
                    type=form.type.data)

        db.session.add(book)
        db.session.commit()

        return redirect(url_for('books.list_books'))
    return render_template('create_book.html', form=form)


@books.route('/list_books')
def list_books():
    books_list = Book.query.all()
    res = []
    for x in books_list:
        res.append({"name": x.name, "author": x.author, "published": x.year_published, "loan_period": x.type})
    return json.dumps(res)
