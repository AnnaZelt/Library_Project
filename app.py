from models.models import init_data
from views import app

DEBUG = 1
if __name__ == '__main__':
    if DEBUG:
        init_data()
    app.run(debug = True)