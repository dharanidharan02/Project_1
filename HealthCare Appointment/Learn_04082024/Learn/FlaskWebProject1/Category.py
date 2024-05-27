from flask import request, jsonify, Blueprint,flash
from model import Doctor, Hospital,db, DoctorAppointments,Appointment# Import Doctor and Hospital models from appropriate location
from datetime import datetime
Category = Blueprint('Category', __name__)

@Category.route('/api/doctors_with_hospitals', methods=['GET'])
def get_doctors_with_hospitals():
    category = request.args.get('category')

    # Fetch doctors with associated hospitals based on category
    doctors_with_hospitals = db.session.query(Doctor.doctorName, Hospital.hospitalName,Doctor.doctorId).join(Hospital).filter(Doctor.category == category).all()

    # Format data as a list of dictionaries
    data = [{'doctorName': doctor[0], 'hospitalName': doctor[1], 'doctorId':doctor[2]} for doctor in doctors_with_hospitals]

    return jsonify(data)

@Category.route('/api/available_appointments', methods=['GET'])
def get_available_appointments():
    doctor_id = request.args.get('doctorId')

    print(doctor_id)
    # Query the database to fetch available appointments for the doctor
    appointments = DoctorAppointments.query.filter_by(doctorId=doctor_id, appointmentAvailable=True).all()
    print(appointments)
    # Construct a list of appointment data to send to the frontend
    appointment_data = [{'appointmentId': appointment.appointmentId, 'time': appointment.appointmentSlots.strftime('%H:%M:%S.%f')} for appointment in appointments]
    print(appointment_data)
    return jsonify(appointment_data)

@Category.route('/book_appointment', methods=['POST'])
def book_appointment():
    datas = request.json
    print(datas)
    appointment_id = datas.get('appointmentId')
    user_id = datas.get('userId')
    appointment_time = datas.get('time')  # Assuming you send appointment time from the client side

    if not user_id or not appointment_id:
        return jsonify({'error': 'Missing user ID or appointment ID'}), 400

    # Check if the appointment is already booked
    existing_appointment = Appointment.query.filter_by(appointment_id=appointment_id).first()
    if existing_appointment and existing_appointment.booked:
        flash('Appointment already booked. Please try another slot.', category='error')
        return jsonify({'error': 'Appointment is already booked'}), 409

    # Create a new appointment record if it doesn't exist or if it's not booked already
    appointment = Appointment.query.filter_by(appointment_id=appointment_id).first()
    if not appointment:
        appointment = Appointment(time=appointment_time, booked=True, user_id=user_id, appointment_id=appointment_id)
        db.session.add(appointment)
        db.session.commit()

        # Update corresponding doctor's appointment status
        doctor_appointment = DoctorAppointments.query.filter_by(appointmentId=appointment_id).first()
        if doctor_appointment:
            print(doctor_appointment)
            doctor_appointment.appointmentAvailable = False
            db.session.commit()

        return jsonify({'message': 'Appointment booked successfully'}), 200
    else:
        flash('Appointment already exists but not booked. Please try again.', category='error')
        return jsonify({'error': 'Appointment already exists but not booked'}), 400
