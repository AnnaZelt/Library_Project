import json
from unicodedata import name
from flask import render_template, url_for, redirect, Blueprint
from project import db,app
from project.students.models import Students
from project.students.forms import AddStudent

# image upload
from distutils.log import debug
import os
from flask import  flash, request
from werkzeug.utils import secure_filename
from flask import send_from_directory


students = Blueprint('students', __name__, template_folder='templates',url_prefix='/students')

# UPLOAD_FOLDER = 'UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# display images from server
@students.route('/uploads/<name>')
def download_file(name):
    return send_from_directory("../" +os.path.join(app.config['UPLOAD_FOLDER']), name)

# check what type allow
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@students.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # print( request.form.get("author"))
        

        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            student = Students(name=request.form.get("stdent_name"),age=request.form.get("age"),img=filename)
            db.session.add(student)
            db.session.commit()
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('students.list_students'))
    return  render_template('upl.html')



# add a new student

@students.route('/test', methods=['GET'])
def test():
    return "test"


@students.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = AddStudent()

    if form.validate_on_submit():

        student = Students(name=form.name.data,age=form.age.data)

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('students.list_students'))
    return render_template('add_student.html', form=form)


@students.route('/students_lst')
def list_students():
    stu_list = Students.query.all()
    # JSON instead HTML
    # res = []
    # for x in clubs_list:
    #     res.append({x.name: x.description})
    # return json.dumps(res)
    return render_template('students.html', stu_list=stu_list)
