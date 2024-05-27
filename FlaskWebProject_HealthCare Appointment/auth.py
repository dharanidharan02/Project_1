from flask import Blueprint, render_template, request, flash, url_for, session, redirect, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from model import User, db, Appointment
import os


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['loggedin'] = True
            session['id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully!', category='success')
            return redirect(url_for('auth.home'))
        else:
            flash('Incorrect username or password!', category='error')
    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Username already exists. Please use a different one or try logging in.', category='error')
        elif existing_email:
            flash('Email already exists. Please use a different one or try logging in.', category='error')
        elif password != confirm_password:
            flash('Passwords do not match. Please try again.', category='error')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully signed up! Please log in.', category='success')
            return redirect(url_for('auth.login'))
    return render_template('signup.html')


@auth.route('/account')
def account_details():
    if 'id' in session:
        user_id = session['id']
        user = User.query.get(user_id)
        if user:
            return render_template('account.html', user=user)
        else:
            flash('User not found', category='error')
            return redirect(url_for('auth.login'))
    else:
        flash('Please log in to view your account details', category='error')
        return redirect(url_for('auth.login'))


@auth.route('/update-email', methods=['POST'])
def update_email():
    user_id = session.get('id')
    new_email = request.json.get('email')
    if not new_email:
        flash('Email cannot be empty!', category='error')
        return jsonify({'error': 'Email cannot be empty.'}), 400
    user = User.query.get(user_id)
    user.email = new_email
    db.session.commit()
    flash('Email updated successfully!', category='success')
    return jsonify({'message': 'Email updated successfully.', 'new_email': new_email}), 200


# Set the UPLOAD_FOLDER variable to your desired folder path
UPLOAD_FOLDER = r'C:\Users\15485\PycharmProjects\Learn_04082024\Learn\FlaskWebProject1\static\uploads'

# Ensure the directory exists, if not create it
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@auth.route('/upload_profile_picture', methods=['POST'])
def upload_profile_picture():
    # Retrieve user ID from session
    user_id = session.get('id')

    # Get the uploaded file from the form
    if 'profile_picture' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)

    profile_picture = request.files['profile_picture']

    # Check if the user selected a file
    if profile_picture.filename == '':
        flash('No selected file', category='error')
        return redirect(request.url)

    # Save the uploaded file to a folder
    if profile_picture:
        # Save the file to a specific location
        filename = secure_filename(profile_picture.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        profile_picture.save(filepath)

        # Generate URL for the uploaded file
        profile_picture_url = url_for('static', filename='uploads/' + filename)

        # Update the user's profile picture path in the database
        user = User.query.get(user_id)
        user.profile_picture_path = profile_picture_url
        db.session.commit()

        # Prepare JSON response
        response_data = {
            'profile_picture_url': profile_picture_url
        }
        return jsonify(response_data), 200
    else:
        flash('Failed to upload profile picture. Please try again later.', category='error')
        return redirect(url_for('auth.account_details'))


@auth.route('/delete_account', methods=['POST'])
def delete_account():
    # Check if the user is logged in
    if 'id' in session:
        user_id = session['id']
        # Retrieve the user from the database
        user = User.query.get(user_id)
        if user:
            # Delete the user from the database
            db.session.delete(user)
            db.session.commit()
            # Clear the session and redirect to the login page
            session.clear()
            flash('Your account has been deleted successfully.', category='success')
            return redirect(url_for('auth.login'))
        else:
            flash('User not found.', category='error')
            return redirect(url_for('auth.account_details'))
    else:
        flash('Please log in to delete your account.', category='error')
        return redirect(url_for('auth.login'))



@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.dashboard'))

@auth.route('/')
def dashboard():
    return render_template('dashboard.html')

@auth.route('/home')
def home():
    return render_template('home.html')


from flask import jsonify, session

@auth.route('/api/user')
def get_user_id():
    if 'id' in session:
        user_id = session['id']
        print(user_id)
        return jsonify({'user_id': user_id})
    else:
        return jsonify({'error': 'User ID not found in session'}), 404


