from flask import Flask, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.Database import init_db, db_session

app = Flask(__name__)

# Link config file
from config import Config
app.config.from_object(Config)

# Set up database
db = SQLAlchemy(app)
init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

# Secret key for sessions
app.secret_key  = Config.SECRET_KEY

# Link api modules to main app
from app.Index import Index
from app.api.Auth import Auth
from app.api.Scheduling import Scheduling

app.register_blueprint(Index)
app.register_blueprint(Auth)
app.register_blueprint(Scheduling)

# Register custom error handler with app
from app.ErrorHandler import CustomError

@app.errorhandler(CustomError)
def handle_custom_error(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response
