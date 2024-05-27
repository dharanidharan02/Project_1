@hospital_login.route('/hospital_login', methods=['GET', 'POST'])
def hospLogin():
    if request.method == 'POST':
        # Retrieve username and password from form data
        username = request.form['username']
        password = request.form['password']
        
        # Query the hospital table to find the user
        hospital = Hospital.query.filter_by(hospitalName=username, password=password).first()
        
        # If a hospital with the given username and password exists
        if hospital:
            # Store hospital ID in session to maintain login state
            session['hospital_id'] = hospital.hospitalId
            # Redirect to hospital dashboard
            return redirect(url_for('hospital_dashboard.hospdashboard'))

        else:
            # If login fails, show error message
            error_message = "Invalid username or password. Please try again."
            return render_template('hospital_login.html', error_message=error_message)
    else:
        # If request method is GET, render the login form
        return render_template('hospital_login.html')
