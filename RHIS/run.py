import os
import secrets 

from flask import Flask, render_template, redirect ,flash, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin import Admin
from flask_login import login_required ,LoginManager, UserMixin , logout_user, login_user
# forms.py
from flask_wtf import FlaskForm 
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5 import SearchField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed




# __init__.py --------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = "7f36875751b5db07ec9a802cf667a72d" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['FLASK_ADMIN_SWATCH'] = 'Darkly'

admin = Admin(app, name = "microblog", template_mode = 'bootstrap3')
db = SQLAlchemy(app) 
 

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------------------------------------models.py-----------------------------------------------------------------------

# user model 
class User (db.Model, UserMixin) : 
    id = db.Column(db.INTEGER , primary_key = True) 
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False , default = 'default.png')
    password = db.Column(db.String(60), nullable = False)
    
#patient model 
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    ssn = db.Column(db.String(14), unique=True, nullable=False)
    reserve_date = db.Column(db.DateTime, nullable=False, default = datetime.utcnow())
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    address = db.Column(db.String(200))
    password = db.Column(db.String(60), nullable = False)
    scans = db.relationship('Scan', backref='scan_owner', lazy=True)
    birth_date = db.Column(db.String(), nullable=False)
#scan model   
class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scan_type = db.Column(db.String(100), nullable=False)
    scan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    fees = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    def _repr_(self):
        return f"Post('{self.scan_type}', '{self.date}')"



# receptionist model 
class Receptionist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    ssn = db.Column(db.String(14), unique=True, nullable=False)
    dob = db.Column(db.DateTime, nullable=False, default = datetime.utcnow())
    salary = db.Column(db.Integer, nullable=False, default=5000)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(6), nullable=False)

#----------------------------------- end of models--------------------------------------------------------- 

#------------------------------------- forms.py----------------------------------------------------------- 

class LoginForm (FlaskForm) :
    email  = StringField("email" , validators = [DataRequired() ,Email() ])
    password = PasswordField("password" , validators = [DataRequired() ])
    remember = BooleanField("remember_me")
    submit = SubmitField("Login")   


class PatientForm (FlaskForm):
    name = StringField("name", 
                            validators = [DataRequired() , Length (min = 2 , max = 20 )])
    ssn = StringField("ssn",
                            validators = [DataRequired() , Length (min = 2 , max = 20 )])

    birth_date = StringField("birth_date",
                            validators = [DataRequired() , Length (min = 2 , max = 20 )])

    gender = StringField("gender", [DataRequired() , Length (min = 2 , max = 20 )])

    address = TextAreaField ("address", validators = [DataRequired(), Length(max=200)])

    submit = SubmitField("add_Patient")    

    def validate_ssn (self, ssn):
        ssn = Patient.query.filter_by(ssn = ssn.data).first()
        if ssn :
            raise ValidationError("this is patient is already exist")
        
    def validate_email (self, email) :
        email = Patient.query.filter_by(email = email.data).first()
        if  email :
            raise ValidationError("that email is exist for other patient! please try another email")

class PatientScanForm (FlaskForm):
    ssn = StringField("ssn",validators = [DataRequired() , Length (min = 2 , max = 20 )])
    scan_type = StringField("Scan_Type", [DataRequired() , Length (min = 2 , max = 100 )])
    fees = StringField("Fees", [DataRequired() , Length (min = 2 , max = 20 )])
    submit = SubmitField("Notify Technician")

class UpdataPatientForm (FlaskForm):
    name = StringField("name", 
                            validators = [DataRequired() , Length (min = 2 , max = 20 )])
    ssn = StringField("ssn",
                            validators = [DataRequired() , Length (min = 2 , max = 20 )])

    email  = StringField("email" , validators = [DataRequired() ,Email() ])

    gender = StringField("gender", [DataRequired() , Length (min = 2 , max = 20 )])

    address = TextAreaField ("address", validators = [DataRequired(), Length(max=200)])

    submit = SubmitField("Update_patient")    


class UploadScanForm(FlaskForm):
   
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Upload Patient Scan')

#---------------------------end of forms ----------------------------------------------------------------


#------------------------------routes -------------------------------------------------------------------

@app.route("/")
def index ():
    return render_template("home.html")

# def check_validation(email) :

#     splitted_email = email.split("@")
#     domain = splitted_email [1]
#     if domain == "p.com":  return "P"
       
#     if domain == "d.com":  return "D"
     
#     if domain == "r.com":  return "R"
     
#     if domain == "t.com":  return "T"
      
#     else : return "revise in the function"


# @app.route("/login/", methods = ["GET", "POST"])
# def login():
#     if current_user.is_authenticated:
#          return redirect(url_for("index"))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email = form.email.data).first()
#         if  user != None : 
#             if user.password == form.password.data :
#                 login_user(user, remember = form.remember.data )
#                 next_page = request.args.get("next")
#                 print(next)
#                 data = check_validation(user.email)
#                 print(data)
#                 if next_page :
#                     if data == "P" and next_page == '/patient'  :
#                         return redirect(url_for(next_page)) 

#                     elif data == "D" and next_page == '/doctor'  :
#                         return redirect(url_for(next_page)) 
#                     elif data == "T" and next_page == '/techinician' :
#                         return redirect(url_for(next_page)) 
                    
#                     elif data == "R"  and next_page == '/recep' :
#                         return redirect(url_for(next_page)) 

#                     else : 
#                             flash("login denied please try to login again" , "danger")

#                             return redirect(url_for("index"))        
#                 else :
#                     if data == "P":
#                         return redirect(url_for('patient_home')) 

#                     elif data == "D" :
#                         return redirect(url_for('doctor_home')) 

#                     elif data == "T" :
#                         return redirect(url_for('technician')) 
                    
#                     elif data == "R" :
#                         return redirect(url_for('recep')) 

#                     else : 
#                             flash("login denied please try to login again" , "danger")
#                             return redirect(url_for("index"))        
#             else: 
#                 flash("login denied please try to login again" , "danger")
#                 return redirect(url_for("index"))
#         else : 
#             flash("your email or password is incorrect !", "danger")
#     return render_template("login.html" , title = "login" , form = form )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/patient")
# @login_required
def patient_home() :
    return render_template("patient_home.html")



@app.route("/doctor")
# @login_required
def doctor_home() :
    return render_template("doctor_home.html")


@app.route("/recep")
# @login_required
def recep():
    all_patients_scans = Scan.query.all()
    return render_template("receptionist.html", p_data = all_patients_scans )



def create_patient_password(name):
    random_hex = secrets.token_hex(5)
    password = random_hex + name
    
    return password

def create_patient_email(name):
    email = name + "@p.com"
    return email


@app.route("/recep/new_patient", methods=['GET', 'POST'])
def add_new_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(name = form.name.data, ssn = form.ssn.data, email =create_patient_email (form.name.data),  birth_date = form.birth_date.data, gender = form.gender.data, 
                         address = form.address.data, password =  create_patient_password (form.name.data) )
        db.session.add(patient)
        db.session.commit()
        flash('the patient has been created! Add patient Scan', 'success')
        return redirect (url_for('patient_scan'))
    return render_template("new_patient.html", form = form, legend = "Add New Patient" )

@app.route("/recep/new_scan", methods=['GET', 'POST'])
def patient_scan():
    form = PatientScanForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(ssn=form.ssn.data).first()
        if patient:
            scan = Scan(scan_type=form.scan_type.data, fees=form.fees.data, scan_owner=patient)
            db.session.add(scan)
            db.session.commit()
            flash('the patient scan has been created, Technition Notified!', 'success')
            # create email xxxx
            return redirect (url_for('recep'))
        else:
            return redirect(url_for("add_new_patient"))
            
    return render_template("new_scan.html", form = form )

@app.route('/update', methods = ['GET', 'POST'])
def update_patient():
    if request.method == 'POST':
        my_data = Patient.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.ssn = request.form['ssn']
        my_data.email = request.form['email']
        my_data.gender = request.form['gender']
        my_data.address = request.form['address']
        
  
        db.session.commit()
        flash("Patient Updated Successfully","success")
        return redirect(url_for('recep'))
  

@app.route("/delete/<id>/", methods=['POST', "GET"])
def delete_patient_scan(id):
    scan = Scan.query.get(id)
    db.session.delete(scan)
    db.session.commit()
    flash("Your data has been deleted!", "success")
    return redirect(url_for("recep"))


@app.route("/patient/<int:id>/")
def visit_patient(id):
    patient = Patient.query.filter_by(id = id).first()
    patient_data = Scan.query.filter_by(scan_owner = patient)
    print(patient_data)
    return render_template("patient_recep.html", p_data = patient_data)




def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/patients_scans', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/technician")
def technician():
   # all_patient_data = Patient.query.all()
    all_patients_scans = Scan.query.all()
    return render_template("technician.html", p_data = all_patients_scans )


@app.route("/Technician/scan_img/<int:id>/", methods=['GET', 'POST'])
def add_scan_img(id):
     scan = Scan.query.filter_by(id=id).first()
     form = UploadScanForm()
     if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            scan.image_file = picture_file
        db.session.commit()
        flash(f'{scan.scan_owner.name} {scan.scan_type} Scan has been uploaded!', 'success')
        return redirect(url_for('technician'))
     image_file = url_for('static', filename='patients_scans/'+ scan.image_file)
     return render_template('scan_img.html', title='Scan Img', image_file=image_file, form=form, )



if __name__ == "__main__" :
    app.run(debug = True )