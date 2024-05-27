from flask import Flask, render_template, request, Blueprint
import re
from model import Hospital,db

hospital_signup = Blueprint('hospital_signup', __name__)

def validate_phone_number(phone_number):
    # Regular expression to match phone number pattern (only digits)
    pattern = r'^\d+$'
    return re.match(pattern, phone_number)

def validate_password(password):
    # Regular expression to enforce password criteria
    pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z0-9]).{8,}$'
    return re.match(pattern, password)

@hospital_signup.route('/hospital_signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        hospital_name = request.form['hospitalName']
        street_address = request.form['streetAddress']
        city = request.form['city']
        state_province = request.form['stateProvince']
        postal_code = request.form['postalCode']
        country = request.form['country']
        phone_number = request.form['phoneNumber']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        # Server-side validation
        if not validate_phone_number(phone_number):
            return "Invalid phone number. Please enter only digits."

        if not validate_password(password):
            return "Invalid password. Password must have minimum 8 characters, at least 1 number, 1 uppercase letter, 1 lowercase letter, and 1 alphanumeric character."

        # Check if passwords match
        if password != confirm_password:
            return "Passwords do not match. Please try again."
        # Add the new hospital to the database session and commit
        # Create a new Hospital object
        new_hospital = Hospital(hospitalName=hospital_name, streetAddress=street_address, city=city,
                                stateProvince=state_province, postalCode=postal_code, country=country,
                                phoneNumber=phone_number, password=password)
        
        db.session.add(new_hospital)
        db.session.commit()
        # Save the hospital details to the database (or perform any other action)
        # Here you can add your code to save to the database
        # For demonstration purposes, let's print the details
        print("Hospital Details:")
        print(f"Hospital Name: {hospital_name}")
        print(f"Street Address: {street_address}")
        print(f"City: {city}")
        print(f"State/Province: {state_province}")
        print(f"Postal/ZIP Code: {postal_code}")
        print(f"Country: {country}")
        print(f"Phone Number: {phone_number}")

        message = "Hospital signed up successfully!"
        return render_template('hospital_login.html', message=message)
    else:
        return render_template('hospital_signup.html')
