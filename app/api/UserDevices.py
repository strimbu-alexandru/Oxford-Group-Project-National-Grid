from flask import Flask, url_for, request, render_template, Blueprint, json, Response, session
from flask_restful import Resource, Api

from app.Models import UserDevices, User
from app.Database import db_session
from app.ErrorHandler import CustomError
from config import Config

Auth = Blueprint('Auth',__name__, url_prefix='/userDevices', template_folder='templates')
api = Api(Auth)

class UserDevicesProcess(Resource):
	def checkUserId(userId):
		user = User.query.filter(User.userId == userId).first()		#get the userId from User database and check if it exists
		if user == None:
			raise CustomError(userId + ': user not found', 600)	

	def post(self):
		userId = request.form['userId']		#get the parameters from the form
		checkUserId(userId)
		deviceName = request.form['deviceName']
		consumption = request.form['consumption']
		timeToCharge = request.form['timeToCHarge']
		userDevices = UserDevices(userId = userId, deviceName = deviceName, consumption = consumption, timeToCHarge = timeToCharge)		#if user is valid, proceed to enter it into the user database
		db_session.add(userDevices)
		db_session.commit()
		return "User added successfully"
			

api.add_resource(UserDevicesProcess '/')


