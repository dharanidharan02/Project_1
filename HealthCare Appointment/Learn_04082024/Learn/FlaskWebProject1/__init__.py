from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extension import db
def create_app():
    app = Flask(__name__)
    app.secret_key = '12345'

    # Import the necessary module
    from sqlalchemy import create_engine

    # Define the individual connection parameters
    driver = 'ODBC Driver 17 for SQL Server'
    server = 'SANA\\SQLEXPRESS'
    database = 'Swiftcare'

    # Construct the database URI
    uri = f"mssql+pyodbc://{server}/{database}?driver={driver}"

    # Create SQLAlchemy engine
    engine = create_engine(uri, echo=True)  # Set echo=True for debugging purposes

    # Set the URI in Flask app config
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)

    # Import blueprints and register them
    from .views import views
    from .auth import auth
    from .Category import Category
    from .hospital_signup import hospital_signup  # Import the hospital signup blueprint
    from .hospital_login import hospital_login
    from .hospital_dashboard import hospital_dashboard
    from .Appointment import appointment

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(Category, url_prefix='/')
    app.register_blueprint(hospital_dashboard, url_prefix='/')
    # Register hospital signup blueprint
    app.register_blueprint(hospital_signup, url_prefix='/')
    # Register hospital login blueprint
    app.register_blueprint(hospital_login, url_prefix='/')
    app.register_blueprint(appointment, url_prefix='/')




    return app
