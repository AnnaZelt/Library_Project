from flask import Blueprint

sports = Blueprint('sports',__name__,url_prefix='/sports')

@sports.route('/swimming')
def sports_swimming():
    return ("swimming")

@sports.route('/biking')
def sports_biking():
    return ("biking")

@sports.route('/soccer')
def sports_soccer():
    return ("biking")