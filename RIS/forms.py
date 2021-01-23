from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from RIS.models import User, Patient, Doctor, Technician, Receptionist
from wtforms.fields.html5 import DateField, DateTimeLocalField
from flask_wtf.file import FileField, FileAllowed
import wtforms


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ReportForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    summary = StringField('Summary', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewDoctor(FlaskForm):
    name = StringField('Doctor Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    ssn = StringField('SSN', validators=[DataRequired()])
    dob = DateField('Birthday', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired(), Length(min=5, max=30)])
    salary = IntegerField('Salary', validators=[DataRequired()])
    submit = SubmitField('Add New Doctor')

    def validate_ssn(self, ssn):
        ssn = Doctor.query.filter_by(ssn=ssn.data).first()
        if ssn:
            raise ValidationError("This ssn already exists")
        
    def validate_email(self, email) :
        email = Doctor.query.filter_by(email = email.data).first()
        if  email :
            raise ValidationError("This Email already exists. try a different one")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class NewReceptionist(FlaskForm):
    name = StringField('Receptionist Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Receptionist Email',
                        validators=[DataRequired(), Email()])
    ssn = StringField('Receptionist SSN', validators=[DataRequired()])
    dob = DateField('Receptionist Birthday', validators=[DataRequired()])
    salary = IntegerField('Receptionist Salary', validators=[DataRequired()])
    gender = StringField('Receptionist Gender', validators=[DataRequired(), Length(min=4, max=6)])
    address = StringField('Receptionist Address', validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('Add New Reciptionist')

    def validate_ssn(self, ssn):
        ssn = Receptionist.query.filter_by(ssn=ssn.data).first()
        if ssn:
            raise ValidationError("This ssn already exists")
        
    def validate_email(self, email) :
        email = Receptionist.query.filter_by(email = email.data).first()
        if  email :
            raise ValidationError("This Email already exists. try a different one")

class NewTechnician(FlaskForm):
    name = StringField('Technician Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Technician Email', validators=[DataRequired(), Email()])
    ssn = StringField('Technician SSN', validators=[DataRequired()])
    dob = DateField('Technician Birthday', validators=[DataRequired()])
    salary = IntegerField('Technician Salary', validators=[DataRequired()])
    gender = StringField('Technician Gender', validators=[DataRequired(), Length(min=4, max=6)])
    address = StringField('Technician Address', validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('Add New Technician')

    def validate_ssn(self, ssn):
        ssn = Technician.query.filter_by(ssn=ssn.data).first()
        if ssn:
            raise ValidationError("This ssn already exists")
        
    def validate_email(self, email) :
        email = Technician.query.filter_by(email = email.data).first()
        if  email :
            raise ValidationError("This Email already exists. try a different one")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class NewPatient(FlaskForm):
    name = StringField("Patient Name", validators = [DataRequired(), Length(min=3, max=50)])
    ssn = StringField("Patient SSN", validators = [DataRequired(), Length (min=14, max=14)])
    email = StringField('Patient Email', validators=[DataRequired(), Email()])
    dob = DateField("Patient Birthday", validators = [DataRequired()])
    gender = StringField("Patient Gender", [DataRequired(), Length(min=4, max=6)])
    address = TextAreaField("Patient Address", validators = [DataRequired(), Length(max=200)])
    submit = SubmitField("Add Patient")    

    def validate_ssn(self, ssn):
        ssn = Patient.query.filter_by(ssn=ssn.data).first()
        if ssn:
            raise ValidationError("this is patient is already exist")
        
    def validate_email(self, email) :
        email = Patient.query.filter_by(email = email.data).first()
        if  email :
            raise ValidationError("that email is exist for other patient! please try another email")

class PatientScanForm(FlaskForm):
    ssn = StringField("SSN", validators=[DataRequired(), Length(min=14, max=14)])
    scan_type = StringField("Scan Type", [DataRequired(), Length (min=2, max=50)])
    fees = StringField("Fees", [DataRequired()])
    technician_ssn = StringField("Technician SSN", [DataRequired() , Length (min=3, max=100)])
    doctor_ssn = StringField("Doctor SSN", [DataRequired(), Length (min=3 , max=100 )])
    submit = SubmitField("Notify Technician")

    def validate_technician_ssn(self, ssn):
        ssn = Technician.query.filter_by(ssn=ssn.data).first()
        if not ssn:
            raise ValidationError("The technician does not exist")
        
    def validate_doctor_ssn(self, ssn):
        ssn = Doctor.query.filter_by(ssn=ssn.data).first()
        if not ssn:
            raise ValidationError("The doctor does not exist")

class UploadScanForm(FlaskForm):
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Upload Patient Scan')

class EventForm(FlaskForm):
    date = DateField("Meeting Day", validators = [DataRequired()])
    doctors = BooleanField('Doctors')
    receptionists = BooleanField('Receptionists')
    technicians = BooleanField('Technicians')
    submit = SubmitField('Notify Staff')