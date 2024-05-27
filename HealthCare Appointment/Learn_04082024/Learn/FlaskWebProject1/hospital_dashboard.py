from flask import Blueprint, render_template, jsonify, request, session
from model import Hospital, Doctor, DoctorAppointments, db, Appointment,User
from flask import Flask
import datetime



hospital_dashboard = Blueprint('hospital_dashboard', __name__)

@hospital_dashboard.route('/hospital_dashboard', methods=['GET', 'POST'])
def hospdashboard():
    if 'hospital_id' in session:
        hospital_id = session['hospital_id']
        hospital = Hospital.query.get(hospital_id)
        doctors = hospital.doctors
        return render_template('hospital_dashboard.html', hospital=hospital, doctors=doctors)
    else:
        return render_template('hospital_login.html')

@hospital_dashboard.route('/save_doctors', methods=['POST'])
def save_doctors():
    try:
        data = request.json
        if 'doctorIds' not in data:
            raise ValueError('Doctor IDs not provided in the request.')

        selected_doctor_ids = data['doctorIds']

        # Update doctor availability status in the database
        Doctor.query.filter(Doctor.doctorId.in_(selected_doctor_ids)).update({'availabilityStatus': True})
        Doctor.query.filter(~Doctor.doctorId.in_(selected_doctor_ids)).update({'availabilityStatus': False})
        db.session.commit()

        return jsonify({'message': 'Doctors availability updated successfully'}), 200
    except Exception as e:
        print(f"Error occurred while updating doctors availability: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update doctors availability. Please try again.'}), 500


# @hospital_dashboard.route('/register_doctor', methods=['POST'])
# def register_doctor():
#     try:
#         data = request.json
#         doctor_name = data['doctorName']
#         category = data['category']
#         hospital_id = session.get('hospital_id')
#
#         availability_status = True
#
#         new_doctor = Doctor(doctorName=doctor_name, category=category, hospitalId=hospital_id,
#                             availabilityStatus=availability_status)
#
#         db.session.add(new_doctor)
#         db.session.commit()
#         generate_appointment_slots(new_doctor.doctorId)
#
#         # Optionally, you can return the newly registered doctor's information in the response
#         return jsonify({'message': 'Doctor registered successfully'}), 200
#     except Exception as e:
#         print(f"Error occurred while registering the new doctor: {e}")
#         db.session.rollback()
#         return jsonify({'error': 'Failed to register the new doctor. Please try again.'}), 500

def generate_appointment_slots(doctor_id):
    # Generate appointment slots for the new doctor
    appointment_slots = []
    # Example: Generate slots for 8 AM to 5 PM with 30-minute intervals
    start_time = datetime.time(8, 0)
    end_time = datetime.time(17, 0)
    interval = datetime.timedelta(minutes=30)
    current_time = datetime.datetime.combine(datetime.date.today(), start_time)
    while current_time <= datetime.datetime.combine(datetime.date.today(), end_time):
        appointment_slots.append(current_time.time())
        current_time += interval

    # Insert generated slots into the database
    for slot in appointment_slots:
        new_appointment = DoctorAppointments(doctorId=doctor_id, appointmentSlots=slot, appointmentAvailable=True)
        db.session.add(new_appointment)
    db.session.commit()


@hospital_dashboard.route('/get_appointment_slots', methods=['GET'])
def get_appointment_slots():
    try:
        doctor_id = request.args.get('doctorId')
        if not doctor_id:
            raise ValueError('Doctor ID not provided in the request.')

        # Fetch appointment slots for the specified doctor ID
        appointment_slots = DoctorAppointments.query.filter_by(doctorId=doctor_id).all()

        # Prepare the slots data to send back to the client
        slots_data = [{'slotId': slot.appointmentId, 'appointmentSlots': str(slot.appointmentSlots)} for slot in appointment_slots]

        return jsonify({'appointmentSlots': slots_data}), 200
    except Exception as e:
        print(f"Error occurred while fetching appointment slots: {e}")
        return jsonify({'error': 'Failed to fetch appointment slots. Please try again.'}), 500

@hospital_dashboard.route('/save_appointment_slots', methods=['POST'])
def save_appointment_slots():
    try:
        data = request.json
        print("Received JSON data:", data)
        # Debug statement

        if 'doctorId' not in data or 'selectedSlots' not in data:
            raise ValueError('Doctor ID or selected slots not provided in the request.')

        doctor_id = data['doctorId']
        print("Doctor ID:", doctor_id)  # Debug statement

        selected_slots = data['selectedSlots']
        print("Selected slots:", selected_slots)


        doctor = Doctor.query.get(doctor_id)
        print("Retrieved Doctor:", doctor)  # Debug statement


        if not doctor:
            raise ValueError('Doctor not found with ID: {}'.format(doctor_id))

        doctor.appointmentSlots = selected_slots
        print(selected_slots)
        DoctorAppointments.query.filter_by(doctorId=doctor_id).update({'appointmentAvailable': False})

        # Set appointmentAvailable to 1 for selected slots
        DoctorAppointments.query.filter(DoctorAppointments.appointmentId.in_(selected_slots)).update(
            {'appointmentAvailable': True})
        db.session.commit()

        return jsonify({'message': 'Appointment slots saved successfully'}), 200
    except Exception as e:
        print(f"Error occurred while saving appointment slots: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to save appointment slots. Please try again.'}), 500

# @hospital_dashboard.route('/edit_doctor', methods=['POST'])
# def edit_doctor():
#     try:
#         data = request.json
#         if 'doctorId' not in data or 'newName' not in data or 'newCategory' not in data:
#             raise ValueError('Doctor ID, new name, or new category not provided in the form data.')
#
#         doctor_id = data['doctorId']
#         new_name = data['newName']
#         new_category = data['newCategory']
#
#         doctor = Doctor.query.get(doctor_id)
#
#         if not doctor:
#             raise ValueError('Doctor not found with the provided ID.')
#
#         doctor.doctorName = new_name
#         doctor.category = new_category
#
#         db.session.commit()
#
#         return jsonify({'message': 'Doctor details updated successfully'}), 200
#     except Exception as e:
#         print(f"Error occurred while updating doctor details: {e}")
#         db.session.rollback()
#         return jsonify({'error': 'Failed to update doctor details. Please try again.'}), 500
#
# @hospital_dashboard.route('/delete_doctor', methods=['POST'])
# def delete_doctor():
#     try:
#         data = request.json
#         if 'doctorId' not in data:
#             raise ValueError('Doctor ID not provided in the request.')
#
#         doctor_id = data['doctorId']
#         doctor = Doctor.query.get(doctor_id)
#
#         if not doctor:
#             raise ValueError('Doctor not found with the provided ID.')
#
#         db.session.delete(doctor)
#         db.session.commit()
#
#         return jsonify({'message': 'Doctor deleted successfully'}), 200
#     except Exception as e:
#         print(f"Error occurred while deleting doctor: {e}")
#         db.session.rollback()
#         return jsonify({'error': 'Failed to delete the doctor. Please try again.'}), 500

@hospital_dashboard.route('/register_doctor', methods=['POST'])
def register_doctor():
    try:
        data = request.json
        doctor_name = data['doctorName']
        category = data['category']
        hospital_id = session.get('hospital_id')

        availability_status = True

        new_doctor = Doctor(doctorName=doctor_name, category=category, hospitalId=hospital_id,
                            availabilityStatus=availability_status)

        db.session.add(new_doctor)
        db.session.commit()
        generate_appointment_slots(new_doctor.doctorId)


        # Optionally, you can return the newly registered doctor's information in the response
        return jsonify({'message': 'Doctor registered successfully'}), 200
    except Exception as e:
        print(f"Error occurred while registering the new doctor: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to register the new doctor. Please try again.'}), 500

@hospital_dashboard.route('/delete_doctor', methods=['POST'])
def delete_doctor():
    try:
        data = request.json
        if 'doctorId' not in data:
            raise ValueError('Doctor ID not provided in the request.')

        doctor_id = data['doctorId']
        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            raise ValueError('Doctor not found with the provided ID.')

        db.session.delete(doctor)
        db.session.commit()

        return jsonify({'message': 'Doctor deleted successfully'}), 200
    except Exception as e:
        print(f"Error occurred while deleting doctor: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete the doctor. Please try again.'}), 500

@hospital_dashboard.route('/edit_doctor', methods=['POST'])
def edit_doctor():
    try:
        data = request.json
        if 'doctorId' not in data or 'newName' not in data or 'newCategory' not in data:
            raise ValueError('Doctor ID, new name, or new category not provided in the form data.')

        doctor_id = data['doctorId']
        new_name = data['newName']
        new_category = data['newCategory']

        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            raise ValueError('Doctor not found with the provided ID.')

        doctor.doctorName = new_name
        doctor.category = new_category

        db.session.commit()

        return jsonify({'message': 'Doctor details updated successfully'}), 200
    except Exception as e:
        print(f"Error occurred while updating doctor details: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update doctor details. Please try again.'}), 500
@hospital_dashboard.route('/api/doctors', methods=['GET'])
def get_doctors():
    try:
        category = request.args.get('category')
        doctors = Doctor.query.filter_by(category=category).all()
        doctor_data = [{'doctorId': doctor.doctorId, 'doctorName': doctor.doctorName, 'category': doctor.category, 'availabilityStatus': doctor.availabilityStatus} for doctor in doctors]
        return jsonify(doctor_data), 200
    except Exception as e:
        print(f"Error occurred while fetching doctors: {e}")
        return jsonify({'error': 'Failed to fetch doctors. Please try again.'}), 500


@hospital_dashboard.route('/get_booked_appointments')
def get_booked_appointments():
    if 'hospital_id' in session:
        hospital_id = session['hospital_id']

        today_date = datetime.date.today()
        # Query booked appointments associated with the hospital's doctors
        booked_appointments = db.session.query(Appointment, Doctor, User) \
            .join(DoctorAppointments, Appointment.appointment_id == DoctorAppointments.appointmentId) \
            .join(Doctor, DoctorAppointments.doctorId == Doctor.doctorId) \
            .join(User, Appointment.user_id == User.id) \
            .filter(Doctor.hospitalId == hospital_id, Appointment.booked == True) \
            .all()

        # Construct JSON response
        booked_appointments_json = [{
            'id': appointment[0].id,
            'time':  f"{today_date} {appointment[0].time.strftime('%H:%M:%S')}",  # Ensure time is formatted correctly
            'doctor_name': appointment[1].doctorName,
            'username': appointment[2].username,
            'email': appointment[2].email
        } for appointment in booked_appointments]

        return jsonify(booked_appointments_json)

    else:
        # If the hospital ID is not in session, return an error response or redirect as appropriate
        return jsonify({'error': 'Hospital ID not found in session'}), 404