import json
from unicodedata import name
from flask import render_template, url_for, redirect, Blueprint
from project import db,app
from project.customers.models import Customers
from project.customers.forms import AddCustomer
from flask import request, jsonify

# image upload
from distutils.log import debug
import os
from flask import  flash, request
from werkzeug.utils import secure_filename
from flask import send_from_directory


customers = Blueprint('customers', __name__, template_folder='templates',url_prefix='/customers')

# # UPLOAD_FOLDER = 'UPLOAD_FOLDER'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# # display images from server
# @customers.route('/uploads/<name>')
# def download_file(name):
#     return send_from_directory("../" +os.path.join(app.config['UPLOAD_FOLDER']), name)

# # check what type allow
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @customers.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # print( request.form.get("author"))
        

        
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             student = Students(name=request.form.get("stdent_name"),age=request.form.get("age"),img=filename)
#             db.session.add(student)
#             db.session.commit()
#             print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # return redirect(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('students.list_students'))
#     return  render_template('upl.html')



# # add a new student

# @customers.route('/test', methods=['GET'])
# def test():
#     return "test"



# @customers.route('/add_customer', methods=['POST', 'get'])
# def add_customer():
#     data = request.get_json()

#     if data:
#         name = data.get('name')
#         city = data.get('city')
#         age = data.get('age')

#         if name and city and age:
#             customer = Customers(name=name, city=city, age=age)

#             db.session.add(customer)
#             db.session.commit()

#             return jsonify({"message": "Customer added successfully"})
#         else:
#             return jsonify({"error": "Invalid data provided"})
#     else:
#         return jsonify({"error": "Invalid JSON data provided"})

@app.route('/add_customer',methods=['post'])
def add_customer():
        data = request.get_json()
        
        if data:
            name = data.get('name')
            city = data.get('city')
            age = data.get('age')

            if name and city and age:
                new_customer = Customers(name=name, city=city, age=age)
                db.session.add (new_customer)
                db.session.commit()
                return {'add':"true"}


@customers.route('/list_customers', methods=['get'])
def list_customers():
    customer_list = Customers.query.all()
    res = []
    for x in customer_list:
        res.append({"name": x.name, "city": x.city, "age": x.age})    
    return json.dumps(res)
