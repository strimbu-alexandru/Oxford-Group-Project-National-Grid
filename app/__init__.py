from flask import Flask, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Link config file
from config import Config
app.config.from_object(Config)

# Set up database
from app.Database import init_db, db_session

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
from app.api.UserDevices import UserDevices
from app.api.ChargingSlots import ChargingSlots
from app.api.SlotCleanUp import SlotCleanUp

app.register_blueprint(Index)
app.register_blueprint(Auth)
app.register_blueprint(Scheduling)
app.register_blueprint(UserDevices)
app.register_blueprint(ChargingSlots)
app.register_blueprint(SlotCleanUp)

# Register custom error handler with app
from app.ErrorHandler import CustomError

@app.errorhandler(CustomError)
def handle_custom_error(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

# Scheduler for async things
from app.api.SlotCleanUp import initScheduler
initScheduler()
