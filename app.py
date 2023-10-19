from models.models import init_data
from views import app

DEBUG = 0
if __name__ == '__main__':
    if DEBUG:
        init_data()
    app.run(debug = True)