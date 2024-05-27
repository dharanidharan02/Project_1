from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from model import Hospital

hospital_login = Blueprint('hospital_login', __name__)

# Define a route for the login page
@hospital_login.route('/hospital_login', methods=['GET', 'POST'])
def hospLogin():
    if request.method == 'POST':
        # Retrieve username and password from form data
        username = request.form['username']
        password = request.form['password']

        # Query the hospital table to find the user
        hospital = Hospital.query.filter_by(hospitalName=username, password=password).first()

        # Check if hospital is found
        if hospital:
            # Store hospital ID in session to maintain login state
            session['hospital_id'] = hospital.hospitalId

            # Redirect to hospital dashboard
            return redirect(url_for('hospital_dashboard.hospdashboard'))
        else:
            # If no hospital is found, show error message
            error_message = "Invalid username or password. Please try again."
            return render_template('hospital_login.html', error_message=error_message)
    else:
        # If request method is GET, render the login form
        return render_template('hospital_login.html')
