from extension import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_picture_path = db.Column(db.String(200))

    # Define the relationship with the Appointment model
    appointments = db.relationship('Appointment', back_populates='user')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_picture_path}')"



#AM: Hospital model
class Hospital(db.Model):
    __tablename__ = 'Hospitals'

    hospitalId = db.Column(db.Integer, primary_key=True)
    hospitalName = db.Column(db.String(255), nullable=False)
    streetAddress = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    stateProvince = db.Column(db.String(100), nullable=False)
    postalCode = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    phoneNumber = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    doctors = db.relationship('Doctor', backref='hospital', lazy=True)
    
    def __repr__(self):
        return f'Hospital(hospitalId={self.hospitalId}, hospitalName={self.hospitalName})'

#AM: Doctor model
class Doctor(db.Model):
    __tablename__ = 'Doctors'

    doctorId = db.Column(db.Integer, primary_key=True)
    doctorName = db.Column(db.String(255), nullable=False)
    hospitalId = db.Column(db.Integer, db.ForeignKey('Hospitals.hospitalId'), nullable=False)
    availabilityStatus = db.Column(db.Boolean, nullable=False)
    category = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'Doctor(doctorId={self.doctorId}, doctorName={self.doctorName}, hospitalId={self.hospitalId}, availabilityStatus={self.availabilityStatus})'

#Am: DoctorAppointment model
class DoctorAppointments(db.Model):
    __tablename__ = 'DoctorAppointments'

    appointmentId = db.Column(db.Integer, primary_key=True)  # Ensure appointmentId is not nullable
    doctorId = db.Column(db.Integer, db.ForeignKey('Doctors.doctorId'), nullable=False)
    appointmentSlots = db.Column(db.Time, nullable=False)
    appointmentAvailable = db.Column(db.Boolean, nullable=False)

    doctor = db.relationship('Doctor', backref='appointments')
    appointments = db.relationship('Appointment', back_populates='DoctorAppointments')

    def __repr__(self):
        return f"<DoctorAppointment {self.appointmentId} - {self.appointmentSlots}>"



class Appointment(db.Model):
    __tablename__ = 'Appointment'

    id = db.Column(db.Integer, primary_key=True)  # Ensure the primary key is named 'id'
    time = db.Column(db.DateTime, nullable=False)  # Assuming you have a field for appointment time
    booked = db.Column(db.Boolean, default=False, nullable=False)  # Boolean field to indicate whether the appointment is booked
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key to associate the appointment with a user
    appointment_id=db.Column(db.Integer, db.ForeignKey('DoctorAppointments.appointmentId'))

    # Define a relationship with the User model
    user = db.relationship('User', back_populates='appointments')
    DoctorAppointments = db.relationship('DoctorAppointments', back_populates='appointments')

    def __repr__(self):
        return f'<Appointment {self.id}>'


# class Reminder(db.Model):
#     __tablename__ = 'reminders'
#
#     id = db.Column(db.Integer, primary_key=True)
#     hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#
#     hospital = db.relationship('Hospital', backref='reminders')
#     user = db.relationship('User', backref='reminders')
#
# class Message(db.Model):
#     __tablename__ = 'messages'
#
#     id = db.Column(db.Integer, primary_key=True)
#     hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#
#     hospital = db.relationship('Hospital', backref='messages')
#     user = db.relationship('User', backref='messages')