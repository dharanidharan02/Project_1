from flask import Blueprint, render_template,request,jsonify,session
from datetime import datetime
# from model import Reminder,Message,db


views =Blueprint('views',__name__)



@views.route('/Category', methods =['GET' , 'POST'] )
def category():

    return render_template(
        'Category.html',
        title='Category',
        year=datetime.now().year,
    )


@views.route('/Appointment', methods =['GET' , 'POST'] )
def appointment():

    return render_template(
        'Appointment.html',
        title='Appointment',
        year=datetime.now().year,
    )


# @views.route('/send_reminder', methods=['POST'])
# def send_reminder():
#     data = request.json
#     hospital_id = data.get('hospital_id')
#     user_id = data.get('user_id')
#     content = data.get('content')
#
#     reminder = Reminder(hospital_id=hospital_id, user_id=user_id, content=content)
#     db.session.add(reminder)
#     db.session.commit()
#
#     return jsonify({'message': 'Reminder sent successfully'})
#
# @views.route('/send_message', methods=['POST'])
# def send_message():
#     data = request.json
#     hospital_id = data.get('hospital_id')
#     user_id = data.get('user_id')
#     content = data.get('content')
#
#     message = Message(hospital_id=hospital_id, user_id=user_id, content=content)
#     db.session.add(message)
#     db.session.commit()
#
#     return jsonify({'message': 'Message sent successfully'})
