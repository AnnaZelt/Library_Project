from models.models import init_data
from views import app

DEBUG = 0
if __name__ == '__main__':
    if DEBUG:
        init_data()
        DEBUG = 0
    app.run(debug = True)