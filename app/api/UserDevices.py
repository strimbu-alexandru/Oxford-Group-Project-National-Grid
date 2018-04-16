from flask import Flask, url_for, request, render_template, Blueprint, json, Response, session
from flask_restful import Resource, Api

from app.Models import UserDevice, User
from app.api.AuthMethods import authMethods
from app.Database import db_session
from app.ErrorHandler import CustomError
from config import Config

UserDevices = Blueprint('UserDevices',__name__, url_prefix='/userDevices', template_folder='templates')
api = Api(UserDevices)

def getUserId():
	if authMethods.isAuthenticated():
		#get the userId from User database
		authToken = authMethods.getAuthTokenFromJWT(session['JWT'])
		user = authMethods.findUserByToken(authToken)
		return user.userId
	return 'Need to login'							#todo: send back to login if not authenticated

class AddUserDevices(Resource):						#add a new user device using the token to identify the user
	def post(self):
		userId = getUserId()
		#get the parameters from the form
		deviceName = request.form['deviceName']
		consumption = request.form['consumption']
		timeToCharge = request.form['timeToCHarge']
		userDevices = UserDevice(userId = userId, deviceName = deviceName, consumption = consumption, timeToCHarge = timeToCharge)		#if user is valid, proceed to enter it into the user database
		db_session.add(userDevices)
		db_session.commit()
		return "Device added successfully!"

class GetUserDevices(Resource):
	def get(self):
		userId = getUserId()
		userDevices = UserDevice.query.filter(UserDevice.userId == userId).all()
		return json.dumps(userDevices)

class DeleteUserDevice(Resource):					#deletes an entry based on userId and deviceName
	def get(self, deviceName):
		userId = getUserId()
		userDevice = UserDevice.query.filter(UserDevice.userId == userId, UserDevice.deviceName == deviceName).first()
		if userDevice != None :						#check if the user device exists
			db_session.delete(userDevice)			#then delete it
			db_session.commit()
			return "Device deleted successfully!"
		return "Device not found in the database!"
		
class DeleteAllUserDevices(Resource):				#deletes all the devices for a user
	def get(self):
		userId = getUserId()
		userDevices = UserDevice.query.filter(UserDevice.userId == userId).all()    #get all the devices
		for item in userDevices :
			db_session.delete(item)
		db_session.commit()
		return "Devices deleted successfully"
	

api.add_resource(AddUserDevices, '/add')
api.add_resource(GetUserDevices, '/get')
api.add_resource(DeleteUserDevice, '/delete/<deviceName>')
api.add_resource(DeleteAllUserDevices, '/deleteAll')
